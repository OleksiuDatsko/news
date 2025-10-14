import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app
from database import IDatabaseConnection
from models import *

from repositories.subscription import SubscriptionRepository
from repositories.admin import AdminRepository
from repositories.user import UserRepository
from repositories.category import CategoryRepository
from repositories.author import AuthorRepository
from repositories.article import ArticleRepository
from repositories.comment import CommentRepository
from repositories.ad import AdRepository
from sqlalchemy.orm import Session

load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG") or "default")


def clear_data(session: Session):
    """Видаляє всі дані з таблиць у правильному порядку."""
    print("Очищення бази даних...")
    session.query(ArticleInteraction).delete()
    session.query(Comment).delete()
    session.query(ArticleView).delete()
    session.query(AdView).delete()
    session.query(UserSubscriptionPlan).delete()
    session.query(Notification).delete()
    session.query(NewsletterSubscription).delete()

    session.query(Article).delete()
    session.query(Ad).delete()
    session.query(Author).delete()
    session.query(Category).delete()
    session.query(User).delete()
    session.query(Admin).delete()
    session.query(SubscriptionPlan).delete()

    session.commit()
    print("Базу даних очищено.")


def seed_database():
    """Наповнює базу даних початковими даними."""
    with app.app_context():
        db_session = app.container.resolve(IDatabaseConnection).get_session()

        clear_data(db_session)

        sub_repo = SubscriptionRepository(db_session)
        admin_repo = AdminRepository(db_session)
        user_repo = UserRepository(db_session)
        category_repo = CategoryRepository(db_session)
        author_repo = AuthorRepository(db_session)
        article_repo = ArticleRepository(db_session)
        comment_repo = CommentRepository(db_session)
        ad_repo = AdRepository(db_session)

        print("Створення планів підписок...")
        free_plan = sub_repo.create(
            {
                "name": "Безкоштовний",
                "permissions": {
                    "no_ads": False,
                    "exclusive_content": False,
                    "save_article": False,
                    "comment": True,
                },
                "price_per_month": 0.0,
                "description": "Доступ до публічних статей з рекламою.",
            }
        )
        premium_plan = sub_repo.create(
            {
                "name": "Преміум",
                "permissions": {
                    "no_ads": True,
                    "exclusive_content": True,
                    "save_article": True,
                    "comment": True,
                },
                "price_per_month": 9.99,
                "description": "Повний доступ до всього контенту без реклами.",
            }
        )
        print("Плани підписок створено.")

        # --- 2. Створення адміністратора ---
        print("Створення адміністратора...")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@news.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin")
        hashed_password = generate_password_hash(admin_password)
        admin_repo.create(
            {
                "email": admin_email,
                "password": hashed_password,
            }
        )
        print(
            f"Адміністратора створено (email: {admin_email}, пароль: {admin_password})."
        )

        # --- 3. Створення користувачів ---
        print("Створення користувачів...")
        generic_user_password = os.getenv("GENERIC_USER_PASSWORD", "user-password")
        hashed_user_password = generate_password_hash(generic_user_password)
        

        premium_user = user_repo.create(
            {
                "email": "premium@news.com",
                "username": "PremiumUser",
                "password": hashed_user_password,
            }
        )
        free_user = user_repo.create(
            {
                "email": "free@news.com",
                "username": "FreeUser",
                "password": hashed_user_password,
            }
        )
        print("Користувачів створено.")
        print(f"\tПароль для користувачів: {generic_user_password}\n\tEmails: free@news.com, premium@news.com")

        # --- 4. Призначення підписок ---
        sub_repo.subscribe_user(user_id=premium_user.id, plan_id=premium_plan.id)
        sub_repo.subscribe_user(user_id=free_user.id, plan_id=free_plan.id)
        print("Підписки призначено.")

        # --- 5. Створення категорій та авторів ---
        print("Створення категорій та авторів...")
        cat_politics = category_repo.create(
            {
                "name": "Політика",
                "description": "Новини та аналітика політичного життя.",
            }
        )
        cat_tech = category_repo.create(
            {"name": "Технології", "description": "Огляди гаджетів та новини IT."}
        )
        cat_sport = category_repo.create(
            {"name": "Спорт", "description": "Найважливіші спортивні події."}
        )
        cat_economy = category_repo.create(
            {"name": "Економіка", "description": "Все про фінанси та бізнес."}
        )
        cat_culture = category_repo.create(
            {"name": "Культура", "description": "Мистецтво, кіно та музика."}
        )
        cat_travel = category_repo.create(
            {"name": "Подорожі", "description": "Ідеї для ваших майбутніх мандрівок."}
        )

        author1 = author_repo.create(
            {
                "first_name": "Олена",
                "last_name": "Петренко",
                "bio": "Головний політичний оглядач.",
            }
        )
        author2 = author_repo.create(
            {
                "first_name": "Максим",
                "last_name": "Ковальчук",
                "bio": "Експерт з ринкових технологій.",
            }
        )
        author3 = author_repo.create(
            {
                "first_name": "Ірина",
                "last_name": "Шевченко",
                "bio": "Спортивний журналіст.",
            }
        )
        author4 = author_repo.create(
            {
                "first_name": "Андрій",
                "last_name": "Захарчук",
                "bio": "Фінансовий аналітик.",
            }
        )
        author5 = author_repo.create(
            {
                "first_name": "Софія",
                "last_name": "Мельник",
                "bio": "Мистецтвознавець та тревел-блогер.",
            }
        )
        print("Категорії та автори створені.")

        # --- 6. Створення статей ---
        print("Створення статей...")
        article1 = article_repo.create(
            {
                "author_id": author1.id,
                "category_id": cat_politics.id,
                "title": "Нові політичні альянси",
                "content": "Детальний аналіз останніх подій...",
                "status": "published",
                "is_breaking": True,
                "views_count": 1520,
            }
        )
        article2 = article_repo.create(
            {
                "author_id": author2.id,
                "category_id": cat_tech.id,
                "title": "Майбутнє ШІ: ексклюзив",
                "content": "Ця стаття доступна лише для преміум-підписників.",
                "status": "published",
                "is_exclusive": True,
                "views_count": 2800,
            }
        )
        article3 = article_repo.create(
            {
                "author_id": author3.id,
                "category_id": cat_sport.id,
                "title": "Історична перемога у футболі",
                "content": "Емоційний репортаж з вирішального матчу.",
                "status": "published",
                "views_count": 3150,
            }
        )
        article4 = article_repo.create(
            {
                "author_id": author4.id,
                "category_id": cat_economy.id,
                "title": "Економічний прогноз на наступний квартал",
                "content": "Аналітики прогнозують зростання ВВП, але є ризики...",
                "status": "published",
                "views_count": 980,
            }
        )
        article5 = article_repo.create(
            {
                "author_id": author5.id,
                "category_id": cat_culture.id,
                "title": "Цифрове мистецтво: як NFT змінює світ",
                "content": "Пояснюємо, що таке NFT і чому це важливо.",
                "status": "draft",
                "is_exclusive": True,
                "views_count": 150,
            }
        )
        article6 = article_repo.create(
            {
                "author_id": author1.id,
                "category_id": cat_politics.id,
                "title": "Аналіз законопроєкту про медіа",
                "content": "Ключові зміни та можливі наслідки для свободи слова.",
                "status": "published",
                "views_count": 750,
            }
        )
        article7 = article_repo.create(
            {
                "author_id": author2.id,
                "category_id": cat_tech.id,
                "title": "Новий квантовий комп'ютер: прорив чи міф?",
                "content": "Розбираємось у складній технології та її перспективах.",
                "status": "published",
                "is_exclusive": True,
                "views_count": 1900,
            }
        )
        article8 = article_repo.create(
            {
                "author_id": author5.id,
                "category_id": cat_travel.id,
                "title": "Топ-5 недооцінених місць в Карпатах",
                "content": "Відкрийте для себе приховані перлини українських гір.",
                "status": "published",
                "views_count": 2200,
            }
        )
        article9 = article_repo.create(
            {
                "author_id": author4.id,
                "category_id": cat_economy.id,
                "title": "Вплив інфляції на малий бізнес",
                "content": "Як підприємцям адаптуватися до нових економічних реалій.",
                "status": "published",
                "views_count": 1100,
            }
        )
        article10 = article_repo.create(
            {
                "author_id": author3.id,
                "category_id": cat_sport.id,
                "title": "Огляд тенісного турніру: нові зірки",
                "content": "Аналіз виступів молодих талантів на міжнародній арені.",
                "status": "published",
                "views_count": 1350,
            }
        )
        print("Статті створено.")

        # --- 7. Створення коментарів ---
        print("Створення коментарів...")
        comment_repo.create(
            {
                "article_id": article1.id,
                "user_id": free_user.id,
                "text": "Дуже цікава стаття!",
            }
        )
        comment_repo.create(
            {
                "article_id": article1.id,
                "user_id": premium_user.id,
                "text": "Написано добре, але є питання.",
            }
        )
        comment_repo.create(
            {
                "article_id": article3.id,
                "user_id": premium_user.id,
                "text": "Це була неймовірна гра! Наші хлопці молодці!",
            }
        )
        comment_repo.create(
            {
                "article_id": article4.id,
                "user_id": free_user.id,
                "text": "Корисна інформація, дякую.",
            }
        )
        print("Коментарі створено.")

        # --- 8. Створення рекламних оголошень ---
        print("Створення рекламних оголошень...")
        ad_repo.create(
            {
                "title": "Знижки на техніку",
                "content": "Купуйте ноутбуки!",
                "ad_type": "banner",
                "is_active": True,
                "impressions_count": 5000,
                "clicks_count": 150,
            }
        )
        ad_repo.create(
            {
                "title": "Курс з програмування",
                "content": "Стань розробником!",
                "ad_type": "sidebar",
                "is_active": True,
                "impressions_count": 12000,
                "clicks_count": 250,
            }
        )
        ad_repo.create(
            {
                "title": "Доставка їжі",
                "content": "Смачна їжа тут!",
                "ad_type": "sidebar",
                "is_active": True,
                "impressions_count": 8000,
                "clicks_count": 180,
            }
        )
        ad_repo.create(
            {
                "title": "Нова колекція одягу",
                "content": "Стильні речі для вашого гардеробу.",
                "ad_type": "inline",
                "is_active": True,
                "impressions_count": 9500,
                "clicks_count": 210,
            }
        )
        ad_repo.create(
            {
                "title": "Онлайн-кінотеатр",
                "content": "Дивіться фільми у високій якості.",
                "ad_type": "video",
                "is_active": True,
                "impressions_count": 25000,
                "clicks_count": 1200,
            }
        )
        ad_repo.create(
            {
                "title": "Квитки на концерт",
                "content": "Не пропустіть виступ улюбленого гурту!",
                "ad_type": "popup",
                "is_active": True,
                "impressions_count": 3000,
                "clicks_count": 450,
            }
        )
        ad_repo.create(
            {
                "title": "Страхування авто",
                "content": "Надійний захист для вашого автомобіля.",
                "ad_type": "banner",
                "is_active": True,
                "impressions_count": 6000,
                "clicks_count": 90,
            }
        )
        ad_repo.create(
            {
                "title": "Курси англійської",
                "content": "Вивчай мову з носіями.",
                "ad_type": "sidebar",
                "is_active": True,
                "impressions_count": 11000,
                "clicks_count": 320,
            }
        )
        ad_repo.create(
            {
                "title": "Спортивне харчування",
                "content": "Все для ваших тренувань.",
                "ad_type": "inline",
                "is_active": True,
                "impressions_count": 7000,
                "clicks_count": 280,
            }
        )
        ad_repo.create(
            {
                "title": "Подорож до Єгипту",
                "content": "Гарячі тури за найкращими цінами!",
                "ad_type": "banner",
                "is_active": True,
                "impressions_count": 15000,
                "clicks_count": 600,
            }
        )
        ad_repo.create(
            {
                "title": "Новий смартфон",
                "content": "Оновіть свій гаджет сьогодні.",
                "ad_type": "video",
                "is_active": True,
                "impressions_count": 18000,
                "clicks_count": 950,
            }
        )
        ad_repo.create(
            {
                "title": "Юридичні послуги",
                "content": "Професійна консультація для вашого бізнесу.",
                "ad_type": "sidebar",
                "is_active": False,
                "impressions_count": 2000,
                "clicks_count": 15,
            }
        )
        ad_repo.create(
            {
                "title": "Фітнес-клуб",
                "content": "Абонемент на рік зі знижкою 50%!",
                "ad_type": "popup",
                "is_active": True,
                "impressions_count": 4500,
                "clicks_count": 700,
            }
        )
        ad_repo.create(
            {
                "title": "Ремонт квартир",
                "content": "Якісно та швидко.",
                "ad_type": "inline",
                "is_active": True,
                "impressions_count": 5500,
                "clicks_count": 110,
            }
        )

        print("Рекламні оголошення створено.")

        db_session.close()


if __name__ == "__main__":
    print("Запуск скрипту для наповнення бази даних...")
    seed_database()
    print("\nУспішно завершено! База даних готова до використання.")
