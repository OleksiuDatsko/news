from repositories.subscription import SubscriptionRepository


class SubscriptionService:
    def __init__(self, repo: SubscriptionRepository):
        self.repo = repo

    def list_plans(self):
        return self.repo.get_all_plans()

    def subscribe(self, user_id: int, plan_id: int):
        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            raise ValueError("План не знайдено")
        return self.repo.subscribe_user(user_id, plan_id)

    def get_current_subscription(self, user_id: int):
        return self.repo.get_active_user_subscription(user_id)

    def get_subscription_history(self, user_id: int):
        return self.repo.get_user_subscription_history(user_id)
