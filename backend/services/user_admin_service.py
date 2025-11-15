from repositories.user import UserRepository
from typing import Dict, Any, Tuple, List

class UserAdminService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_users_paginated(self, page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
        """
        Отримує пагінований список користувачів для адмін-панелі.
        """
        users, total = self.user_repo.get_paginated_users(
            page=page, per_page=per_page
        )
        
        result = [user.to_dict() for user in users]
        return result, total