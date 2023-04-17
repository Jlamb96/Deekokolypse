
class color_changer():
    def __init__(self):
        self.nothing = 1




    def hunger_change(self, hunger):
        if hunger < 30:
            color = "red"
        elif hunger < 50:
            color = "yellow"
        else:
            color = "white"
        return color

    def energy_change(self, energy):
        if energy < 30:
            color = "red"
        elif energy < 50:
            color = "yellow"
        else:
            color = "white"
        return color

    def thirst_change(self, thirst):
        if thirst < 30:
            color = "red"
        elif thirst < 50:
            color = "yellow"
        else:
            color = "white"
        return color

    def health_change(self, health):
        if health < 30:
            color = "red"
        elif health < 50:
            color = "yellow"
        else:
            color = "white"
        return color

