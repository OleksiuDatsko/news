import os
import random
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from faker import Faker
from sqlalchemy.orm import Session
from app import create_app
from database import IDatabaseConnection
from models import *
from models.author import author_followers

fake = Faker("uk_UA")

load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG") or "default")


def clear_data(session: Session):
    """Видаляє всі дані з таблиць у правильному порядку."""
    print("Очищення бази даних...")
    session.query(author_followers).delete(synchronize_session=False)
    session.query(ArticleInteraction).delete(synchronize_session=False)
    session.query(Comment).delete(synchronize_session=False)
    session.query(ArticleView).delete(synchronize_session=False)
    session.query(AdView).delete(synchronize_session=False)
    session.query(UserSubscriptionPlan).delete(synchronize_session=False)
    session.query(Notification).delete(synchronize_session=False)
    session.query(NewsletterSubscription).delete(synchronize_session=False)
    session.query(Article).delete(synchronize_session=False)
    session.query(Ad).delete(synchronize_session=False)
    session.query(Author).delete(synchronize_session=False)
    session.query(Category).delete(synchronize_session=False)
    session.query(User).delete(synchronize_session=False)
    session.query(Admin).delete(synchronize_session=False)
    session.query(SubscriptionPlan).delete(synchronize_session=False)
    session.commit()
    print("Базу даних очищено.")


def get_random_content():
    """Генерує випадковий HTML-вміст статті."""
    title = fake.sentence(nb_words=random.randint(4, 8))
    p1 = fake.paragraph(nb_sentences=random.randint(5, 10))
    p2 = fake.paragraph(nb_sentences=random.randint(6, 12))
    return f"<h2>{title}</h2><p>{p1}</p><p>{p2}</p>"


def seed_plans(session: Session) -> list[SubscriptionPlan]:
    """Створює плани підписок."""
    print("Створення планів підписок...")
    plans_data = [
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
        },
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
        },
        {
            "name": "Студентський",
            "permissions": {
                "no_ads": False,
                "exclusive_content": True,
                "save_article": True,
                "comment": True,
            },
            "price_per_month": 4.99,
            "description": "Доступ до ексклюзивних статей за спеціальною ціною.",
        },
    ]

    plans = [SubscriptionPlan(**data) for data in plans_data]
    session.add_all(plans)
    session.commit()
    print("✓ Плани підписок створено.")
    return plans


def seed_admin(session: Session):
    """Створює головного адміністратора."""
    print("Створення адміністратора...")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@news.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin")
    admin = Admin(email=admin_email, password=generate_password_hash(admin_password))
    session.add(admin)
    session.commit()
    print(f"✓ Адміністратор: {admin_email} / {admin_password}")


def seed_categories(session: Session) -> list[Category]:
    """Створює категорії новин."""
    print("Створення категорій...")
    categories_data = [
        {
            "name": "Політика",
            "description": "Новини та аналітика політичного життя.",
            "slug": "politika",
        },
        {
            "name": "Технології",
            "description": "Огляди гаджетів та новини IT.",
            "slug": "tehnologii",
        },
        {
            "name": "Спорт",
            "description": "Найважливіші спортивні події.",
            "slug": "sport",
        },
        {
            "name": "Економіка",
            "description": "Все про фінанси та бізнес.",
            "slug": "ekonomika",
        },
        {
            "name": "Культура",
            "description": "Мистецтво, кіно та музика.",
            "slug": "kultura",
        },
        {
            "name": "Подорожі",
            "description": "Ідеї для ваших майбутніх мандрівок.",
            "slug": "podorozhi",
        },
        {
            "name": "Здоров'я",
            "description": "Медичні новини та поради.",
            "slug": "zdorovya",
        },
        {
            "name": "Наука",
            "description": "Наукові дослідження та відкриття.",
            "slug": "nauka",
        },
    ]

    categories = [Category(**data) for data in categories_data]
    session.add_all(categories)
    session.commit()
    print(f"✓ Категорій створено: {len(categories)}")
    return categories


def seed_users(session: Session, plans: list[SubscriptionPlan]) -> list[User]:
    """Створює 150 користувачів і призначає їм плани."""
    print("Створення 150 користувачів...")
    generic_password = os.getenv("GENERIC_USER_PASSWORD", "user-password")
    hashed_password = generate_password_hash(generic_password)

    users_to_add = []
    subscriptions_to_add = []

    for i in range(150):
        user = User(
            email=fake.email(),
            username=fake.user_name() + str(i),
            password=hashed_password,
            preferences={
                "favorite_categories": [
                    random.choice(
                        app.config.get("CATEGORIES_LIST", ["politika", "sport"])
                    )
                ]
            },
        )
        users_to_add.append(user)

    session.add_all(users_to_add)
    session.commit()

    print("✓ Користувачів створено. Призначення підписок...")
    for user in users_to_add:
        plan = random.choice(plans)
        sub = UserSubscriptionPlan(user_id=user.id, plan_id=plan.id, is_active=True)
        subscriptions_to_add.append(sub)

    session.add_all(subscriptions_to_add)
    session.commit()

    print(f"✓ Користувачів створено: {len(users_to_add)}")
    return users_to_add


