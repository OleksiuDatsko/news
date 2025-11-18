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


def seed_database():
    """Наповнює базу даних розширеними початковими даними."""
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
                    "description": "Повний доступ для вашої команди. Розрахунок за одного користувача.",
                }
            )
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
            # 3. КОРИСТУВАЧІ (РОЗШИРЕНО - 15 користувачів)
            # ============================================================
            print("Створення користувачів...")
            generic_user_password = os.getenv("GENERIC_USER_PASSWORD", "user-password")
            hashed_user_password = generate_password_hash(generic_user_password)

            users = {
                "premium": user_repo.create(
                    {
                        "email": "premium@news.com",
                        "username": "PremiumUser",
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": ["tehnologii", "ekonomika"]
                        },
                    }
                ),
                "free": user_repo.create(
                    {
                        "email": "free@news.com",
                        "username": "FreeUser",
                        "password": hashed_user_password,
                    }
                ),
                "tech": user_repo.create(
                    {
                        "email": "tech@news.com",
                        "username": "TechEnthusiast",
                        "password": hashed_user_password,
                        "preferences": {
                            "dailyDigest": True,
                            "breakingNews": True,
                            "favorite_categories": ["tehnologii", "ekonomika"],
                        },
                    }
                ),
                "politics": user_repo.create(
                    {
                        "email": "politics@news.com",
                        "username": "PoliticsReader",
                        "password": hashed_user_password,
                        "preferences": {
                            "dailyDigest": False,
                            "breakingNews": True,
                            "favorite_categories": ["politika"],
                        },
                    }
                ),
                "sports": user_repo.create(
                    {
                        "email": "sport@news.com",
                        "username": "SportsFan",
                        "password": hashed_user_password,
                        "preferences": {
                            "dailyDigest": True,
                            "breakingNews": False,
                            "favorite_categories": ["sport"],
                        },
                    }
                ),
                "culture": user_repo.create(
                    {
                        "email": "culture@news.com",
                        "username": "CultureLover",
                        "password": hashed_user_password,
                        "preferences": {
                            "dailyDigest": True,
                            "breakingNews": True,
                            "favorite_categories": ["kultura", "podorozhi"],
                        },
                    }
                ),
                "business": user_repo.create(
                    {
                        "email": "business@news.com",
                        "username": "BusinessAnalyst",
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": ["ekonomika", "politika"]
                        },
                    }
                ),
                "curious": user_repo.create(
                    {
                        "email": "curious@news.com",
                        "username": "CuriousReader",
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": [
                                "tehnologii",
                                "kultura",
                                "podorozhi",
                            ]
                        },
                    }
                ),
                "news_addict": user_repo.create(
                    {
                        "email": "newsaddict@news.com",
                        "username": "NewsAddict",
                        "password": hashed_user_password,
                        "preferences": {
                            "breakingNews": True,
                            "favorite_categories": ["politika", "sport", "ekonomika"],
                        },
                    }
                ),
                "casual": user_repo.create(
                    {
                        "email": "casual@news.com",
                        "username": "CasualReader",
                        "password": hashed_user_password,
                    }
                ),
                "Anna": user_repo.create(
                    {
                        "email": "anna@news.com",
                        "username": "Anna_K",
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": ["kultura", "podorozhi"]
                        },
                    }
                ),
                "Ivan": user_repo.create(
                    {
                        "email": "ivan@news.com",
                        "username": "Ivan_M",
                        "password": hashed_user_password,
                        "preferences": {"favorite_categories": ["sport", "tehnologii"]},
                    }
                ),
                "Mariya": user_repo.create(
                    {
                        "email": "mariya@news.com",
                        "username": "Mariya_P",
                        "password": hashed_user_password,
                        "preferences": {"favorite_categories": ["ekonomika"]},
                    }
                ),
                "Dmytro": user_repo.create(
                    {
                        "email": "dmytro@news.com",
                        "username": "Dmytro_S",
                        "password": hashed_user_password,
                        "preferences": {
                            "favorite_categories": ["politika", "ekonomika"]
                        },
                    }
                ),
                "Olga": user_repo.create(
                    {
                        "email": "olga@news.com",
                        "username": "Olga_V",
                        "password": hashed_user_password,
                        "preferences": {"favorite_categories": ["kultura", "sport"]},
                    }
                ),
            }
            print(f"✓ Користувачів створено: {len(users)}")
            print(f"  Пароль для всіх: {generic_user_password}")

            # ============================================================
            # 4. ПІДПИСКИ КОРИСТУВАЧІВ
            # ============================================================
            print("Призначення підписок користувачам...")
            sub_repo.subscribe_user(
                user_id=users["premium"].id, plan_id=premium_plan.id
            )
            sub_repo.subscribe_user(user_id=users["free"].id, plan_id=free_plan.id)
            sub_repo.subscribe_user(user_id=users["tech"].id, plan_id=premium_plan.id)
            sub_repo.subscribe_user(user_id=users["politics"].id, plan_id=free_plan.id)
            sub_repo.subscribe_user(user_id=users["sports"].id, plan_id=student_plan.id)
            sub_repo.subscribe_user(
                user_id=users["culture"].id, plan_id=premium_plan.id
            )
            sub_repo.subscribe_user(
                user_id=users["business"].id, plan_id=corporate_plan.id
            )
            sub_repo.subscribe_user(
                user_id=users["curious"].id, plan_id=student_plan.id
            )
            sub_repo.subscribe_user(
                user_id=users["news_addict"].id, plan_id=premium_plan.id
            )
            sub_repo.subscribe_user(user_id=users["casual"].id, plan_id=free_plan.id)
            sub_repo.subscribe_user(user_id=users["Anna"].id, plan_id=premium_plan.id)
            sub_repo.subscribe_user(user_id=users["Ivan"].id, plan_id=student_plan.id)
            sub_repo.subscribe_user(user_id=users["Mariya"].id, plan_id=free_plan.id)
            sub_repo.subscribe_user(
                user_id=users["Dmytro"].id, plan_id=corporate_plan.id
            )
            sub_repo.subscribe_user(user_id=users["Olga"].id, plan_id=free_plan.id)
            print("✓ Підписки призначено.")

            # ============================================================
            # 5. КАТЕГОРІЇ
            # ============================================================
            print("Створення категорій...")
            categories = {
                "politics": category_repo.create(
                    {
                        "name": "Політика",
                        "description": "Новини та аналітика політичного життя.",
                        "slug": "politika",
                    }
                ),
                "tech": category_repo.create(
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
                "economy": category_repo.create(
                    {
                        "name": "Економіка",
                        "description": "Все про фінанси та бізнес.",
                        "slug": "ekonomika",
                    }
                ),
                "culture": category_repo.create(
                    {
                        "name": "Культура",
                        "description": "Мистецтво, кіно та музика.",
                        "slug": "kultura",
                    }
                ),
                "travel": category_repo.create(
                    {
                        "name": "Подорожі",
                        "description": "Ідеї для ваших майбутніх мандрівок.",
                        "slug": "podorozhi",
                    }
                ),
                "health": category_repo.create(
                    {
                        "name": "Здоров'я",
                        "description": "Медичні новини та поради.",
                        "slug": "zdorovya",
                    }
                ),
                "science": category_repo.create(
                    {
                        "name": "Наука",
                        "description": "Наукові дослідження та відкриття.",
                        "slug": "nauka",
                    }
                ),
            }
            print(f"✓ Категорій створено: {len(categories)}")

            # ============================================================
            # 6. АВТОРИ (РОЗШИРЕНО - 12 авторів)
            # ============================================================
            print("Створення авторів...")
            authors = {
                "politics_1": author_repo.create(
                    {
                        "first_name": "Олена",
                        "last_name": "Петренко",
                        "bio": "Головний політичний оглядач з 15-річним досвідом.",
                    }
                ),
                "politics_2": author_repo.create(
                    {
                        "first_name": "Сергій",
                        "last_name": "Коваленко",
                        "bio": "Спеціаліст з міжнародних відносин.",
                    }
                ),
                "tech_1": author_repo.create(
                    {
                        "first_name": "Максим",
                        "last_name": "Ковальчук",
                        "bio": "Експерт з ринкових технологій та ШІ.",
                    }
                ),
                "tech_2": author_repo.create(
                    {
                        "first_name": "Юлія",
                        "last_name": "Іванова",
                        "bio": "Tech журналістка, фокус на стартапи.",
                    }
                ),
                "sport_1": author_repo.create(
                    {
                        "first_name": "Ірина",
                        "last_name": "Шевченко",
                        "bio": "Спортивний журналіст та колишній атлет.",
                    }
                ),
                "sport_2": author_repo.create(
                    {
                        "first_name": "Павло",
                        "last_name": "Сидоренко",
                        "bio": "Експерт з футзалу та малих видів спорту.",
                    }
                ),
                "economy_1": author_repo.create(
                    {
                        "first_name": "Андрій",
                        "last_name": "Захарчук",
                        "bio": "Фінансовий аналітик з 20-річним досвідом.",
                    }
                ),
                "economy_2": author_repo.create(
                    {
                        "first_name": "Катерина",
                        "last_name": "Бондаренко",
                        "bio": "Економіст, спеціаліст з місцевих ринків.",
                    }
                ),
                "culture_1": author_repo.create(
                    {
                        "first_name": "Софія",
                        "last_name": "Мельник",
                        "bio": "Мистецтвознавець та тревел-блогер.",
                    }
                ),
                "culture_2": author_repo.create(
                    {
                        "first_name": "Денис",
                        "last_name": "Литвин",
                        "bio": "Кінокритик та режисер документального кіно.",
                    }
                ),
                "science_1": author_repo.create(
                    {
                        "first_name": "Вадим",
                        "last_name": "Марченко",
                        "bio": "Науковець у сфері біотехнологій.",
                    }
                ),
                "health_1": author_repo.create(
                    {
                        "first_name": "Марина",
                        "last_name": "Гончаренко",
                        "bio": "Медицинська журналістка, доктор наук.",
                    }
                ),
            }
            print(f"✓ Авторів створено: {len(authors)}")

            # ============================================================
            # 7. ПІДПИСКИ НА АВТОРІВ
            # ============================================================
            print("Створення підписок на авторів...")
            users["tech"].followed_authors.append(authors["tech_1"])
            users["tech"].followed_authors.append(authors["tech_2"])
            users["tech"].followed_authors.append(authors["economy_1"])

            users["politics"].followed_authors.append(authors["politics_1"])
            users["politics"].followed_authors.append(authors["politics_2"])

            users["sports"].followed_authors.append(authors["sport_1"])
            users["sports"].followed_authors.append(authors["sport_2"])

            users["culture"].followed_authors.append(authors["culture_1"])
            users["culture"].followed_authors.append(authors["culture_2"])

            users["business"].followed_authors.append(authors["economy_1"])
            users["business"].followed_authors.append(authors["economy_2"])
            users["business"].followed_authors.append(authors["politics_1"])

            users["curious"].followed_authors.append(authors["tech_1"])
            users["curious"].followed_authors.append(authors["culture_1"])
            users["curious"].followed_authors.append(authors["science_1"])

            users["news_addict"].followed_authors.append(authors["politics_1"])
            users["news_addict"].followed_authors.append(authors["sport_1"])
            users["news_addict"].followed_authors.append(authors["economy_1"])

            users["Anna"].followed_authors.extend(
                [authors["culture_1"], authors["culture_2"]]
            )
            users["Ivan"].followed_authors.extend(
                [authors["sport_1"], authors["tech_1"]]
            )
            users["Mariya"].followed_authors.append(authors["economy_1"])
            users["Dmytro"].followed_authors.extend(
                [authors["politics_1"], authors["economy_1"]]
            )
            users["Olga"].followed_authors.extend(
                [authors["culture_1"], authors["sport_1"]]
            )

            print("✓ Підписки на авторів створено.")

            # ============================================================
            # 8. СТАТТІ (РОЗШИРЕНО - 60 статей)
            # ============================================================
            print("Створення статей...")

            articles = []
            article_data = [
                # ===== ПОЛІТИКА (10 статей) =====
                {
                    "author": authors["politics_1"],
                    "category": categories["politics"],
                    "title": "Нові політичні альянси: що очікувати у наступному десятилітті?",
                    "content": "<h2>Проведено аналіз</h2><p>Експерти передбачають принципові зміни в політичному ландшафті...</p>",
                    "is_breaking": True,
                    "views_count": 1520,
                },
                {
                    "author": authors["politics_1"],
                    "category": categories["politics"],
                    "title": "Місцеві вибори: хто лідирує в опитуваннях?",
                    "content": "<p>Останні опитування показують цікаву динаміку...</p>",
                    "views_count": 450,
                },
                {
                    "author": authors["politics_2"],
                    "category": categories["politics"],
                    "title": "Дипломатичні переговори: прорив чи затишшя перед бурею?",
                    "content": "<p>Міжнародні переговори набирають темпу...</p>",
                    "is_breaking": True,
                    "views_count": 890,
                },
                {
                    "author": authors["politics_2"],
                    "category": categories["politics"],
                    "title": "Анти-корупційна реформа: перший рік результатів",
                    "content": "<p>Аналіз впровадженої реформи дає позитивні сигнали...</p>",
                    "views_count": 620,
                },
                {
                    "author": authors["politics_1"],
                    "category": categories["politics"],
                    "title": "Парламентські дебати: гарячі темы тижня",
                    "content": "<p>У парламенті тривають бурхливі дискусії...</p>",
                    "views_count": 1230,
                },
                {
                    "author": authors["politics_2"],
                    "category": categories["politics"],
                    "title": "Регіональна політика: нові тренди розвитку",
                    "content": "<p>Регіони активізують власні стратегії розвитку...</p>",
                    "views_count": 340,
                },
                {
                    "author": authors["politics_1"],
                    "category": categories["politics"],
                    "title": "(ЧЕРНЕТКА) Таємна угода: що знає громадськість?",
                    "content": "<p>Розслідування таємної угоди...</p>",
                    "status": "draft",
                    "is_exclusive": True,
                    "views_count": 25,
                },
                {
                    "author": authors["politics_2"],
                    "category": categories["politics"],
                    "title": "Міжнародні санкції: чи будуть посилені?",
                    "content": "<p>Світові гравці обговорюють можливість посилення санкцій...</p>",
                    "is_breaking": True,
                    "views_count": 1650,
                },
                {
                    "author": authors["politics_1"],
                    "category": categories["politics"],
                    "title": "Новий виборчий закон: що змінюється?",
                    "content": "<p>Парламент схвалив нові вибори закон...</p>",
                    "views_count": 780,
                },
                {
                    "author": authors["politics_2"],
                    "category": categories["politics"],
                    "title": "Громадянське суспільство: голос народу посилюється",
                    "content": "<p>Організації громадськості активно впливають на політику...</p>",
                    "views_count": 560,
                },
                # ===== ТЕХНОЛОГІЇ (10 статей) =====
                {
                    "author": authors["tech_1"],
                    "category": categories["tech"],
                    "title": "Майбутнє ШІ: ексклюзивний аналіз та прогнози від інсайдерів",
                    "content": "<h2>Революція штучного інтелекту</h2><p>Експерти прогнозують масштабні зміни...</p>",
                    "is_exclusive": True,
                    "is_breaking": True,
                    "views_count": 2800,
                },
                {
                    "author": authors["tech_2"],
                    "category": categories["tech"],
                    "title": "Стартапи Гарвардського прискорювача: інновації року",
                    "content": "<p>Молоді компанії показують дивовижні результати...</p>",
                    "views_count": 1450,
                },
                {
                    "author": authors["tech_1"],
                    "category": categories["tech"],
                    "title": "Новий квантовий комп'ютер: прорив чи міф?",
                    "content": "<p>Дослідники представили прототип, який може революціонізувати обчислення...</p>",
                    "is_exclusive": True,
                    "views_count": 1900,
                },
                {
                    "author": authors["tech_2"],
                    "category": categories["tech"],
                    "title": "Що таке 6G і коли його очікувати?",
                    "content": "<p>Перші зусилля створення наступного покоління зв'язку...</p>",
                    "views_count": 820,
                },
                {
                    "author": authors["tech_1"],
                    "category": categories["tech"],
                    "title": "Огляд 'NeoGlass 2': окуляри доповненої реальності",
                    "content": "<p>Революційна технологія AR тепер доступна...</p>",
                    "views_count": 1050,
                },
                {
                    "author": authors["tech_2"],
                    "category": categories["tech"],
                    "title": "Кібербезпека 2025: нові вектори атак",
                    "content": "<p>Експерти попереджають про нові загрози...</p>",
                    "is_exclusive": True,
                    "views_count": 1600,
                },
                {
                    "author": authors["tech_1"],
                    "category": categories["tech"],
                    "title": "Як компанії використовують Big Data для прибутку",
                    "content": "<p>Аналіз даних дає надзвичайні прибутки...</p>",
                    "views_count": 780,
                },
                {
                    "author": authors["tech_2"],
                    "category": categories["tech"],
                    "title": "Блокчейн для звичайних людей: поясняємо просто",
                    "content": "<p>Розбираємось, як насправді працює блокчейн...</p>",
                    "views_count": 2100,
                },
                {
                    "author": authors["tech_1"],
                    "category": categories["tech"],
                    "title": "Облачні сервіси: який вибрати для вашого бізнесу?",
                    "content": "<p>Порівняння головних гравців на ринку...</p>",
                    "views_count": 950,
                },
                {
                    "author": authors["tech_2"],
                    "category": categories["tech"],
                    "title": "Хакери проти штучного інтелекту: хто переможе?",
                    "content": "<p>Цікава баталія технологій відбувається прямо зараз...</p>",
                    "is_breaking": True,
                    "views_count": 1350,
                },
                # ===== СПОРТ (10 статей) =====
                {
                    "author": authors["sport_1"],
                    "category": categories["sport"],
                    "title": "Історична перемога у фіналі Чемпіонату Світу з футболу",
                    "content": "<p>Команда здійснила неймовірний камбек...</p>",
                    "views_count": 3150,
                },
                {
                    "author": authors["sport_2"],
                    "category": categories["sport"],
                    "title": "Огляд тенісного турніру: нові зірки",
                    "content": "<p>Молоді таланти захоплюють світ тенісу...</p>",
                    "views_count": 1350,
                },
                {
                    "author": authors["sport_1"],
                    "category": categories["sport"],
                    "title": "Скандал у баскетбольній лізі: чи були матчі договірними?",
                    "content": "<p>Слідство розслідує можливі маніпуляції...</p>",
                    "views_count": 1150,
                },
                {
                    "author": authors["sport_2"],
                    "category": categories["sport"],
                    "title": "Олімпійські ігри 2028: 5 видів спорту, на які варто очікувати",
                    "content": "<p>Новинки призведуть до революції в змаганнях...</p>",
                    "views_count": 1890,
                },
                {
                    "author": authors["sport_1"],
                    "category": categories["sport"],
                    "title": "Волейбольна революція: як жінки змінили гру",
                    "content": "<p>Жіночий волейбол набирає популярності...</p>",
                    "views_count": 780,
                },
                {
                    "author": authors["sport_2"],
                    "category": categories["sport"],
                    "title": "Формула-1: найбільш динамічний сезон в історії",
                    "content": "<p>Невизначеність досі тримає світ у напруженні...</p>",
                    "is_exclusive": True,
                    "views_count": 2340,
                },
                {
                    "author": authors["sport_1"],
                    "category": categories["sport"],
                    "title": "Марафон чемпіонів: 5 найскладніших гонок у світі",
                    "content": "<p>Атлети змагаються на межі можливостей...</p>",
                    "views_count": 1200,
                },
                {
                    "author": authors["sport_2"],
                    "category": categories["sport"],
                    "title": "Дитячий спорт: як правильно почати тренування?",
                    "content": "<p>Експертні поради для батьків...</p>",
                    "views_count": 1620,
                },
                {
                    "author": authors["sport_1"],
                    "category": categories["sport"],
                    "title": "Легка атлетика: обновлені рекорди та техніки",
                    "content": "<p>Як спортсмени встановлюють нові межи...</p>",
                    "views_count": 890,
                },
                {
                    "author": authors["sport_2"],
                    "category": categories["sport"],
                    "title": "E-спорт: гейминг став справжнім спортом",
                    "content": "<p>Мільйони глядачів спостерігають за кіберспортом...</p>",
                    "is_breaking": True,
                    "views_count": 2560,
                },
                # ===== ЕКОНОМІКА (10 статей) =====
                {
                    "author": authors["economy_1"],
                    "category": categories["economy"],
                    "title": "Економічний прогноз на наступний квартал",
                    "content": "<p>Аналітики передбачають помірне зростання...</p>",
                    "views_count": 980,
                },
                {
                    "author": authors["economy_2"],
                    "category": categories["economy"],
                    "title": "Вплив інфляції на малий бізнес",
                    "content": "<p>Малі підприємства стискають ремені...</p>",
                    "views_count": 1100,
                },
                {
                    "author": authors["economy_1"],
                    "category": categories["economy"],
                    "title": "Ринок нерухомості 2025: 'бульбашка' чи стабільне зростання?",
                    "content": "<p>Експерти відрізняються у прогнозах...</p>",
                    "is_exclusive": True,
                    "views_count": 990,
                },
                {
                    "author": authors["economy_2"],
                    "category": categories["economy"],
                    "title": "Стартапи змінюють індустрію: випадок Українського 'Юнікорна'",
                    "content": "<p>Локальна компанія вийшла на світовий рівень...</p>",
                    "views_count": 1450,
                },
                {
                    "author": authors["economy_1"],
                    "category": categories["economy"],
                    "title": "Фондовий ринок впав на 10% на тлі новин про регуляції",
                    "content": "<p>Інвестори у паніці розпродають акції...</p>",
                    "is_breaking": True,
                    "views_count": 1700,
                },
                {
                    "author": authors["economy_2"],
                    "category": categories["economy"],
                    "title": "Крипто-визнання: чи прийматиме центробанк цифрові гроші?",
                    "content": "<p>Регулятори готуються до революції платежів...</p>",
                    "is_exclusive": True,
                    "views_count": 1320,
                },
                {
                    "author": authors["economy_1"],
                    "category": categories["economy"],
                    "title": "Світова торгівля: санкції та альянси переформатуються",
                    "content": "<p>Геополітика впливає на економіку більш ніж коли-небудь...</p>",
                    "views_count": 1230,
                },
                {
                    "author": authors["economy_2"],
                    "category": categories["economy"],
                    "title": "Бізнес для всіх: як отримати мікрокредит за годину?",
                    "content": "<p>ФінТек революціонізує доступ до капіталу...</p>",
                    "views_count": 1550,
                },
                {
                    "author": authors["economy_1"],
                    "category": categories["economy"],
                    "title": "Робота майбутнього: автоматизація чи можливості?",
                    "content": "<p>Робощик замінювати працівників чи створювати нові робочі місця?...</p>",
                    "views_count": 2100,
                },
                {
                    "author": authors["economy_2"],
                    "category": categories["economy"],
                    "title": "Сталий розвиток: прибуток та планета можуть жити разом?",
                    "content": "<p>Компанії доводять, що ESG – це прибутковий напрямок...</p>",
                    "views_count": 1400,
                },
                # ===== КУЛЬТУРА (8 статей) =====
                {
                    "author": authors["culture_1"],
                    "category": categories["culture"],
                    "title": "Цифрове мистецтво: як NFT змінює світ",
                    "content": "<p>Мистецтво переходить у цифровий простір...</p>",
                    "status": "draft",
                    "is_exclusive": True,
                    "views_count": 150,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["culture"],
                    "title": "Виставка авангардного мистецтва: що хотів сказати автор?",
                    "content": "<p>Критики розбирають сенс скульптур...</p>",
                    "views_count": 610,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["culture"],
                    "title": "Ексклюзив: режисер 'Тіней' про свій новий фільм",
                    "content": "<p>Інтерв'ю з режисером за кулісами...</p>",
                    "is_exclusive": True,
                    "views_count": 850,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["culture"],
                    "title": "Українське кіно: світовий успіх чи місцева справа?",
                    "content": "<p>Аналіз успіху український фільмів за кордоном...</p>",
                    "views_count": 1180,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["culture"],
                    "title": "Музика як мистецтво лікування: нова наука звуку",
                    "content": "<p>Психолог розповідає про силу музики...</p>",
                    "views_count": 920,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["culture"],
                    "title": "Театр у XXI столітті: старовинне мистецтво отримує новий вигляд",
                    "content": "<p>Театральні режисери експериментують з віртуальною реальністю...</p>",
                    "views_count": 1340,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["culture"],
                    "title": "Літерата та письменництво: як писати у цифрову епоху?",
                    "content": "<p>Письменники обговорюють вплив ШІ на творчість...</p>",
                    "views_count": 780,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["culture"],
                    "title": "Ретро-мода повертається: лукбук з 90-х років",
                    "content": "<p>Молодь знову носить старі забуті стилі...</p>",
                    "is_exclusive": True,
                    "views_count": 1570,
                },
                # ===== ПОДОРОЖІ (6 статей) =====
                {
                    "author": authors["culture_1"],
                    "category": categories["travel"],
                    "title": "Топ-5 недооцінених місць в Карпатах (та як до них дістатися)",
                    "content": "<p>Скриті красоти, які не знайдете у путівниках...</p>",
                    "views_count": 2200,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["travel"],
                    "title": "Приховані дворики Львова: гід для справжніх поціновувачів",
                    "content": "<p>Туристична маршрут для змаганних людей...</p>",
                    "views_count": 1300,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["travel"],
                    "title": "Дешево подорожувати світом: 10 лайфхаків мандрівника",
                    "content": "<p>Як побачити багато, витративши мало...</p>",
                    "views_count": 1850,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["travel"],
                    "title": "Сейшели vs Мальдіви: який вибрати для медового місяця?",
                    "content": "<p>Порівняння райських острівів...</p>",
                    "views_count": 1620,
                },
                {
                    "author": authors["culture_2"],
                    "category": categories["travel"],
                    "title": "Вулканічні гарячі джерела в Ісландії: прорив для туризму",
                    "content": "<p>Нові маршути вже доступні для туристів...</p>",
                    "is_exclusive": True,
                    "views_count": 1450,
                },
                {
                    "author": authors["culture_1"],
                    "category": categories["travel"],
                    "title": "Венеція тоне: останній шанс побачити Венецію",
                    "content": "<p>Урбанізація та клімат загрожують давньому місту...</p>",
                    "views_count": 2340,
                },
                # ===== ЗДОРОВ'Я (4 статей) =====
                {
                    "author": authors["health_1"],
                    "category": categories["health"],
                    "title": "Нова вакцина: як вона працює і чи вона безпечна?",
                    "content": "<p>Медичний журналіст розбирає науку...</p>",
                    "is_breaking": True,
                    "views_count": 1340,
                },
                {
                    "author": authors["health_1"],
                    "category": categories["health"],
                    "title": "Менталізм 2025: як діяти при стресі?",
                    "content": "<p>Психолог дає практичні поради...</p>",
                    "views_count": 1560,
                },
                {
                    "author": authors["health_1"],
                    "category": categories["health"],
                    "title": "Фітнес тренди: що дійсно працює, а що маркетинг?",
                    "content": "<p>Розбираємось у фітнес-лайфхаках...</p>",
                    "views_count": 1210,
                },
                {
                    "author": authors["health_1"],
                    "category": categories["health"],
                    "title": "Харчування при сахарному діабеті: практичний гід",
                    "content": "<p>Дієтолог розповідає про здорове харчування при діабеті...</p>",
                    "views_count": 980,
                },
                # ===== НАУКА (2 статей) =====
                {
                    "author": authors["science_1"],
                    "category": categories["science"],
                    "title": "CRISPR: редагування генів змінює медицину",
                    "content": "<p>Революція в генній терапії розпочалася...</p>",
                    "is_exclusive": True,
                    "views_count": 1870,
                },
                {
                    "author": authors["science_1"],
                    "category": categories["science"],
                    "title": "Марс чекає: як люди колонізуватимуть червану планету?",
                    "content": "<p>Науковці повільно готуються до експедиції...</p>",
                    "views_count": 2100,
                },
            ]

            for item in article_data:
                article = article_repo.create(
                    {
                        "author_id": item["author"].id,
                        "category_id": item["category"].id,
                        "title": item["title"],
                        "content": item["content"],
                        "status": item.get("status", "published"),
                        "is_breaking": item.get("is_breaking", False),
                        "is_exclusive": item.get("is_exclusive", False),
                        "views_count": item.get("views_count", 0),
                    }
                )
                articles.append(article)

            print(f"✓ Статей створено: {len(articles)}")

            # ============================================================
            # 9. ЛАЙКИ, ЗБЕРЕЖЕННЯ та ВЗАЄМОДІЇ
            # ============================================================
            print("Створення взаємодій (лайки, збереження)...")
            interactions_to_add = []

            # Індекси статей по категоріях (обновлено для 60 статей)
            interactions_map = {
                "politics": list(range(0, 10)),
                "tech": list(range(10, 20)),
                "sports": list(range(20, 30)),
                "economy": list(range(30, 40)),
                "culture": list(range(40, 48)),
                "travel": list(range(48, 54)),
                "health": list(range(54, 58)),
                "science": list(range(58, 60)),
            }

            # TechEnthusiast - Premium
            for idx in interactions_map["tech"][:8]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["tech"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            interactions_to_add.append(
                ArticleInteraction(
                    user_id=users["tech"].id,
                    article_id=articles[10].id,
                    interaction_type="saved",
                )
            )
            interactions_to_add.append(
                ArticleInteraction(
                    user_id=users["tech"].id,
                    article_id=articles[14].id,
                    interaction_type="saved",
                )
            )

            # PoliticsReader - Free
            for idx in interactions_map["politics"][:5]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["politics"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            # SportsFan - Student
            for idx in interactions_map["sports"][:7]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["sports"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            interactions_to_add.append(
                ArticleInteraction(
                    user_id=users["sports"].id,
                    article_id=articles[20].id,
                    interaction_type="saved",
                )
            )

            # CultureLover - Premium
            for idx in interactions_map["culture"]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["culture"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            for idx in interactions_map["travel"][:4]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["culture"].id,
                        article_id=articles[idx].id,
                        interaction_type="saved",
                    )
                )

            # BusinessAnalyst - Corporate
            for idx in interactions_map["economy"]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["business"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            for idx in interactions_map["politics"][:3]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["business"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            # CuriousReader - Student
            for idx in [10, 11, 12, 40, 41, 42, 48, 49, 58, 59]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["curious"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            interactions_to_add.append(
                ArticleInteraction(
                    user_id=users["curious"].id,
                    article_id=articles[42].id,
                    interaction_type="saved",
                )
            )

            # NewsAddict - Premium
            for idx in [0, 20, 30, 40, 1, 21, 31, 41]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["news_addict"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            # Free, Premium users та інші
            for idx in [0, 20, 48, 49]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["free"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            for idx in [0, 10, 40, 41]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["premium"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["premium"].id,
                        article_id=articles[idx].id,
                        interaction_type="saved",
                    )
                )

            # Anna, Ivan, Mariya, etc.
            for idx in interactions_map["culture"]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Anna"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            for idx in interactions_map["tech"][:5]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Ivan"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )
            for idx in interactions_map["sports"][:5]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Ivan"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            for idx in interactions_map["economy"][:6]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Mariya"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            for idx in [0, 1, 2, 30, 31]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Dmytro"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            for idx in [40, 41, 20, 21]:
                interactions_to_add.append(
                    ArticleInteraction(
                        user_id=users["Olga"].id,
                        article_id=articles[idx].id,
                        interaction_type="like",
                    )
                )

            db_session.add_all(interactions_to_add)
            print(f"✓ Взаємодій створено: {len(interactions_to_add)}")

            # ============================================================
            # 10. КОМЕНТАРІ (40+ коментарів) - ОБНОВЛЕНО
            # ============================================================
            print("Створення коментарів...")
            comments_data = [
                # Коментарі до політичних статей
                (
                    0,
                    users["politics"].id,
                    "Дуже цікава стаття! Дякую за глибокий аналіз.",
                ),
                (
                    0,
                    users["premium"].id,
                    "Написано добре, але не згоден з пунктом про енергетичну безпеку. Мені здається, тут є ризики.",
                ),
                (
                    1,
                    users["politics"].id,
                    "Цифри не збігаються з моїми спостереженнями. Де ви брали дані?",
                ),
                (
                    2,
                    users["Dmytro"].id,
                    "Найчастіше прочитаний матеріал про дипломатію. Браво!",
                ),
                (
                    3,
                    users["business"].id,
                    "Реформа дійсно змінює ситуацію, але потужні олігархи все ще чинять опір.",
                ),
                # Коментарі до спортивних статей
                (
                    20,
                    users["sports"].id,
                    "Це була неймовірна гра! Я був на стадіоні, емоції просто зашкалюють! Наші хлопці молодці!",
                ),
                (
                    20,
                    users["casual"].id,
                    "Кращий матч, який я коли-небудь бачив. Фізичні, вольові, стратегічні аспекти – все на найвищому рівні.",
                ),
                (
                    21,
                    users["Ivan"].id,
                    "Молода зірка дійсно грає приголомшливо добре. Має чемпіонський потенціал.",
                ),
                (
                    22,
                    users["news_addict"].id,
                    "Якщо це правда про договіри, це найбільший скандал у спорту цього року!",
                ),
                (
                    29,
                    users["sports"].id,
                    "E-спорт – це не спорт! Люди крутять мишками на дивані!",
                ),
                (
                    29,
                    users["casual"].id,
                    "@SportsFan Ви помиляєтесь. Це вимагає таланту, стратегії та здібностей. Точно як шахи.",
                ),
                # Коментарі до економічних статей
                (
                    30,
                    users["business"].id,
                    "Економіка буде стабільна, якщо центробанк утримуватиме курс.",
                ),
                (
                    31,
                    users["casual"].id,
                    "Мої друзі з малим бізнесом дійсно страждають від інфляції. Грустна реальність.",
                ),
                (
                    34,
                    users["Mariya"].id,
                    "Фондовий ринок буде і надалі волатильним. Краще тримати готівку!",
                ),
                (
                    38,
                    users["business"].id,
                    "Робота майбутнього – це буде новий рівень зайнятості для освічених людей.",
                ),
                # Коментарі до туристичних статей
                (
                    48,
                    users["culture"].id,
                    "Був на Боржаві минулого літа, це дійсно космос! Чорниці можна їсти просто з куща годинами :)",
                ),
                (
                    48,
                    users["Anna"].id,
                    "Дякую за ідеї! Про Криворівню не знав, обов'язково заїду наступного разу.",
                ),
                (
                    49,
                    users["culture"].id,
                    "Львів – це така красива та історична місто! Кожен кут розповідає історію.",
                ),
                (
                    50,
                    users["curious"].id,
                    "10 лайфхаків – дійсно корисні! Уже заплановую подорож до Бенгалії.",
                ),
                (
                    51,
                    users["Anna"].id,
                    "Мальдіви вибираємо! Туди краще літати. Сейшели – це дорого і далеко.",
                ),
                # Коментарі до культурних статей
                (
                    40,
                    users["culture"].id,
                    "NFT – це майбутнє мистецтва чи просто спекуляція?",
                ),
                (
                    41,
                    users["Anna"].id,
                    "Виставка була справді авангардна! Деякі твори мене шокували.",
                ),
                (
                    42,
                    users["culture"].id,
                    "Крутий фільм! Режисер – справжній художник. Чекаю наступного проекту!",
                ),
                (
                    43,
                    users["curious"].id,
                    "Українське кіно дійсно набирає популярність. Гордимося!",
                ),
                (
                    45,
                    users["Anna"].id,
                    "Театр – це душа культури. Віртуальна реальність не замінить живої емоції.",
                ),
                # Коментарі до здоров'я
                (
                    54,
                    users["news_addict"].id,
                    "Вакцина безпечна? Я все ще маю сумніви...",
                ),
                (
                    54,
                    users["premium"].id,
                    "Дослідження показує, що вакцина ефективна на 95%. Довіряйте науці!",
                ),
                (
                    55,
                    users["casual"].id,
                    "Стрес – це основна проблема 21 століття. Потребуємо більше часу для релаксації.",
                ),
                (
                    56,
                    users["Anna"].id,
                    "Фітнес тренди мінливі. Найважливіше – знайти те, що вам подобається!",
                ),
                # Коментарі до технологій
                (
                    10,
                    users["tech"].id,
                    "ШІ дійсно революціонізує все! Але потребуємо етичних норм.",
                ),
                (
                    11,
                    users["curious"].id,
                    "Стартапи з Гарварду створюють майбутнє прямо зараз. Вразливо!",
                ),
                (
                    12,
                    users["tech"].id,
                    "Квантові комп'ютери – це чи наступний крок людства, чи дорога до катастрофи?",
                ),
                (
                    15,
                    users["tech"].id,
                    "Чекаю, коли батарея буде тримати хоча б 8 годин. До того – це просто іграшка для багатіїв.",
                ),
                (19, users["casual"].id, "Хакери й ШІ – як у фільму про Термінаторів!"),
                # Коментарі до решти статей
                (1, users["casual"].id, "Всі вони однакові, нічого не зміниться."),
                (
                    1,
                    users["news_addict"].id,
                    "Не згоден з попереднім коментатором. Важливо ходити на вибори. Дякую за аналітику опитувань.",
                ),
                (
                    4,
                    users["casual"].id,
                    "Найтруднішим буде переглад всієї системи судочинства.",
                ),
                (56, users["sports"].id, "Йога – це не спорт, це медитація! :)"),
            ]

            for article_idx, user_id, text in comments_data:
                if article_idx < len(articles):  # Перевірка індексу
                    comment_repo.create(
                        {
                            "article_id": articles[article_idx].id,
                            "user_id": user_id,
                            "text": text,
                        }
                    )

            print(f"✓ Коментарів створено: {len(comments_data)}")

            # ============================================================
            # 11. РЕКЛАМНІ ОГОЛОШЕННЯ (20+ реклам)
            # ============================================================
            print("Створення рекламних оголошень...")
            ads_data = [
                {
                    "title": "Знижки на техніку",
                    "ad_type": "banner",
                    "impressions": 5000,
                    "clicks": 150,
                },
                {
                    "title": "Курс з Python",
                    "ad_type": "sidebar",
                    "impressions": 12000,
                    "clicks": 250,
                },
                {
                    "title": "Доставка їжі 'Смаколик'",
                    "ad_type": "sidebar",
                    "impressions": 8000,
                    "clicks": 180,
                },
                {
                    "title": "Нова колекція одягу",
                    "ad_type": "inline",
                    "impressions": 9500,
                    "clicks": 210,
                },
                {
                    "title": "Онлайн-кінотеатр 'KinoGo'",
                    "ad_type": "video",
                    "impressions": 25000,
                    "clicks": 1200,
                },
                {
                    "title": "Квитки на концерт 'Ocean'",
                    "ad_type": "popup",
                    "impressions": 3000,
                    "clicks": 450,
                },
                {
                    "title": "Страхування авто 'Надійно'",
                    "ad_type": "banner",
                    "impressions": 6000,
                    "clicks": 90,
                },
                {
                    "title": "Курси англійської 'SpeakUp'",
                    "ad_type": "sidebar",
                    "impressions": 11000,
                    "clicks": 320,
                },
                {
                    "title": "Спортивне харчування",
                    "ad_type": "inline",
                    "impressions": 7000,
                    "clicks": 280,
                },
                {
                    "title": "Подорож до Єгипту",
                    "ad_type": "banner",
                    "impressions": 15000,
                    "clicks": 600,
                },
                {
                    "title": "Новий смартфон 'Pixel 9'",
                    "ad_type": "video",
                    "impressions": 18000,
                    "clicks": 950,
                },
                {
                    "title": "Юридичні послуги 'Право'",
                    "ad_type": "sidebar",
                    "impressions": 2000,
                    "clicks": 15,
                    "active": False,
                },
                {
                    "title": "Фітнес-клуб 'SportLife'",
                    "ad_type": "popup",
                    "impressions": 4500,
                    "clicks": 700,
                },
                {
                    "title": "Ремонт квартир 'Майстер'",
                    "ad_type": "inline",
                    "impressions": 5500,
                    "clicks": 110,
                },
                {
                    "title": "Книгарня 'Літера'",
                    "ad_type": "banner",
                    "impressions": 8500,
                    "clicks": 310,
                },
                {
                    "title": "Вебінар з маркетингу",
                    "ad_type": "sidebar",
                    "impressions": 6200,
                    "clicks": 420,
                },
                {
                    "title": "Кава 'Gourmet Beans'",
                    "ad_type": "inline",
                    "impressions": 4300,
                    "clicks": 130,
                },
                {
                    "title": "Ігровий монітор 'ViewMax'",
                    "ad_type": "video",
                    "impressions": 16000,
                    "clicks": 880,
                },
                {
                    "title": "Підпишіться на розсилку!",
                    "ad_type": "popup",
                    "impressions": 10000,
                    "clicks": 1500,
                },
                {
                    "title": "Еко-товари 'Zeleno'",
                    "ad_type": "sidebar",
                    "impressions": 7100,
                    "clicks": 190,
                },
                {
                    "title": "Ветеринарна клініка 'ДоброЛап'",
                    "ad_type": "banner",
                    "impressions": 3900,
                    "clicks": 120,
                },
                {
                    "title": "Йога-студія 'Гармонія'",
                    "ad_type": "inline",
                    "impressions": 5100,
                    "clicks": 220,
                },
                {
                    "title": "Хмарне сховище 'CloudDrive'",
                    "ad_type": "sidebar",
                    "impressions": 13000,
                    "clicks": 410,
                },
                {
                    "title": "Альбом гурту 'Stray'",
                    "ad_type": "video",
                    "impressions": 22000,
                    "clicks": 1100,
                },
            ]

            for ad in ads_data:
                ad_repo.create(
                    {
                        "title": ad["title"],
                        "content": f"Реклама товару '{ad['title']}'. Дізнайтеся більше!",
                        "ad_type": ad["ad_type"],
                        "is_active": ad.get("active", True),
                        "impressions_count": ad["impressions"],
                        "clicks_count": ad["clicks"],
                    }
                )

            print(f"✓ Рекламних оголошень створено: {len(ads_data)}")

            # ============================================================
            # ФІКСАЦІЯ ВСІХ ЗМІН
            # ============================================================
            db_session.commit()
            print("\n✅ Усі дані успішно створено і збережено!")

        except Exception as e:
            print(f"\n❌ СТАЛАСЯ ПОМИЛКА: {e}")
            import traceback

            traceback.print_exc()
            db_session.rollback()
        finally:
            db_session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  ЗАПУСК РОЗШИРЕНОГО SEED-СКРИПТУ ДЛЯ БД")
    print("=" * 60)
    seed_database()
    print("\n" + "=" * 60)
    print("  БА ЗА ДАНИХ ГОТОВА ДО ВИКОРИСТАННЯ")
    print("=" * 60)
