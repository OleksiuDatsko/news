from repositories.author import AuthorRepository
from typing import Dict, Any, Tuple, List

class AuthorAdminService:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def get_authors_paginated(self, page: int, per_page: int, search: str) -> Tuple[List[Dict[str, Any]], int]:
        """
        Отримує пагінований список авторів для адмін-панелі.
        """
        authors, total = self.author_repo.get_paginated_authors(
            page=page, per_page=per_page, search_query=search
        )
        
        result = [author.to_dict() for author in authors]
        return result, total