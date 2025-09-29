from flask import Blueprint, request, jsonify
from middleware.auth_middleware import admin_token_required
from repositories import get_ad_repo
from datetime import datetime

ad_bp = Blueprint("ad", __name__)


@ad_bp.route("/", methods=["GET"])
@admin_token_required
def get_all_ads(current_admin):
    """Отримує всі рекламні оголошення"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")  # active, inactive, expired
    ad_type = request.args.get("type")

    try:
        ad_repo = get_ad_repo()
        ads = ad_repo.get_all()

        # Фільтрація за статусом
        if status == "active":
            ads = [
                ad
                for ad in ads
                if ad.is_active and (not ad.end_date or ad.end_date > datetime.now())
            ]
        elif status == "inactive":
            ads = [ad for ad in ads if not ad.is_active]
        elif status == "expired":
            ads = [ad for ad in ads if ad.end_date and ad.end_date < datetime.now()]

        # Фільтрація за типом
        if ad_type:
            ads = [ad for ad in ads if ad.ad_type == ad_type]

        # Сортування за датою створення (новіші спочатку)
        ads = sorted(ads, key=lambda x: x.id, reverse=True)

        # Пагінація
        start = (page - 1) * per_page
        end = start + per_page
        paginated_ads = ads[start:end]

        result = []
        for ad in paginated_ads:
            ad_data = ad.to_dict()

            # Додаємо розраховані поля
            ad_data["ctr"] = (
                round((ad.clicks_count / ad.impressions_count * 100), 2)
                if ad.impressions_count > 0
                else 0
            )
            ad_data["status"] = (
                "active"
                if ad.is_active and (not ad.end_date or ad.end_date > datetime.now())
                else "inactive"
            )
            if ad.end_date and ad.end_date < datetime.now():
                ad_data["status"] = "expired"

            result.append(ad_data)

        return (
            jsonify(
                {
                    "ads": result,
                    "page": page,
                    "per_page": per_page,
                    "total": len(ads),
                    "filters": {"status": status, "type": ad_type},
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/", methods=["POST"])
@admin_token_required
def create_ad(current_admin):
    """Створює нове рекламне оголошення"""
    data = request.get_json()

    if not data.get("title"):
        return jsonify({"msg": "Заголовок є обов'язковим"}), 400
    if not data.get("ad_type"):
        return jsonify({"msg": "Тип реклами є обов'язковим"}), 400

    valid_ad_types = ["banner", "sidebar", "popup", "inline", "video"]
    if data.get("ad_type") not in valid_ad_types:
        return (
            jsonify(
                {"msg": f"Невірний тип реклами. Допустимі: {', '.join(valid_ad_types)}"}
            ),
            400,
        )

    try:
        ad_repo = get_ad_repo()

        # Парсимо дати якщо вони є
        start_date = None
        end_date = None

        if data.get("start_date"):
            start_date = datetime.fromisoformat(
                data.get("start_date").replace("Z", "+00:00")
            )
        if data.get("end_date"):
            end_date = datetime.fromisoformat(
                data.get("end_date").replace("Z", "+00:00")
            )

        ad = ad_repo.create(
            {
                "title": data.get("title"),
                "content": data.get("content"),
                "ad_type": data.get("ad_type"),
                "is_active": data.get("is_active", True),
                "start_date": start_date,
                "end_date": end_date,
                "impressions_count": 0,
                "clicks_count": 0,
            }
        )
        return jsonify(ad.to_dict()), 201
    except ValueError as e:
        return jsonify({"msg": f"Помилка формату дати: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/<int:ad_id>", methods=["GET"])
@admin_token_required
def get_ad(current_admin, ad_id):
    """Отримує рекламне оголошення за ID з детальною статистикою"""
    try:
        ad_repo = get_ad_repo()
        ad = ad_repo.get_by(id=ad_id)
        if not ad:
            return jsonify({"msg": "Рекламне оголошення не знайдено"}), 404

        ad_data = ad.to_dict()

        # Додаємо розраховані метрики
        ad_data["ctr"] = (
            round((ad.clicks_count / ad.impressions_count * 100), 2)
            if ad.impressions_count > 0
            else 0
        )
        ad_data["status"] = (
            "active"
            if ad.is_active and (not ad.end_date or ad.end_date > datetime.now())
            else "inactive"
        )
        if ad.end_date and ad.end_date < datetime.now():
            ad_data["status"] = "expired"

        # Додаємо статистику за останні дні (імітація)
        ad_data["recent_performance"] = {
            "daily_impressions": (
                ad.impressions_count // 30 if ad.impressions_count > 0 else 0
            ),
            "daily_clicks": ad.clicks_count // 30 if ad.clicks_count > 0 else 0,
            "days_active": 30,  # заглушка
        }

        return jsonify(ad_data), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/<int:ad_id>", methods=["PUT"])
@admin_token_required
def update_ad(current_admin, ad_id):
    """Оновлює рекламне оголошення"""
    data = request.get_json()

    try:
        ad_repo = get_ad_repo()
        ad = ad_repo.get_by(id=ad_id)
        if not ad:
            return jsonify({"msg": "Рекламне оголошення не знайдено"}), 404

        update_data = {}
        updatable_fields = ["title", "content", "ad_type", "is_active"]

        for field in updatable_fields:
            if field in data:
                if field == "ad_type":
                    valid_ad_types = ["banner", "sidebar", "popup", "inline", "video"]
                    if data.get(field) not in valid_ad_types:
                        return (
                            jsonify(
                                {
                                    "msg": f"Невірний тип реклами. Допустимі: {', '.join(valid_ad_types)}"
                                }
                            ),
                            400,
                        )
                update_data[field] = data.get(field)

        # Обробка дат
        if "start_date" in data:
            if data.get("start_date"):
                update_data["start_date"] = datetime.fromisoformat(
                    data.get("start_date").replace("Z", "+00:00")
                )
            else:
                update_data["start_date"] = None

        if "end_date" in data:
            if data.get("end_date"):
                update_data["end_date"] = datetime.fromisoformat(
                    data.get("end_date").replace("Z", "+00:00")
                )
            else:
                update_data["end_date"] = None

        updated_ad = ad_repo.update(ad, update_data)
        return jsonify(updated_ad.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": f"Помилка формату дати: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/<int:ad_id>", methods=["DELETE"])
@admin_token_required
def delete_ad(current_admin, ad_id):
    """Видаляє рекламне оголошення"""
    try:
        ad_repo = get_ad_repo()
        ad = ad_repo.get_by(id=ad_id)
        if not ad:
            return jsonify({"msg": "Рекламне оголошення не знайдено"}), 404

        ad_repo.delete(ad)
        return jsonify({"msg": "Рекламне оголошення видалено"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/<int:ad_id>/toggle", methods=["PUT"])
@admin_token_required
def toggle_ad_status(current_admin, ad_id):
    """Перемикає статус активності реклами"""
    try:
        ad_repo = get_ad_repo()
        ad = ad_repo.get_by(id=ad_id)
        if not ad:
            return jsonify({"msg": "Рекламне оголошення не знайдено"}), 404

        updated_ad = ad_repo.update(ad, {"is_active": not ad.is_active})
        return (
            jsonify(
                {
                    "msg": f"Реклама {'активована' if updated_ad.is_active else 'деактивована'}",
                    "ad": updated_ad.to_dict(),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


@ad_bp.route("/statistics", methods=["GET"])
@admin_token_required
def get_ads_statistics(current_admin):
    """Отримує загальну статистику по рекламі"""
    try:
        ad_repo = get_ad_repo()
        ads = ad_repo.get_all()

        current_time = datetime.now()

        stats = {
            "total_ads": len(ads),
            "active_ads": len(
                [
                    ad
                    for ad in ads
                    if ad.is_active and (not ad.end_date or ad.end_date > current_time)
                ]
            ),
            "inactive_ads": len([ad for ad in ads if not ad.is_active]),
            "expired_ads": len(
                [ad for ad in ads if ad.end_date and ad.end_date < current_time]
            ),
            "total_impressions": sum([ad.impressions_count for ad in ads]),
            "total_clicks": sum([ad.clicks_count for ad in ads]),
        }

        stats["overall_ctr"] = (
            round((stats["total_clicks"] / stats["total_impressions"] * 100), 2)
            if stats["total_impressions"] > 0
            else 0
        )

        # Статистика по типах реклами
        ad_types_stats = {}
        for ad in ads:
            if ad.ad_type not in ad_types_stats:
                ad_types_stats[ad.ad_type] = {"count": 0, "impressions": 0, "clicks": 0}
            ad_types_stats[ad.ad_type]["count"] += 1
            ad_types_stats[ad.ad_type]["impressions"] += ad.impressions_count
            ad_types_stats[ad.ad_type]["clicks"] += ad.clicks_count

        # Розраховуємо CTR для кожного типу
        for ad_type in ad_types_stats:
            impressions = ad_types_stats[ad_type]["impressions"]
            clicks = ad_types_stats[ad_type]["clicks"]
            ad_types_stats[ad_type]["ctr"] = (
                round((clicks / impressions * 100), 2) if impressions > 0 else 0
            )

        stats["by_type"] = ad_types_stats

        # Топ 5 найкращих реклам по CTR
        top_ads = sorted(
            [ad for ad in ads if ad.impressions_count > 0],
            key=lambda x: x.clicks_count / x.impressions_count,
            reverse=True,
        )[:5]

        stats["top_performing"] = [
            {
                "id": ad.id,
                "title": ad.title,
                "ctr": round((ad.clicks_count / ad.impressions_count * 100), 2),
                "impressions": ad.impressions_count,
                "clicks": ad.clicks_count,
            }
            for ad in top_ads
        ]

        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
