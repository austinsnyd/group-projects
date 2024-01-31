def geq(a, b):
    return a >= b


def logical_mess(a, b, c):
    if a is None or b is None or c is None:
        return -1
    elif a == b or a == c or b == c:
        return 1
    elif a == b == c:
        return 2
    elif c == 10 and a != 5:
        return 3
    elif c == 10 and a == 5:
        return 4
    elif c > 10 and a > b:
        return 4
    else:
        return 6


class Adventurer:
    def __init__(self, name, starting_gold):
        self.name = name
        self.gold = max(starting_gold, 0)
        self.inventory = []

    def lose_gold(self, amount):
        if self.gold - amount < 0:
            self.gold = 0
            return False
        else:
            self.gold -= amount
            return True

    def win_gold(self, amount):
        self.gold += amount

    def add_inventory(self, item):
        self.inventory.append(item)

    def remove_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            return False