def seed_authors(session: Session) -> list[Author]:
    """Створює 60 авторів."""
    print("Створення 60 авторів...")
    authors_to_add = []
    for _ in range(60):
        author = Author(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            bio=fake.sentence(nb_words=random.randint(10, 20)),
        )
        authors_to_add.append(author)

    session.add_all(authors_to_add)
    session.commit()
    print(f"✓ Авторів створено: {len(authors_to_add)}")
    return authors_to_add


def seed_articles(
    session: Session, authors: list[Author], categories: list[Category]
) -> list[Article]:
    """Створює 1000 статей."""
    print("Створення 1000 статей...")
    articles_to_add = []
    for i in range(10000):
        article = Article(
            author_id=random.choice(authors).id,
            category_id=random.choice(categories).id,
            title=fake.sentence(nb_words=random.randint(5, 12)),
            content=get_random_content(),
            status=random.choice(["published", "published", "draft"]),
            is_breaking=random.choice([True, False, False, False]),
            is_exclusive=random.choice([True, False, False]),
            views_count=random.randint(10, 150),
        )
        articles_to_add.append(article)
        if (i + 1) % 100 == 0:
            print(f"  └─ Підготовлено статей: {i + 1}/1000")

    session.add_all(articles_to_add)
    session.commit()
    print(f"✓ Статей створено: {len(articles_to_add)}")
    return articles_to_add


def seed_interactions(session: Session, users: list[User], articles: list[Article]):
    """Створює лайки та збереження для статей."""
    print("Створення взаємодій (лайки/збереження)...")
    interactions_to_add = []

    for user in users:
        num_interactions = min(random.randint(10, 100), len(articles))
        random_articles = random.sample(articles, k=num_interactions)

        for article in random_articles:
            interaction_type = random.choice(["like", "like", "like", "saved"])
            interaction = ArticleInteraction(
                user_id=user.id,
                article_id=article.id,
                interaction_type=interaction_type,
            )
            interactions_to_add.append(interaction)

    session.add_all(interactions_to_add)
    session.commit()
    print(f"✓ Взаємодій створено: {len(interactions_to_add)}")


def seed_comments(session: Session, users: list[User], articles: list[Article]):
    """Створює коментарі до статей."""
    print("Створення коментарів...")
    comments_to_add = []

    for article in articles:
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
            comment = Comment(
                article_id=article.id,
                user_id=random.choice(users).id,
                text=fake.sentence(nb_words=random.randint(5, 20)),
            )
            comments_to_add.append(comment)

    session.add_all(comments_to_add)
    session.commit()
    print(f"✓ Коментарів створено: {len(comments_to_add)}")


def seed_ads(session: Session):
    """Створює рекламні оголошення."""
    print("Створення рекламних оголошень...")
    ad_titles = [
        "Курс з Python",
        "Онлайн-кінотеатр",
        "Квитки на концерт",
        "Курси англійської",
        "Подорож до Єгипту",
        "Новий смартфон",
        "Фітнес-клуб",
        "Вебінар з маркетингу",
    ]
    ads_to_add = []
    for title in ad_titles:
        ad = Ad(
            title=title,
            content=f"Реклама '{title}'. {fake.sentence(nb_words=3)}",
            ad_type=random.choice(["banner", "sidebar", "video"]),
            is_active=True,
            impressions_count=random.randint(5000, 30000),
            clicks_count=random.randint(100, 2000),
        )
        ads_to_add.append(ad)

    session.add_all(ads_to_add)
    session.commit()
    print(f"✓ Рекламних оголошень створено: {len(ads_to_add)}")


def seed_database():
    """Наповнює базу даних початковими даними."""
    with app.app_context():
        db_session = app.container.resolve(IDatabaseConnection).get_session()
        try:
            clear_data(db_session)

            plans = seed_plans(db_session)
            seed_admin(db_session)
            categories = seed_categories(db_session)
            users = seed_users(db_session, plans)
            authors = seed_authors(db_session)
            articles = seed_articles(db_session, authors, categories)
            seed_interactions(db_session, users, articles)
            seed_comments(db_session, users, articles)
            seed_ads(db_session)

            print("\n" + "=" * 60)
            print("✅ УСІ ДАНІ УСПІШНО СТВОРЕНО!")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ СТАЛАСЯ ПОМИЛКА: {e}")
            import traceback

            traceback.print_exc()
            db_session.rollback()
        finally:
            db_session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  ЗАПУСК РОЗШИРЕНОГО SEED-СКРИПТУ")
    print("=" * 60)
    seed_database()
    print("\n" + "=" * 60)
    print("  БАЗА ДАНИХ ГОТОВА ДО ВИКОРИСТАННЯ")
    print("=" * 60)
