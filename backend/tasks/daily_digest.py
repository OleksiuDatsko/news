import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import json
from sqlalchemy import desc
from sqlalchemy.orm import Session
from pywebpush import webpush, WebPushException


os.environ.setdefault("FLASK_CONFIG", "default")

from app import create_app
from models.user import User
from models.article import Article
from models.push_subscription import PushSubscription
from models.notification import Notification
from models.newsletter import NewsletterSubscription
from database import IDatabaseConnection


load_dotenv("/app/.env")
VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": os.environ.get("VAPID_ADMIN_EMAIL")}

app = create_app()


def send_daily_digest_push():
    """
    Збирає та надсилає щоденний дайджест PUSH-СПОВІЩЕНЬ користувачам,
    які на нього підписані (в налаштуваннях профілю).
    """
    with app.app_context():
        print(f"[{datetime.now()}] Запуск завдання 'send_daily_digest_PUSH'...")

        db_session: Session = app.container.resolve(IDatabaseConnection).get_session()

        try:
            users_to_notify = (
                db_session.query(User)
                .filter(User.preferences["dailyDigest"].as_boolean() == True)
                .all()
            )

            if not users_to_notify:
                print("Користувачів для PUSH-дайджесту не знайдено.")
                db_session.close()
                return

            print(f"Знайдено {len(users_to_notify)} користувачів для розсилки.")

            twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
            top_articles = (
                db_session.query(Article)
                .filter(
                    Article.status == "published",
                    Article.created_at >= twenty_four_hours_ago,
                )
                .order_by(desc(Article.views_count))
                .limit(5)
                .all()
            )

            if not top_articles:
                print("Немає нових статей за останні 24 години.")
                db_session.close()
                return
            
            top_article = top_articles[0]

            push_payload = {
                "title": "Ваш щоденний дайджест новин 📰",
                "body": f"Головна історія: {top_article.title}",
                "url": f"/articles/{top_article.id}",
            }

            notifications = []
            for user in users_to_notify:
                notifications.append(
                    Notification(
                        user_id=user.id,
                        article_id=top_article.id,
                        type="daily_digest",
                        title=push_payload["title"],
                        message=push_payload["body"],
                    )
                )
                print(f"Створено сповіщення для користувача {user.id}.")

            if notifications:
                db_session.add_all(notifications)
                print(f"[Observer]: Створено {len(notifications)} сповіщень в БД.")
                db_session.commit()

            subscriptions = (
                db_session.query(PushSubscription)
                .filter(
                    PushSubscription.user_id.in_([user.id for user in users_to_notify])
                )
                .all()
            )

            print(f"Надсилання дайджесту на {len(subscriptions)} пристроїв...")

            sent_count = 0
            for sub in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": sub.endpoint,
                            "keys": {
                                "p256dh": sub.p256dh,
                                "auth": sub.auth,
                            },
                        },
                        data=json.dumps(push_payload),
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS,
                    )
                    sent_count += 1
                except WebPushException as e:
                    print(f"Push failed: {e}")

            print(f"Успішно надіслано {sent_count} PUSH-сповіщень.")

        except Exception as e:
            print(f"ПОМИЛКА під час виконання daily_digest_PUSH: {e}")
        finally:
            if db_session.is_active:
                db_session.close()
            print("Завдання 'send_daily_digest_PUSH' завершено.")


def send_daily_digest_email_stub():
    with app.app_context():
        print(f"[{datetime.now()}] Запуск завдання 'send_daily_digest_EMAIL_STUB'...")

        db_session: Session = app.container.resolve(IDatabaseConnection).get_session()

        try:
            active_email_subs = (
                db_session.query(NewsletterSubscription)
                .filter_by(type="general_digest", is_active=True)
                .all()
            )

            if not active_email_subs:
                print("Користувачів для EMAIL-розсилки не знайдено.")
                db_session.close()
                return

            user_ids = [sub.user_id for sub in active_email_subs]
            users = db_session.query(User).filter(User.id.in_(user_ids)).all()

            print(f"Знайдено {len(users)} користувачів для EMAIL-розсилки.")

            for user in users:
                print(
                    f"  [ЗАГЛУШКА]: Надсилаємо email-дайджест користувачу {user.email}..."
                )

            print(f"Успішно 'надіслано' {len(users)} email-дайджестів.")

        except Exception as e:
            print(f"ПОМИЛКА під час виконання email_stub: {e}")
        finally:
            if db_session.is_active:
                db_session.close()
            print("Завдання 'send_daily_digest_EMAIL_STUB' завершено.")


if __name__ == "__main__":
    send_daily_digest_push()
    send_daily_digest_email_stub()
