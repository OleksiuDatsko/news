# backend/services/ad_service.py
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from repositories.ad import AdRepository


class AdService:
    def __init__(self, ad_repo: AdRepository):
        self.ad_repo = ad_repo

    def should_show_ads(self, user_permissions: dict) -> bool:
        return not user_permissions.get("no_ads", False)

    def get_ads_for_user(
        self,
        ad_type: Optional[str] = None,
        user_permissions: Optional[dict] = None,
        limit: int = 5,
    ) -> List:
        if user_permissions and not self.should_show_ads(user_permissions):
            return []

        # Отримуємо активні реклами
        current_time = datetime.now()
        ads = self.ad_repo.get_all()

        # Фільтруємо активні реклами
        active_ads = [
            ad
            for ad in ads
            if ad.is_active
            and (not ad.start_date or ad.start_date <= current_time)
            and (not ad.end_date or ad.end_date >= current_time)
        ]

        # Фільтруємо за типом якщо вказано
        if ad_type:
            active_ads = [ad for ad in active_ads if ad.ad_type == ad_type]

        # Обмежуємо кількість
        return active_ads[:limit]

    def get_ads_by_placement(
        self,
        user_permissions: Optional[dict] = None,
        placements: List[str] = ["banner", "sidebar", "popup", "inline", "video"],
    ) -> Dict[str, List]:
        if user_permissions and not self.should_show_ads(user_permissions):
            return {"banner": [], "sidebar": [], "popup": [], "inline": [], "video": []}

        result = {}

        for ad_type in placements:
            result[ad_type] = self.get_ads_for_user(
                ad_type=ad_type, user_permissions=user_permissions, limit=3
            )

        return result

    def record_impression(
        self,
        ad_id: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> bool:
        """
        Реєструє показ реклами.

        Args:
            ad_id: ID рекламного оголошення
            user_id: ID користувача (якщо залогінений)
            session_id: ID сесії (для незалогінених)
            ip_address: IP адреса

        Returns:
            True якщо показ зареєстровано успішно
        """
        try:
            # Отримуємо рекламу
            ad = self.ad_repo.get_by(id=ad_id)
            if not ad:
                raise ValueError(f"Рекламне оголошення з ID {ad_id} не знайдено")

            # Оновлюємо лічильник показів
            self.ad_repo.update(ad, {"impressions_count": ad.impressions_count + 1})

            # Створюємо запис про перегляд
            from repositories import get_ad_view_repo

            ad_view_repo = get_ad_view_repo()
            ad_view_repo.create(
                {
                    "ad_id": ad_id,
                    "user_id": user_id,
                    "session_id": session_id,
                    "ip_address": ip_address,
                    "viewed_at": datetime.now(),
                }
            )

            return True
        except Exception as e:
            print(f"Помилка при реєстрації показу реклами: {str(e)}")
            return False

    def record_click(self, ad_id: int) -> bool:
        try:
            ad = self.ad_repo.get_by(id=ad_id)
            if not ad:
                raise ValueError(f"Рекламне оголошення з ID {ad_id} не знайдено")

            # Оновлюємо лічильник кліків
            self.ad_repo.update(ad, {"clicks_count": ad.clicks_count + 1})

            return True
        except Exception as e:
            print(f"Помилка при реєстрації кліку по рекламі: {str(e)}")
            return False

    def get_ad_statistics(self, ad_id: int) -> Dict:
        ad = self.ad_repo.get_by(id=ad_id)
        if not ad:
            raise ValueError(f"Рекламне оголошення з ID {ad_id} не знайдено")

        ctr = (
            round((ad.clicks_count / ad.impressions_count * 100), 2)
            if ad.impressions_count > 0
            else 0
        )

        return {
            "ad_id": ad.id,
            "title": ad.title,
            "impressions": ad.impressions_count,
            "clicks": ad.clicks_count,
            "ctr": ctr,
            "is_active": ad.is_active,
            "ad_type": ad.ad_type,
        }
