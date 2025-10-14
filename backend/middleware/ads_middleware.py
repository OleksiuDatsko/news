from functools import wraps
from repositories import get_ad_repo
from services.ad_service import AdService


def ads_injector(ad_type: str = None, limit=3, strategy="default"):
    """
    Декоратор, що інжектить рекламу обраного типу в параметри функції-обробника.
    ["banner", "sidebar", "popup", "inline", "video"]
    """

    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            user_permissions = {}
            if current_user:
                user_permissions = current_user.permissions
            ad_repo = get_ad_repo()
            ad_service = AdService(ad_repo)

            ads = []
            if ad_type is not None:
                if ad_service.should_show_ads(user_permissions):
                    ads = ad_service.get_ads_for_user(
                        ad_type=ad_type,
                        user_permissions=user_permissions,
                        limit=limit,
                        strategy=strategy,
                    )
                    ads = [ad.to_dict() for ad in ads]

            return f(current_user, ads, *args, **kwargs)

        return wrapper

    return decorator
