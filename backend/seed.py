import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app
from database import IDatabaseConnection
from models import *
from models.author import author_followers
from repositories.subscription import SubscriptionRepository
from repositories.admin import AdminRepository
from repositories.user import UserRepository
from repositories.category import CategoryRepository
from repositories.author import AuthorRepository
from repositories.article import ArticleRepository
from repositories.comment import CommentRepository
from repositories.ad import AdRepository
from sqlalchemy.orm import Session
import random

load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG") or "default")


def clear_data(session: Session):
    """Видаляє всі дані з таблиць у правильному порядку."""
    print("Очищення бази даних...")
    session.execute(author_followers.delete())
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


def random_email(prefix="user"):
    """Генерує випадкову email адресу."""
    return f"{prefix}{random.randint(1000, 999999)}@news.com"


def random_username(base="User"):
    """Генерує випадкове імʼя користувача."""
    return f"{base}_{random.randint(100, 99999)}"


def random_name():
    """Генерує випадкове ім'я."""
    first_names = [
        "Олена",
        "Сергій",
        "Максим",
        "Юлія",
        "Ірина",
        "Павло",
        "Андрій",
        "Катерина",
        "Софія",
        "Денис",
        "Вадим",
        "Марина",
        "Ігор",
        "Владислав",
        "Гордій",
        "Ростислав",
        "Дарія",
        "Михайло",
        "Анна",
        "Іван",
        "Марія",
        "Дмитро",
        "Олга",
        "Віктор",
        "Ліза",
        "Роман",
        "Наталія",
        "Костянтин",
        "Ірина",
        "Павло",
        "Юлія",
        "Денис",
        "Анастасія",
        "Євген",
    ]

    last_names = [
        "Петренко",
        "Коваленко",
        "Ковальчук",
        "Іванова",
        "Шевченко",
        "Сидоренко",
        "Захарчук",
        "Бондаренко",
        "Мельник",
        "Литвин",
        "Марченко",
        "Гончаренко",
        "Іванець",
        "Кравченко",
        "Остапенко",
        "Сокур",
        "Забара",
        "Чорна",
        "Білий",
        "Смик",
        "Гринь",
        "Павлів",
        "Тарас",
        "Волощук",
        "Лютий",
        "Кучер",
    ]

    return random.choice(first_names), random.choice(last_names)


def random_text(length=100, max_length=300):
    """Генерує випадковий текст."""
    texts = [
        "Це дуже цікава стаття! Дякую за аналіз.",
        "Абсолютно згоден. Це змінить ситуацію.",
        "Не погоджуюся з цією точкою зору.",
        "Браво! Найкраще пояснення що я бачив.",
        "Потребуємо більше статей про цю тему.",
        "Це правда? Розслідження потрібне!",
        "Цей матеріал має вірусніти!",
        "Реально корисна інформація для мене.",
        "Чекаю продовження цієї теми.",
        "Мої друзі мають прочитати це!",
        "Як це було написано? Геніально!",
        "Потребуємо більше таких авторів.",
        "Це змінило мою думку про цьому.",
        "Геніальне пояснення складних речей.",
        "Мені подобається цей стиль написання.",
    ]
    return random.choice(texts)


