class Item:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.shopping_cart = []

    def add(self, item: Item):
        self.shopping_cart.append(item)

    def total(self) -> int:
        return sum(item.price for item in self.shopping_cart)

    def __len__(self) -> int:
        return len(self.shopping_cart)
    
    
if __name__ == '__main__':
    n = int(input())
    items = []
    for _ in range(n):
        name, price = input().split()
        item = Item(name, int(price))
        items.append(item)

    cart = ShoppingCart()
    for i in range(int(input())):
        operation = input().split()
        if operation[0] == 'add':
            item_name = operation[1]
            item = next(item for item in items if item.name == item_name)
            cart.add(item)
        elif operation[0] == 'total':
            print(cart.total())
        elif operation[0] == 'len':
            print(len(cart))