import random
from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict

rotation_state = defaultdict(int)

class AdSelectionStrategy(ABC):
    """Абстрактний базовий клас для всіх стратегій вибору реклами."""
    
    @abstractmethod
    def select_ads(self, ads: List, limit: int) -> List:
        """Метод, який обирає та повертає рекламні оголошення."""
        pass

class DefaultAdStrategy(AdSelectionStrategy):
    """Стандартна стратегія: повертає перші `limit` оголошень."""
    
    def select_ads(self, ads: List, limit: int) -> List:
        return ads[:limit]

class RotationAdStrategy(AdSelectionStrategy):
    """
    Стратегія ротації: показує оголошення по черзі.
    Зберігає індекс останнього показаного оголошення для кожного типу.
    """
    
    def select_ads(self, ads: List, limit: int) -> List:
        if not ads:
            return []
            
        ad_type_key = ads[0].ad_type
        
        start_index = rotation_state[ad_type_key]
        
        num_ads = len(ads)
        selected = []
        for i in range(num_ads):
            index = (start_index + i) % num_ads
            selected.append(ads[index])
            if len(selected) == limit:
                break
        
        # Оновлюємо стан для наступного виклику
        rotation_state[ad_type_key] = (start_index + len(selected)) % num_ads
        
        return selected

class RandomAdStrategy(AdSelectionStrategy):
    """Стратегія випадкового вибору: повертає випадкові оголошення."""
    
    def select_ads(self, ads: List, limit: int) -> List:
        return random.sample(ads, min(limit, len(ads)))