def random_article_title(category_name):
    """Генерує випадковий заголовок статті."""
    templates = {
        "politika": [
            "Нові політичні альянси у {topic}",
            "Як {topic} змінить політичний ландшафт?",
            "Експерти про {topic}: прогнози на рік",
            "Скандал у парламенті: {topic}",
            "{topic} впливає на курс гривні",
            "Дипломатичний крок: {topic}",
        ],
        "tehnologii": [
            "Революція ШІ: як {topic} змінює світ",
            "Новий гаджет {topic}: перший огляд",
            "Квантові комп'ютери та {topic}",
            "{topic} для звичайних людей",
            "Стартап про {topic} залучив мільйони",
            "Кібербезпека та {topic}: нові загрози",
        ],
        "sport": [
            "Чемпіонат з {topic}: неймовірні результати",
            "Новий чемпіон у {topic}",
            "{topic}: як тренуватися як професіонал?",
            "Скандал у {topic}: що сталось?",
            "Молода зірка {topic} покорює світ",
            "Олімпіада 2028: {topic} у фокусі",
        ],
        "ekonomika": [
            "Економічний прогноз: роль {topic}",
            "Як {topic} впливає на ринок?",
            "Бізнес-тренди 2025: {topic}",
            "Інвестиції у {topic}: перспективи",
            "{topic} та інфляція: зв'язок",
            "Стартапи у {topic} змінюють індустрію",
        ],
        "kultura": [
            "Виставка про {topic}: мистецтво чи маркетинг?",
            "Як {topic} впливає на культуру?",
            "Новий фільм про {topic}",
            "Мистецтво та {topic}: синтез",
            "Театр переосмислює {topic}",
            "Музика та {topic}: історія",
        ],
        "podorozhi": [
            "Подорож до {topic}: перший раз?",
            "Топ-5 місць у {topic}",
            "Як дешево подорожувати до {topic}?",
            "Приховані дворики {topic}",
            "{topic}: місто чи село?",
            "Мандрівка по {topic} за тиждень",
        ],
        "zdorovya": [
            "Здоров'я та {topic}: що треба знати?",
            "Новий метод лікування {topic}",
            "Психічне здоров'я: {topic}",
            "Вправи для {topic}: експертні ради",
            "Харчування при {topic}",
            "Як запобігти {topic}?",
        ],
        "nauka": [
            "Наукові відкриття у {topic}",
            "Як {topic} змінює нашу розуміння світу?",
            "Дослідження про {topic} шокували вчених",
            "Майбутнє науки: {topic}",
            "Експеримент з {topic}: результати",
            "Нобелівська премія за {topic}",
        ],
    }

    topics = {
        "politika": ["санкції", "вибори", "дипломатія", "реформи", "альянси", "угоди"],
        "tehnologii": ["ШІ", "блокчейн", "квантові", "5G", "AR", "роботи"],
        "sport": ["футбол", "теніс", "велоспорт", "хокей", "плавання", "гімнастика"],
        "ekonomika": [
            "крипто",
            "акції",
            "нерухомість",
            "стартапи",
            "інвестиції",
            "банки",
        ],
        "kultura": ["театр", "кіно", "музика", "мистецтво", "танець", "література"],
        "podorozhi": ["Карпати", "Львів", "Балі", "Венеція", "Португалія", "Мальдіви"],
        "zdorovya": ["вакцини", "фітнес", "медитація", "сон", "харчування", "стрес"],
        "nauka": ["CRISPR", "Марс", "чорні дири", "climat", "ДНК", "енергія"],
    }

    template = random.choice(templates.get(category_name, templates["nauka"]))
    topic = random.choice(topics.get(category_name, topics["nauka"]))

    return template.format(topic=topic)


def random_article_content():
    """Генерує випадковий вміст статті."""
    intro = random.choice(
        [
            "Новітні дослідження показують",
            "Експерти передбачають",
            "На думку аналітиків,",
            "Останні дані свідчать про",
            "Проведене дослідження виявило",
        ]
    )

    body = random.choice(
        [
            "що ця тема набирає неймовірної популярності.",
            "значні зміни у цій індустрії.",
            "революційні підходи до розв'язання проблеми.",
            "глибокі зміни у суспільстві.",
            "новий рівень розвитку та інновацій.",
        ]
    )

    conclusion = random.choice(
        [
            "Очікуємо подальшого розвитку ситуації.",
            "Це змінить світ у найближчому майбутньому.",
            "Слід бути готовими до змін.",
            "Це дійсно історичний момент.",
            "Часи змінюються, і нам потрібно адаптуватися.",
        ]
    )

    return f"<h2>Аналіз ситуації</h2><p>{intro} {body}</p><p>{conclusion}</p>"


