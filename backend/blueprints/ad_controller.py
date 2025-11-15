from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_optional
from repositories import get_ad_repo, get_ad_view_repo
from services.ad_service import AdService

ad_bp = Blueprint("ad_public", __name__)


@ad_bp.route("/", methods=["GET"])
@token_optional
def get_ads(current_user):
    ad_type = request.args.get("type")
    limit = request.args.get("limit", 5, type=int)
    strategy = request.args.get("strategy", "default")

    ad_repo = get_ad_repo()
    ad_service = AdService(ad_repo)

    user_permissions = current_user.permissions if current_user else {}

    ads = ad_service.get_ads_for_user(
        ad_type=ad_type,
        user_permissions=user_permissions,
        limit=limit,
        strategy=strategy,
    )

    result = [ad.to_dict() for ad in ads]
    return (
        jsonify(
            {
                "ads": result,
                "show_ads": ad_service.should_show_ads(user_permissions),
            }
        ),
        200,
    )


@ad_bp.route("/<int:ad_id>", methods=["GET"])
@token_optional
def get_ad_by_id(current_user, ad_id):
    ad_repo = get_ad_repo()
    ad_service = AdService(ad_repo)

    user_permissions = current_user.permissions if current_user else {}
    ad = ad_repo.get_by(id=ad_id)

    if not ad:
        raise ValueError(f"Рекламне оголошення з ID {ad_id} не знайдено")

    return (
        jsonify(
            {
                "ad": ad.to_dict(),
                "show_ads": ad_service.should_show_ads(user_permissions),
            }
        ),
        200,
    )


@ad_bp.route("/by-placement", methods=["GET"])
@token_optional
def get_ads_by_placement(current_user):
    ad_repo = get_ad_repo()
    ad_service = AdService(ad_repo)

    user_permissions = current_user.permissions if current_user else {}

    requested = request.args.get("placement")
    strategy = request.args.get("strategy", "default")
    if requested:
        placements = [p.strip() for p in requested.split(",") if p.strip()]
        allowed = {"banner", "sidebar", "popup", "inline", "video"}
        placements = [p for p in placements if p in allowed]
        if not placements:
            placements = list(allowed)
    else:
        placements = ["banner", "sidebar", "popup", "inline", "video"]

    ads = ad_service.get_ads_by_placement(
        user_permissions=user_permissions,
        placements=placements,
        strategy=strategy,
    )

    result = {
        placement: [ad.to_dict() for ad in ads_list]
        for placement, ads_list in ads.items()
    }

    return (
        jsonify(
            {
                "placements": result,
                "show_ads": ad_service.should_show_ads(user_permissions),
            }
        ),
        200,
    )


@ad_bp.route("/<int:ad_id>/impression", methods=["POST"])
@token_optional
def record_impression(current_user, ad_id):
    data = request.get_json() or {}

    ad_repo = get_ad_repo()
    ad_service = AdService(ad_repo)

    success = ad_service.record_impression(
        ad_id=ad_id,
        user_id=current_user.id if current_user else None,
        session_id=data.get("session_id"),
        ip_address=request.remote_addr,
    )

    if success:
        return jsonify({"msg": "Показ зареєстровано"}), 200
    else:
        return jsonify({"msg": "Помилка при реєстрації показу"}), 500


@ad_bp.route("/<int:ad_id>/click", methods=["GET"])
def record_click(ad_id):
    ad_repo = get_ad_repo()
    ad_service = AdService(ad_repo)

    success = ad_service.record_click(ad_id)

    if success:
        return jsonify({"msg": "Клік зареєстровано"}), 200
    else:
        return jsonify({"msg": "Помилка при реєстрації кліку"}), 500
