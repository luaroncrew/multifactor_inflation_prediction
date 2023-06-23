from typing import List


class ShoppingCart:
    items: List = []

    def __init__(self) -> None:
        pass

    def add(self, item: str):
        self.items.append(item)

    def size(self) -> int:
        return len(self.items)

    def get_items(self) -> List[str]:
        return self.items