def seed_database():
    """Наповнює базу даних розширеними початковими даними з циклами."""
    with app.app_context():
        db_session = app.container.resolve(IDatabaseConnection).get_session()

        try:
            clear_data(db_session)

            sub_repo = SubscriptionRepository(db_session)
            admin_repo = AdminRepository(db_session)
            user_repo = UserRepository(db_session)
            category_repo = CategoryRepository(db_session)
            author_repo = AuthorRepository(db_session)
            article_repo = ArticleRepository(db_session)
            comment_repo = CommentRepository(db_session)
            ad_repo = AdRepository(db_session)

            # ============================================================
            # 1. ПЛАНИ ПІДПИСОК
            # ============================================================
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
            student_plan = sub_repo.create(
                {
                    "name": "Студентський",
                    "permissions": {
                        "no_ads": False,
                        "exclusive_content": True,
                        "save_article": True,
                        "comment": True,
                    },
                    "price_per_month": 4.99,
                    "description": "Доступ до ексклюзивних статей за спеціальною ціною для студентів (з рекламою).",
                }
            )
            corporate_plan = sub_repo.create(
                {
                    "name": "Корпоративний",
                    "permissions": {
                        "no_ads": True,
                        "exclusive_content": True,
                        "save_article": True,
                        "comment": True,
                    },
                    "price_per_month": 7.99,
                    "description": "Повний доступ для вашої команди.",
                }
            )
            plans = [free_plan, premium_plan, student_plan, corporate_plan]
            print("✓ Плани підписок створено.")

            # ============================================================
            # 2. АДМІНІСТРАТОР
            # ============================================================
            print("Створення адміністратора...")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@news.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin")
            admin_repo.create(
                {
                    "email": admin_email,
                    "password": generate_password_hash(admin_password),
                }
            )
            print(f"✓ Адміністратор: {admin_email} / {admin_password}")

            # ============================================================
            # 3. КАТЕГОРІЇ
            # ============================================================
            print("Створення категорій...")
            categories = {
                "politika": category_repo.create(
                    {
                        "name": "Політика",
                        "description": "Новини та аналітика політичного життя.",
                        "slug": "politika",
                    }
                ),
                "tehnologii": category_repo.create(
                    {
                        "name": "Технології",
                        "description": "Огляди гаджетів та новини IT.",
                        "slug": "tehnologii",
                    }
                ),
                "sport": category_repo.create(
                    {
                        "name": "Спорт",
                        "description": "Найважливіші спортивні події.",
                        "slug": "sport",
                    }
                ),
                "ekonomika": category_repo.create(
                    {
                        "name": "Економіка",
                        "description": "Все про фінанси та бізнес.",
                        "slug": "ekonomika",
                    }
                ),
                "kultura": category_repo.create(
                    {
                        "name": "Культура",
                        "description": "Мистецтво, кіно та музика.",
                        "slug": "kultura",
                    }
                ),
                "podorozhi": category_repo.create(
                    {
                        "name": "Подорожі",
                        "description": "Ідеї для ваших майбутніх мандрівок.",
                        "slug": "podorozhi",
                    }
                ),
                "zdorovya": category_repo.create(
                    {
                        "name": "Здоров'я",
                        "description": "Медичні новини та поради.",
                        "slug": "zdorovya",
                    }
                ),
                "nauka": category_repo.create(
                    {
                        "name": "Наука",
                        "description": "Наукові дослідження та відкриття.",
                        "slug": "nauka",
                    }
                ),
            }
            print(f"✓ Категорій створено: {len(categories)}")

            # ============================================================
            # 4. КОРИСТУВАЧИ (100+ користувачів в циклі)
            # ============================================================
            print("Створення користувачів (ЦИКЛ - 150 користувачів)...")
            generic_user_password = os.getenv("GENERIC_USER_PASSWORD", "user-password")
            hashed_user_password = generate_password_hash(generic_user_password)

            users = {}
            for i in range(150):
                user = user_repo.create(
                    {
                        "email": random_email(f"user{i}"),
                        "username": random_username(f"User"),
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": random.sample(
                                list(categories.keys()), k=random.randint(1, 3)
                            )
                        },
                    }
                )
                users[f"user_{i}"] = user
                if (i + 1) % 30 == 0:
                    print(f"  └─ Користувачів створено: {i + 1}/150")

            print(f"✓ Користувачів створено: {len(users)}")

            # ============================================================
            # 5. ПІДПИСКИ КОРИСТУВАЧІВ
            # ============================================================
            print("Призначення підписок користувачам (ЦИКЛ)...")
            for key, user in users.items():
                plan = random.choice(plans)
                sub_repo.subscribe_user(user_id=user.id, plan_id=plan.id)
            print("✓ Підписки призначено.")

            # ============================================================
            # 6. АВТОРИ (50+ авторів в циклі)
            # ============================================================
            print("Створення авторів (ЦИКЛ - 60 авторів)...")
            authors = {}
            for i in range(60):
                first_name, last_name = random_name()
                author = author_repo.create(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "bio": f"Спеціаліст з досвідом більше 10 років у своїй галузі. Автор {random.randint(20, 200)} статей.",
                    }
                )
                authors[f"author_{i}"] = author
                if (i + 1) % 20 == 0:
                    print(f"  └─ Авторів створено: {i + 1}/60")

            print(f"✓ Авторів створено: {len(authors)}")

            # ============================================================
            # 7. СТАТТІ (500+ статей в циклі)
            # ============================================================
            print("Створення статей (ЦИКЛ - 1000 статей)...")
            articles = []
            article_count = 0

            for category_slug, category_obj in categories.items():
                for i in range(int(1000 / len(categories))):  # ~62 статей на категорію
                    article = article_repo.create(
                        {
                            "author_id": random.choice(list(authors.values())).id,
                            "category_id": category_obj.id,
                            "title": random_article_title(category_slug),
                            "content": random_article_content(),
                            "status": random.choice(
                                ["published", "published", "draft"]
                            ),  # більше 66% опублікованих
                            "is_breaking": random.choice(
                                [True, False, False, False]
                            ),  # 25% breaking news
                            "is_exclusive": random.choice(
                                [True, False, False]
                            ),  # 33% ексклюзивних
                            "views_count": random.randint(100, 3000),
                        }
                    )
                    articles.append(article)
                    article_count += 1

                    if article_count % 100 == 0:
                        print(f"  └─ Статей створено: {article_count}/500")

            print(f"✓ Статей створено: {len(articles)}")

            # ============================================================
            # 8. ЛАЙКИ І ЗБЕРЕЖЕННЯ (1000+ взаємодій в циклі)
            # ============================================================
            print("Створення взаємодій (ЦИКЛ - лайки та збереження)...")
            interactions_to_add = []

            for user_key, user in list(users.items()):
                # Кожен користувач взаємодіє з 10-20 статтями
                random_articles = random.sample(
                    articles, k=min(random.randint(10, 30), len(articles))
                )

                for article in random_articles:
                    interaction_type = random.choice(["like", "like", "like", "saved"])
                    interactions_to_add.append(
                        ArticleInteraction(
                            user_id=user.id,
                            article_id=article.id,
                            interaction_type=interaction_type,
                        )
                    )

                if len(interactions_to_add) % 500 == 0:
                    print(f"  └─ Взаємодій додано: {len(interactions_to_add)}")
            db_session.add_all(interactions_to_add)
            print(f"✓ Взаємодій створено: {len(interactions_to_add)}")

            # ============================================================
            # 9. КОМЕНТАРІ (1000+ коментарів в циклі)
            # ============================================================
            print("Створення коментарів (ЦИКЛ - 1000+ коментарів)...")
            comments_count = 0

            # Кожна стаття отримує 1-3 коментарі
            for article in articles:
                num_comments = random.randint(1, 5)

                for _ in range(num_comments):
                    random_user = random.choice(list(users.values()))
                    comment_repo.create(
                        {
                            "article_id": article.id,
                            "user_id": random_user.id,
                            "text": random_text(),
                        }
                    )
                    comments_count += 1

                if comments_count % 200 == 0:
                    print(f"  └─ Коментарів створено: {comments_count}")

            print(f"✓ Коментарів створено: {comments_count}")

            # ============================================================
            # 10. РЕКЛАМНІ ОГОЛОШЕННЯ (МІНІМУМ - тільки 8 реклам)
            # ============================================================
            print("Створення рекламних оголошень (МІНІМУМ)...")
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

            for ad_title in ad_titles:
                ad_repo.create(
                    {
                        "title": ad_title,
                        "content": f"Реклама '{ad_title}'. Дізнайтеся більше!",
                        "ad_type": random.choice(["banner", "sidebar", "video"]),
                        "is_active": True,
                        "impressions_count": random.randint(5000, 30000),
                        "clicks_count": random.randint(100, 2000),
                    }
                )

            print(f"✓ Рекламних оголошень створено: {len(ad_titles)}")

            # ============================================================
            # ФІКСАЦІЯ ВСІХ ЗМІН
            # ============================================================
            db_session.commit()

            print("\n" + "=" * 60)
            print("✅ УСІ ДАНІ УСПІШНО СТВОРЕНО И ЗБЕРЕЖЕНО!")
            print("=" * 60)
            print(f"\n📊 ФІНАЛЬНА СТАТИСТИКА:")
            print(f"   • Користувачів: {len(users)}")
            print(f"   • Авторів: {len(authors)}")
            print(f"   • Статей: {len(articles)}")
            print(f"   • Категорій: {len(categories)}")
            print(f"   • Коментарів: {comments_count}")
            print(f"   • Взаємодій (лайки/збереження): {len(interactions_to_add)}")
            print(f"   • Рекламних оголошень: {len(ad_titles)}")
            print("\n" + "=" * 60)

        except Exception as e:
            print(f"\n❌ СТАЛАСЯ ПОМИЛКА: {e}")
            import traceback

            traceback.print_exc()
            db_session.rollback()
        finally:
            db_session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  ЗАПУСК РОЗШИРЕНОГО SEED-СКРИПТУ З ЦИКЛАМИ")
    print("=" * 60)
    seed_database()
    print("\n" + "=" * 60)
    print("  БА ЗА ДАНИХ ГОТОВА ДО ВИКОРИСТАННЯ")
    print("=" * 60)
