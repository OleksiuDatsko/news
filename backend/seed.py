import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app
from database import IDatabaseConnection
from models import *
from models.author import author_followers  # 👈 *** ВАЖЛИВО: Імпортуємо M2M таблицю ***

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
    # Очищення M2M таблиці `author_followers`
    session.execute(author_followers.delete()) # 👈 *** ДОДАНО ОЧИЩЕННЯ M2M ***
    
    # Очищення залежних таблиць
    session.query(ArticleInteraction).delete()
    session.query(Comment).delete()
    session.query(ArticleView).delete()
    session.query(AdView).delete()
    session.query(UserSubscriptionPlan).delete()
    session.query(Notification).delete()
    session.query(NewsletterSubscription).delete()

    # Очищення основних таблиць
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
            
            # --- 🔽🔽🔽 ДОДАВАННЯ НОВИХ ПЛАНІВ 🔽🔽🔽 ---
            student_plan = sub_repo.create(
                {
                    "name": "Студентський",
                    "permissions": {
                        "no_ads": False, # Студенти бачать рекламу
                        "exclusive_content": True, # Але мають доступ до ексклюзиву
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
                    "price_per_month": 7.99, # Дешевше за преміум, бо оптом
                    "description": "Повний доступ для вашої команди. Розрахунок за одного користувача.",
                }
            )
            # --- 🔼🔼🔼 КІНЕЦЬ НОВИХ ПЛАНІВ 🔼🔼🔼 ---

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
            
            # --- 🔽🔽🔽 ПОЧАТОК НОВИХ КОРИСТУВАЧІВ 🔽🔽🔽 ---
            
            tech_user = user_repo.create(
                {
                    "email": "tech@news.com",
                    "username": "TechEnthusiast",
                    "password": hashed_user_password,
                    "preferences": {
                        "dailyDigest": True,
                        "breakingNews": True,
                        "favorite_categories": ["tehnologii", "ekonomika"]
                    }
                }
            )
            
            politics_user = user_repo.create(
                {
                    "email": "politics@news.com",
                    "username": "PoliticsReader",
                    "password": hashed_user_password,
                    "preferences": {
                        "dailyDigest": False,
                        "breakingNews": True,
                        "favorite_categories": ["politika"]
                    }
                }
            )
            
            sports_user = user_repo.create(
                {
                    "email": "sport@news.com",
                    "username": "SportsFan",
                    "password": hashed_user_password,
                    "preferences": {
                        "dailyDigest": True,
                        "breakingNews": False,
                        "favorite_categories": ["sport"]
                    }
                }
            )

            culture_user = user_repo.create(
                {
                    "email": "culture@news.com",
                    "username": "CultureLover",
                    "password": hashed_user_password,
                    "preferences": {
                        "dailyDigest": True,
                        "breakingNews": True,
                        "favorite_categories": ["kultura", "podorozhi"]
                    }
                }
            )
            
            print("Нових користувачів створено.")
            print(f"\tПароль для всіх: {generic_user_password}")

            # --- 🔼🔼🔼 КІНЕЦЬ НОВИХ КОРИСТУВАЧІВ 🔼🔼🔼 ---
            

            # --- 4. Призначення підписок ---
            sub_repo.subscribe_user(user_id=premium_user.id, plan_id=premium_plan.id)
            sub_repo.subscribe_user(user_id=free_user.id, plan_id=free_plan.id)
            
            # --- 🔽🔽🔽 ПІДПИСКИ ДЛЯ НОВИХ КОРИСТУВАЧІВ 🔽🔽🔽 ---
            sub_repo.subscribe_user(user_id=tech_user.id, plan_id=premium_plan.id) # Tech - Преміум
            sub_repo.subscribe_user(user_id=politics_user.id, plan_id=free_plan.id) # Politics - Безкоштовний
            sub_repo.subscribe_user(user_id=sports_user.id, plan_id=student_plan.id) # 👈 *** ОНОВЛЕНО: SportsFan тепер студент ***
            sub_repo.subscribe_user(user_id=culture_user.id, plan_id=premium_plan.id) # Culture - Преміум
            print("Підписки призначено.")
            # --- 🔼🔼🔼 КІНЕЦЬ ПІДПИСОК 🔼🔼🔼 ---

            # --- 5. Створення категорій та авторів ---
            print("Створення категорій та авторів...")
            cat_politics = category_repo.create(
                {
                    "name": "Політика",
                    "description": "Новини та аналітика політичного життя.",
                    "slug": "politika",
                }
            )
            cat_tech = category_repo.create(
                {"name": "Технології", "description": "Огляди гаджетів та новини IT.", "slug": "tehnologii"}
            )
            cat_sport = category_repo.create(
                {"name": "Спорт", "description": "Найважливіші спортивні події.", "slug": "sport"}
            )
            cat_economy = category_repo.create(
                {"name": "Економіка", "description": "Все про фінанси та бізнес.", "slug": "ekonomika"}
            )
            cat_culture = category_repo.create(
                {"name": "Культура", "description": "Мистецтво, кіно та музика.", "slug": "kultura"}
            )
            cat_travel = category_repo.create(
                {"name": "Подорожі", "description": "Ідеї для ваших майбутніх мандрівок.", "slug": "podorozhi"}
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
            # (Тут ваш поточний код створення 20 статей. Я його скорочу для ясності, але він має бути тут)
            
            # --- ВЕЛИКА СТАТТЯ 1 ---
            article1 = article_repo.create(
                {
                    "author_id": author1.id,
                    "category_id": cat_politics.id,
                    "title": "Нові політичні альянси: що очікувати у наступному десятилітті?",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_breaking": True, "views_count": 1520,
                }
            )
            # --- ВЕЛИКА СТАТТЯ 2 ---
            article2 = article_repo.create(
                {
                    "author_id": author2.id,
                    "category_id": cat_tech.id,
                    "title": "Майбутнє ШІ: ексклюзивний аналіз та прогнози від інсайдерів",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_exclusive": True, "is_breaking": True, "views_count": 2800,
                }
            )
            article3 = article_repo.create(
                {
                    "author_id": author3.id, "category_id": cat_sport.id,
                    "title": "Історична перемога у фіналі Чемпіонату Світу з футболу",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 3150,
                }
            )
            article4 = article_repo.create(
                {
                    "author_id": author4.id, "category_id": cat_economy.id,
                    "title": "Економічний прогноз на наступний квартал",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 980,
                }
            )
            article5 = article_repo.create(
                {
                    "author_id": author5.id, "category_id": cat_culture.id,
                    "title": "Цифрове мистецтво: як NFT змінює світ",
                    "content": """... (Багато HTML) ...""",
                    "status": "draft", "is_exclusive": True, "views_count": 150,
                }
            )
            article6 = article_repo.create(
                {
                    "author_id": author1.id, "category_id": cat_politics.id,
                    "title": "Аналіз законопроєкту про медіа",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 750,
                }
            )
            article7 = article_repo.create(
                {
                    "author_id": author2.id, "category_id": cat_tech.id,
                    "title": "Новий квантовий комп'ютер: прорив чи міф?",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_exclusive": True, "views_count": 1900,
                }
            )
            article8 = article_repo.create(
                {
                    "author_id": author5.id, "category_id": cat_travel.id,
                    "title": "Топ-5 недооцінених місць в Карпатах (та як до них дістатися)",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 2200,
                }
            )
            article9 = article_repo.create(
                {
                    "author_id": author4.id, "category_id": cat_economy.id,
                    "title": "Вплив інфляції на малий бізнес",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 1100,
                }
            )
            article10 = article_repo.create(
                {
                    "author_id": author3.id, "category_id": cat_sport.id,
                    "title": "Огляд тенісного турніру: нові зірки",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 1350,
                }
            )
            article11 = article_repo.create(
                {
                    "author_id": author1.id, "category_id": cat_politics.id,
                    "title": "Місцеві вибори: хто лідирує в опитуваннях?",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 450,
                }
            )
            article12 = article_repo.create(
                {
                    "author_id": author2.id, "category_id": cat_tech.id,
                    "title": "Що таке 6G і коли його очікувати?",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 820,
                }
            )
            article13 = article_repo.create(
                {
                    "author_id": author3.id, "category_id": cat_sport.id,
                    "title": "Скандал у баскетбольній лізі: чи були матчі договірними?",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 1150,
                }
            )
            article14 = article_repo.create(
                {
                    "author_id": author4.id, "category_id": cat_economy.id,
                    "title": "Ринок нерухомості 2025: 'бульбашка' чи стабільне зростання?",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_exclusive": True, "views_count": 990,
                }
            )
            article15 = article_repo.create(
                {
                    "author_id": author5.id, "category_id": cat_culture.id,
                    "title": "Виставка авангардного мистецтва: що хотів сказати автор?",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 610,
                }
            )
            article16 = article_repo.create(
                {
                    "author_id": author5.id, "category_id": cat_travel.id,
                    "title": "Приховані дворики Львова: гід для справжніх поціновувачів",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 1300,
                }
            )
            article17 = article_repo.create(
                {
                    "author_id": author1.id, "category_id": cat_politics.id,
                    "title": "(ЧЕРНЕТКА) Розслідування корупційних схем у морському порту",
                    "content": """... (Багато HTML) ...""",
                    "status": "draft", "is_exclusive": True, "views_count": 25,
                }
            )
            article18 = article_repo.create(
                {
                    "author_id": author2.id, "category_id": cat_tech.id,
                    "title": "Огляд 'NeoGlass 2': окуляри доповненої реальності",
                    "content": """... (Багато HTML) ...""", "status": "published", "views_count": 1050,
                }
            )
            article19 = article_repo.create(
                {
                    "author_id": author4.id, "category_id": cat_economy.id,
                    "title": "Фондовий ринок впав на 10% на тлі новин про регуляції",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_breaking": True, "views_count": 1700,
                }
            )
            article20 = article_repo.create(
                {
                    "author_id": author5.id, "category_id": cat_culture.id,
                    "title": "Ексклюзив: режисер 'Тіней' про свій новий фільм",
                    "content": """... (Багато HTML) ...""",
                    "status": "published", "is_exclusive": True, "views_count": 850,
                }
            )

            print("Статті створено.")
            
            # --- 🔽🔽🔽 ПОЧАТОК НОВИХ ВЗАЄМОДІЙ 🔽🔽🔽 ---
            print("Створення підписок на авторів...")
            # TechEnthusiast підписується на авторів 2 (Tech) та 4 (Economy)
            tech_user.followed_authors.append(author2)
            tech_user.followed_authors.append(author4)
            tech_user.followed_authors.append(author1) # 👈 *** ДОДАНО ***
            
            # PoliticsReader підписується на автора 1 (Politics)
            politics_user.followed_authors.append(author1)
            politics_user.followed_authors.append(author4) # 👈 *** ДОДАНО ***
            
            # SportsFan підписується на автора 3 (Sport)
            sports_user.followed_authors.append(author3)
            
            # CultureLover підписується на автора 5 (Culture/Travel)
            culture_user.followed_authors.append(author5)
            
            # --- 🔽 ДОДАНО ПІДПИСКИ ДЛЯ БАЗОВИХ ЮЗЕРІВ 🔽 ---
            # PremiumUser підписується на Політику (author1) та Культуру (author5)
            premium_user.followed_authors.append(author1)
            premium_user.followed_authors.append(author5)

            # FreeUser підписується на Спорт (author3)
            free_user.followed_authors.append(author3)
            # --- 🔼 КІНЕЦЬ ДОДАНИХ ПІДПИСОК 🔼 ---

            print("Підписки на авторів створено.")

            print("Створення лайків та збережень...")
            interactions_to_add = [
                # TechEnthusiast (Premium)
                ArticleInteraction(user_id=tech_user.id, article_id=article2.id, interaction_type="like"),
                ArticleInteraction(user_id=tech_user.id, article_id=article7.id, interaction_type="like"),
                ArticleInteraction(user_id=tech_user.id, article_id=article12.id, interaction_type="like"),
                ArticleInteraction(user_id=tech_user.id, article_id=article4.id, interaction_type="saved"),
                ArticleInteraction(user_id=tech_user.id, article_id=article7.id, interaction_type="saved"),
                
                # PoliticsReader (Free) - не може зберігати
                ArticleInteraction(user_id=politics_user.id, article_id=article1.id, interaction_type="like"),
                ArticleInteraction(user_id=politics_user.id, article_id=article6.id, interaction_type="like"),
                ArticleInteraction(user_id=politics_user.id, article_id=article11.id, interaction_type="like"),

                # SportsFan (Student) - 👈 *** ОНОВЛЕНО: Тепер може зберігати ***
                ArticleInteraction(user_id=sports_user.id, article_id=article3.id, interaction_type="like"),
                ArticleInteraction(user_id=sports_user.id, article_id=article10.id, interaction_type="like"),
                ArticleInteraction(user_id=sports_user.id, article_id=article13.id, interaction_type="like"),
                ArticleInteraction(user_id=sports_user.id, article_id=article3.id, interaction_type="saved"), # 👈 *** ДОДАНО ЗБЕРЕЖЕННЯ ***
                
                # CultureLover (Premium)
                ArticleInteraction(user_id=culture_user.id, article_id=article8.id, interaction_type="like"),
                ArticleInteraction(user_id=culture_user.id, article_id=article15.id, interaction_type="like"),
                ArticleInteraction(user_id=culture_user.id, article_id=article16.id, interaction_type="like"),
                ArticleInteraction(user_id=culture_user.id, article_id=article20.id, interaction_type="like"),
                ArticleInteraction(user_id=culture_user.id, article_id=article8.id, interaction_type="saved"),
                ArticleInteraction(user_id=culture_user.id, article_id=article16.id, interaction_type="saved"),
                ArticleInteraction(user_id=culture_user.id, article_id=article20.id, interaction_type="saved"),
                
                # FreeUser (для тестів)
                ArticleInteraction(user_id=free_user.id, article_id=article1.id, interaction_type="like"),
                ArticleInteraction(user_id=free_user.id, article_id=article8.id, interaction_type="like"),

                # PremiumUser (для тестів)
                ArticleInteraction(user_id=premium_user.id, article_id=article1.id, interaction_type="like"),
                ArticleInteraction(user_id=premium_user.id, article_id=article2.id, interaction_type="like"),
                ArticleInteraction(user_id=premium_user.id, article_id=article2.id, interaction_type="saved"),
                ArticleInteraction(user_id=premium_user.id, article_id=article8.id, interaction_type="saved"),
            ]
            db_session.add_all(interactions_to_add)
            print("Лайки та збереження додано.")
            
            # --- 🔼🔼🔼 КІНЕЦЬ НОВИХ ВЗАЄМОДІЙ 🔼🔼🔼 ---

            # --- 7. Створення коментарів ---
            print("Створення коментарів...")
            # (Ваш поточний код створення коментарів)
            comment_repo.create(
                { "article_id": article1.id, "user_id": free_user.id, "text": "Дуже цікава стаття! Дякую за глибокий аналіз."}
            )
            comment_repo.create(
                {
                    "article_id": article1.id,
                    "user_id": premium_user.id,
                    "text": "Написано добре, але не згоден з пунктом про енергетичну безпеку. Мені здається, тут є ризики.",
                }
            )
            comment_repo.create(
                {
                    "article_id": article3.id,
                    "user_id": premium_user.id,
                    "text": "Це була неймовірна гра! Я був на стадіоні, емоції просто зашкалюють! Наші хлопці молодці!",
                }
            )
            comment_repo.create(
                {
                    "article_id": article4.id,
                    "user_id": free_user.id,
                    "text": "Корисна інформація, дякую. Як раз думав, що робити з цінами у своїй кав'ярні.",
                }
            )
            comment_repo.create(
                {
                    "article_id": article8.id,
                    "user_id": free_user.id,
                    "text": "Був на Боржаві минулого літа, це дійсно космос! Чорниці можна їсти просто з куща годинами :)",
                }
            )
            comment_repo.create(
                {
                    "article_id": article8.id,
                    "user_id": premium_user.id,
                    "text": "Дякую за ідеї! Про Криворівню не знав, обов'язково заїду наступного разу.",
                }
            )

            # --- НОВІ КОМЕНТАРІ ---
            comment_repo.create(
                {
                    "article_id": article11.id,
                    "user_id": free_user.id,
                    "text": "Всі вони однакові, нічого не зміниться.",
                }
            )
            comment_repo.create(
                {
                    "article_id": article11.id,
                    "user_id": premium_user.id,
                    "text": "Не згоден з попереднім коментатором. Важливо ходити на вибори. Дякую за аналітику опитувань.",
                }
            )
            comment_repo.create(
                {
                    "article_id": article18.id,
                    "user_id": premium_user.id,
                    "text": "Чекаю, коли батарея буде тримати хоча б 8 годин. До того – це просто іграшка для багатіїв.",
                }
            )
            comment_repo.create(
                { "article_id": article19.id, "user_id": free_user.id, "text": "Оце так новина! Треба було зранку все продавати..."}
            )
            # --- КІНЕЦЬ НОВИХ КОМЕНТАРІВ ---

            print("Коментарі створено.")

            # --- 8. Створення рекламних оголошень ---
            print("Створення рекламних оголошень...")
            # (Ваш поточний код створення реклами)
            ad_repo.create(
                { "title": "Знижки на техніку", "content": "Оновіть свій ноутбук! Знижки до -30% на всю лінійку XPS.", "ad_type": "banner", "is_active": True, "impressions_count": 5000, "clicks_count": 150, }
            )
            ad_repo.create(
                {
                    "title": "Курс з Python",
                    "content": "Станьте розробником за 6 місяців. Гарантія працевлаштування.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 12000,
                    "clicks_count": 250,
                }
            )
            ad_repo.create(
                {
                    "title": "Доставка їжі 'Смаколик'",
                    "content": "Безкоштовна доставка першого замовлення за промокодом 'NEWSAPP'.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 8000,
                    "clicks_count": 180,
                }
            )
            ad_repo.create(
                {
                    "title": "Нова колекція одягу",
                    "content": "Стильні речі для вашого осіннього гардеробу.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 9500,
                    "clicks_count": 210,
                }
            )
            ad_repo.create(
                {
                    "title": "Онлайн-кінотеатр 'KinoGo'",
                    "content": "Дивіться ексклюзивні прем'єри фільмів у високій якості.",
                    "ad_type": "video",
                    "is_active": True,
                    "impressions_count": 25000,
                    "clicks_count": 1200,
                }
            )
            ad_repo.create(
                {
                    "title": "Квитки на концерт 'Ocean'",
                    "content": "Не пропустіть виступ улюбленого гурту у вашому місті!",
                    "ad_type": "popup",
                    "is_active": True,
                    "impressions_count": 3000,
                    "clicks_count": 450,
                }
            )
            ad_repo.create(
                {
                    "title": "Страхування авто 'Надійно'",
                    "content": "Надійний захист для вашого автомобіля. Розрахуйте вартість онлайн.",
                    "ad_type": "banner",
                    "is_active": True,
                    "impressions_count": 6000,
                    "clicks_count": 90,
                }
            )
            ad_repo.create(
                {
                    "title": "Курси англійської 'SpeakUp'",
                    "content": "Вивчай мову з носіями. Перший урок безкоштовно.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 11000,
                    "clicks_count": 320,
                }
            )
            ad_repo.create(
                {
                    "title": "Спортивне харчування",
                    "content": "Все для ваших тренувань. Протеїни, вітаміни та аксесуари.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 7000,
                    "clicks_count": 280,
                }
            )
            ad_repo.create(
                {
                    "title": "Подорож до Єгипту",
                    "content": "Гарячі тури за найкращими цінами! Від $499 на тиждень.",
                    "ad_type": "banner",
                    "is_active": True,
                    "impressions_count": 15000,
                    "clicks_count": 600,
                }
            )
            ad_repo.create(
                {
                    "title": "Новий смартфон 'Pixel 9'",
                    "content": "Оновіть свій гаджет сьогодні. Камера зі штучним інтелектом.",
                    "ad_type": "video",
                    "is_active": True,
                    "impressions_count": 18000,
                    "clicks_count": 950,
                }
            )
            ad_repo.create(
                {
                    "title": "Юридичні послуги 'Право'",
                    "content": "Професійна консультація для вашого бізнесу. Відкриття ФОП.",
                    "ad_type": "sidebar",
                    "is_active": False,  # Неактивна реклама для тестування
                    "impressions_count": 2000,
                    "clicks_count": 15,
                }
            )
            ad_repo.create(
                {
                    "title": "Фітнес-клуб 'SportLife'",
                    "content": "Абонемент на рік зі знижкою 50% лише до кінця місяця!",
                    "ad_type": "popup",
                    "is_active": True,
                    "impressions_count": 4500,
                    "clicks_count": 700,
                }
            )
            ad_repo.create(
                {
                    "title": "Ремонт квартир 'Майстер'",
                    "content": "Якісно, швидко та з гарантією. Безкоштовний виїзд замірника.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 5500,
                    "clicks_count": 110,
                }
            )

            # --- Додаткові оголошення ---

            ad_repo.create(
                {
                    "title": "Книгарня 'Літера'",
                    "content": "Нові надходження світових бестселерів. Замовляйте онлайн.",
                    "ad_type": "banner",
                    "is_active": True,
                    "impressions_count": 8500,
                    "clicks_count": 310,
                }
            )
            ad_repo.create(
                {
                    "title": "Вебінар з маркетингу",
                    "content": "Дізнайтеся, як просувати свій бренд у 2025 році. Реєстрація відкрита.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 6200,
                    "clicks_count": 420,
                }
            )
            ad_repo.create(
                {
                    "title": "Кава 'Gourmet Beans'",
                    "content": "Свіжообсмажена арабіка з доставкою додому.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 4300,
                    "clicks_count": 130,
                }
            )
            ad_repo.create(
                {
                    "title": "Новий ігровий монітор 'ViewMax'",
                    "content": "4K, 144Hz. Повне занурення у гру.",
                    "ad_type": "video",
                    "is_active": True,
                    "impressions_count": 16000,
                    "clicks_count": 880,
                }
            )
            ad_repo.create(
                {
                    "title": "Підпишіться на нашу розсилку!",
                    "content": "Отримуйте ексклюзивні статті та знижки першими.",
                    "ad_type": "popup",
                    "is_active": True,
                    "impressions_count": 10000,
                    "clicks_count": 1500,
                }
            )
            ad_repo.create(
                {
                    "title": "Еко-товари 'Zeleno'",
                    "content": "Все для свідомого споживання: від косметики до побутової хімії.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 7100,
                    "clicks_count": 190,
                }
            )
            ad_repo.create(
                {
                    "title": "Ветеринарна клініка 'ДоброЛап'",
                    "content": "Цілодобова допомога вашим улюбленцям. Консультація онлайн.",
                    "ad_type": "banner",
                    "is_active": True,
                    "impressions_count": 3900,
                    "clicks_count": 120,
                }
            )
            ad_repo.create(
                {
                    "title": "Йога-студія 'Гармонія'",
                    "content": "Знайдіть свій внутрішній баланс. Пробне заняття – 100 грн.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 5100,
                    "clicks_count": 220,
                }
            )
            ad_repo.create(
                {
                    "title": "Хмарне сховище 'CloudDrive'",
                    "content": "Надійне зберігання ваших файлів. 1ТБ за 99 грн/міс.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 13000,
                    "clicks_count": 410,
                }
            )
            ad_repo.create(
                {
                    "title": "Новий альбом гурту 'Stray'",
                    "content": "Слухайте на всіх стрімінгових платформах!",
                    "ad_type": "video",
                    "is_active": True,
                    "impressions_count": 22000,
                    "clicks_count": 1100,
                }
            )
            ad_repo.create(
                {
                    "title": "Дитячі іграшки 'Joy'",
                    "content": "Розвиваючі ігри для дітей будь-якого віку.",
                    "ad_type": "banner",
                    "is_active": True,
                    "impressions_count": 6800,
                    "clicks_count": 160,
                }
            )
            ad_repo.create(
                {
                    "title": "Зимові шини 'NordTire'",
                    "content": "Готуйте авто до зими! Знижки на монтаж.",
                    "ad_type": "banner",
                    "is_active": False,  # Ще одна неактивна
                    "impressions_count": 4000,
                    "clicks_count": 50,
                }
            )
            ad_repo.create(
                {
                    "title": "Курси фотографії",
                    "content": "Навчіться робити професійні знімки на свій смартфон.",
                    "ad_type": "inline",
                    "is_active": True,
                    "impressions_count": 5300,
                    "clicks_count": 300,
                }
            )
            ad_repo.create(
                {
                    "title": "Оренда офісів 'WorkSpace'",
                    "content": "Сучасні офісні рішення для вашого бізнесу. Від $200/міс.",
                    "ad_type": "sidebar",
                    "is_active": True,
                    "impressions_count": 9100,
                    "clicks_count": 230,
                }
            )
            ad_repo.create(
                {
                    "title": "Зубна клініка 'Smile'",
                    "content": "Професійна чистка зубів зі знижкою 20%.",
                    "ad_type": "popup",
                    "is_active": True,
                    "impressions_count": 2800,
                    "clicks_count": 350,
                }
            )

            print("Рекламні оголошення створено.")
            
            # --- 9. Фіксація всіх змін ---
            db_session.commit()

        except Exception as e:
            print(f"!!! СТАЛАСЯ ПОМИЛКА: {e}")
            db_session.rollback()
        finally:
            db_session.close()


if __name__ == "__main__":
    print("Запуск скрипту для наповнення бази даних...")
    seed_database()
    print("\nУспішно завершено! База даних готова до використання.")