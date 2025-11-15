from repositories.admin import AdminRepository
from typing import Dict, Any, Tuple, List

class AdminUserService:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def get_admins_paginated(self, page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
        """
        Отримує пагінований список адміністраторів для адмін-панелі.
        """
        admins, total = self.admin_repo.get_paginated_admins(
            page=page, per_page=per_page
        )
        
        result = [admin.to_dict() for admin in admins]
        return result, total