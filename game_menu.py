import random
from tkinter import *
import sys
import pygame
import graphics
from tkinter import messagebox
from graphics import Scav_Camp
from graphics import trader
from status_check import color_changer

MAX_DAYS = 14
STARTING_MONEY = random.randint(85, 150)
STARTING_HUNGER = 100
STARTING_THIRST = 100
STARTING_HEALTH = 100
STARTING_ENERGY = 100
STARTING_LOCATION = Scav_Camp
pygame.mixer.init()


class GameStats:
    def __init__(self):
        # Define game variables
        self.trader_buy_list = None
        self.window = Tk()
        self.window.iconbitmap("favicon.ico")
        self.window.title("Deekokolypse")
        self.color_change = color_changer()
        self.times_looted = 0
        self.window.config(width=self.window.winfo_screenwidth(), height=self.window.winfo_screenheight(), bg="black")
        self.days_left = MAX_DAYS
        self.money = STARTING_MONEY
        self.hunger = STARTING_HUNGER
        self.thirst = STARTING_THIRST
        self.health = STARTING_HEALTH
        self.energy = STARTING_ENERGY
        self.location_player = STARTING_LOCATION
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("song.mp3"), loops=10)
        pygame.mixer.Channel(0).set_volume(0.2)
        pygame.mixer.Channel(1).set_volume(0.3)
        pygame.mixer.Channel(2).set_volume(0.5)
        self.car_parts = []
        self.tools = []
        self.weapons = []
        self.ammo = 10
        self.drinks = []
        self.food = []
        self.meds = []
        self.canvas_top = Canvas(self.window, bg="black", highlightthickness=0)
        self.canvas_bottom = Canvas(self.window, bg="#113826", highlightthickness=0)
        self.canvas_text = Canvas(self.window, bg="black", highlightthickness=0)
        self.canvas_text.grid(row=0, column=0)
        self.canvas_top.grid(row=0, column=1)
        self.canvas_bottom.grid(row=1, column=0, columnspan=4)
        self.health_number = Label(self.canvas_text, text=f"Health: {self.health}", fg="white", bg="black",
                                   font='Helvetica 18 bold')
        self.health_number.grid(column=0, row=0)
        self.hunger_number = Label(self.canvas_text, text=f"Hunger: {self.hunger}", fg="white", bg="black",
                                   font='Helvetica 18 bold')
        self.hunger_number.grid(column=0, row=1)
        self.ammo_have = Label(self.canvas_text, text=f"Ammo: {self.ammo}", fg="white", bg="black",
                               font="Helvetica 18 bold")
        self.ammo_have.grid(column=0, row=3, columnspan=1)
        self.money_number = Label(self.canvas_text, text=f"Money: ${self.money}", fg="white", bg="black",
                                  font='Helvetica 18 bold')
        self.money_number.grid(column=1, row=3)
        self.thirst_number = Label(self.canvas_text, text=f"Thirst: {self.thirst}", fg="white", bg="black",
                                   font="Helvetica 18 bold")
        self.thirst_number.grid(column=1, row=1)
        self.energy_number = Label(self.canvas_text, text=f"Energy: {self.energy}", fg="white", bg="black",
                                   font='Helvetica 18 bold')
        self.energy_number.grid(column=1, row=0)
        self.days_number = Label(self.canvas_text, text=f"Days Left: {self.days_left}", fg="red", bg="black",
                                 font='Helvetica 24 bold')
        self.days_number.grid(column=3, row=0, pady=(0, 120), padx=25)
        self.current_location = Label(self.canvas_top, text=f"Current Location:", fg="red", bg="black",
                                      font='Helvetica 12 bold')
        self.current_location.grid(column=0, row=2)
        self.location_pic = Label(self.canvas_top, text=self.location_player, fg="red", bg="black",
                                  font=("Courier", 10))
        self.location_pic.grid(column=0, row=3, pady=30, padx=30)
        self.checked_state = IntVar()
        self.mute_button = Checkbutton(self.canvas_top, text="Mute Sound?", variable=self.checked_state,
                                       command=self.play)
        self.mute_button.grid(column=1, row=3)
        if len(self.tools) == 0:
            self.tools_owned = Label(self.canvas_top, text=f"Tools: None", fg="white", bg="black",
                                 font="Helvetica 18 bold")
        else:
            tools_formatted = str(self.tools)
            tools_formatted = tools_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.tools_owned = Label(self.canvas_top, text=f"Tools: {tools_formatted}", fg="white", bg="black",
                                     font="Helvetica 18 bold")
        self.tools_owned.grid(column=0, row=5)
        if len(self.car_parts) == 0:
            self.car_parts_text = Label(self.canvas_top, text=f"Car Parts: None", fg="white", bg="black",
                                        font="Helvetica 18 bold")
        else:
            self.car_parts_text = Label(self.canvas_top, text=f"Car Parts: {self.car_parts}", fg="white", bg="black",
                                        font='Helvetica 18 bold')
        self.car_parts_text.grid(column=0, row=4)

        self.TOOLS = ["Wrench", "Hammer", "Screwdriver", "Pliers"]
        self.TOOLS2 = ["Wrench", "Hammer", "Screwdriver", "Pliers"]


        self.DRINKS = ["Energy Drink", "Clean Water", "Milk", "Fruit Juice", "Soda", "Lemonade", "Green Tea",
                       "Sparkling Water", "Sports Drink"]
        self.FOOD = ["MRE", "Noodles", "Canned Beef", "Candy Bar", "Crackers", "Deli Meat", "Potato Chips",
                     "Canned Sardines", "Cereal", "Bread", "Hotdogs", "Watermelon"]
        self.FOOD_FOREST = ["Corn", "Wild Onion", "Fish", "Wild Carrot", "Wild Meat"]
        self.MEDS = ["IFAK", "AFAK", "Civilian MedKit", "Bandage", "Grizzly Medkit", "AI-2 Medkit"]
        self.PARTS = ["Engine", "Transmission", "Tire", "Battery", "Steering Wheel"]
        self.PARTS2 = ["Engine", "Transmission", "Tire", "Battery", "Steering Wheel"]
        self.parts_missing = ["Engine", "Transmission", "Tire", "Battery", "Steering Wheel"]

        self.thirst_add = {"Energy Drink": 25,
                           "Clean Water": 45,
                           "Milk": 40,
                           "Fruit Juice": 35,
                           'Soda': 20,
                           "Lemonade": 37,
                           "Dirty Water": 25,
                           "Green Tea": 30,
                           "Sparkling Water": 40,
                           "Sports Drink": 42,
                           "Watermelon": 20
                           }

        self.food_add = {"MRE": 50,
                         "Noodles": 25,
                         "Canned Beef": 35,
                         "Candy Bar": 15,
                         "Corn": 20,
                         "Wild Onion": 15,
                         "Fish": 45,
                         "Wild Carrot": 18,
                         "Crackers": 15,
                         "Deli Meat": 30,
                         "Potato Chips": 10,
                         "Canned Sardines": 28,
                         "Cereal": 32,
                         "Wild Meat": 35,
                         "Bread": 27,
                         "Hotdogs": 38,
                         "Watermelon": 20
                         }
        self.MED_ADD = {"IFAK": 35,
                        "AFAK": 45,
                        "Civilian MedKit": 25,
                        "Bandage": 15,
                        "AI-2 Medkit": 20,
                        "Grizzly Medkit": 65,
                        "Saline Bag": 100
                        }
        self.MASTER_LIST = {"MRE": 30,
                            "Noodles": 15,
                            "Canned Beef": 20,
                            "Candy Bar": 8,
                            "Corn": 8,
                            "Wild Onion": 8,
                            "Fish": 25,
                            "Wild Carrot": 10,
                            "Crackers": 8,
                            "Deli Meat": 18,
                            "Potato Chips": 6,
                            "Canned Sardines": 22,
                            "Wrench": 25,
                            "Hammer": 15,
                            "Screwdriver": 10,
                            "Pliers": 15,
                            "Engine": 200,
                            "Transmission": 150,
                            "Tire": 50,
                            "Steering Wheel": 45,
                            "Battery": 50,
                            "Energy Drink": 15,
                            "Clean Water": 25,
                            "Milk": 30,
                            "Fruit Juice": 15,
                            'Soda': 8,
                            "Lemonade": 17,
                            "Sports Drink": 25,
                            "IFAK": 15,
                            "AFAK": 20,
                            "Civilian MedKit": 10,
                            "Bandage": 5,
                            "Grizzly Medkit": 30,
                            "Saline Bag": 45,
                            "Ammo": 20,
                            "Cereal": 18,
                            "Green Tea": 13,
                            "Sparkling Water": 25,
                            "Wild Meat": 20,
                            "AI-2 Medkit": 10,
                            "Bread": 15,
                            "Hotdogs": 23,
                            "Watermelon": 13
                            }
        self.EXTRA_ADD = {"Saline Bag": 100,
                          "Soda": 10,
                          "Energy Drink": 25,
                          "Sports Drink": 18
                          }

        GameStats.create_middle_buttons(self)
        if len(self.weapons) == 0:
            self.weapons_number = Label(self.canvas_top, text=f"Weapons: None", fg="white", bg="black",
                                        font='Helvetica 18 bold')
            self.weapons_number.grid(column=0, row=6)
        else:
            weapons_formatted = str(self.weapons)
            weapons_formatted = weapons_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.weapons_number = Label(self.canvas_top, text=f"Weapons: {weapons_formatted}", fg="white", bg="black",
                                        font='Helvetica 18 bold')
            self.weapons_number.grid(column=0, row=6)
        self.drinks_text = Label(self.canvas_text, text=f"Drinks: {len(self.drinks)}", fg="white", bg="black",
                                 font="Helvetica 18 bold")
        self.drinks_text.grid(column=3, row=1)
        self.food_text = Label(self.canvas_text, text=f"Food: {len(self.food)}", fg="white", bg="black",
                               font="Helvetica 18 bold")
        self.food_text.grid(column=3, row=2)
        self.meds_text = Label(self.canvas_text, text=f"Meds: {len(self.meds)}", fg="white", bg="black",
                               font="Helvetica 18 bold")
        self.meds_text.grid(column=3, row=3)
        self.random_trader_loot()
        self.window.mainloop()

    # Define game functions
    def random_trader_loot(self):
        self.trader_buy_list = []
        for _ in range(random.randint(1, 2)):
            self.trader_buy_list.append(random.choice(self.TOOLS2))
            self.trader_buy_list.append(random.choice(self.PARTS2))
        for _ in range(random.randint(7, 10)):
            self.trader_buy_list.append(random.choice(self.DRINKS))
        for _ in range(random.randint(3, 8)):
            self.trader_buy_list.append(random.choice(self.FOOD))
        for _ in range(random.randint(2, 4)):
            self.trader_buy_list.append(random.choice(self.FOOD_FOREST))
        for _ in range(random.randint(2, 4)):
            self.trader_buy_list.append(random.choice(self.MEDS))

    def fight_zombie(self):
        print("Fighting zombie...")
        self.energy = random.randint(10, 20)
        self.health -= random.randint(10, 20)
        self.hunger -= random.randint(5, 10)
        self.thirst -= random.randint(5, 10)

    def listbox_used_food(self, event):
        # Gets current selection from listbox
        try:
            self.eat_confirm_button.destroy()
        except:
            None
        self.food_eaten = (self.food_list.get(self.food_list.curselection()))
        self.eat_confirm_button = Button(self.canvas_bottom, text=f"Eat {self.food_eaten}?", command=self.eat_food,
                                         font=18)
        self.eat_confirm_button.grid(column=1, row=2)

    def eat_food(self):
        self.no_health_loss = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("eat1.mp3"))
        self.food.remove(self.food_eaten)
        self.food_list.destroy()
        self.eat_confirm_button.destroy()
        self.hunger += self.food_add[self.food_eaten]
        if self.food_eaten in self.thirst_add:
            self.thirst += self.thirst_add[self.food_eaten]
        if self.food_eaten == "Candy Bar":
            self.energy += 15
        if self.hunger > 100:
            self.hunger = 100
        GameStats.update_text(self)
        self.eat_confirm_button.destroy()
        self.consume_menu.destroy()
        self.game_over()
        GameStats.create_middle_buttons(self)

    def food_buttons(self):
        if len(self.food) == 0:
            messagebox.showinfo("No food", "You have no food")
        else:
            GameStats.delete_buttons(self)
            self.consume_menu = Button(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=18)
            self.consume_menu.grid(column=1, row=1)
            self.food_list = Listbox(self.canvas_bottom, height=(len(self.food)), width=20, font=60, bg="black",
                                     fg="white", highlightthickness=0)
            for food_item in self.food:
                if food_item in self.food:
                    self.food_list.insert(self.food.index(food_item), food_item)
                    self.food_list.bind("<<ListboxSelect>>", self.listbox_used_food)
                    self.food_list.grid(column=1, row=0)

    def exit_eat_drink(self):
        try:
            self.consume_menu.destroy()
        except:
            None
        try:
            self.drink_confirm_button.destroy()
        except:
            None
        try:
            self.eat_confirm_button.destroy()
        except:
            None
        try:
            self.drink_box.destroy()
        except:
            None
        try:
            self.food_list.destroy()
        except:
            None
        try:
            self.med_box.destroy()
            self.med_confirm_button.destroy()
        except:
            None
        GameStats.create_middle_buttons(self)

    def listbox_used_drink(self, event):
        # Gets current selection from listbox
        try:
            self.drink_confirm_button.destroy()
        except:
            None
        finally:
            self.drink_consumed = (self.drink_box.get(self.drink_box.curselection()))
            self.drink_confirm_button = Button(self.canvas_bottom, text=f"Drink {self.drink_consumed}?",
                                               command=self.drink_liquid, font=18)
            self.drink_confirm_button.grid(column=1, row=2)

    def drink_liquid(self):
        self.no_health_loss = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("drink1.mp3"))
        try:
            self.drinks.remove(self.drink_consumed)
        finally:
            self.drink_box.destroy()
            self.drink_confirm_button.destroy()
            self.thirst += self.thirst_add[self.drink_consumed]
            if self.drink_consumed in self.EXTRA_ADD:
                self.energy += self.EXTRA_ADD[self.drink_consumed]
            elif self.drink_consumed == "Milk":
                self.hunger += 15
            elif self.drink_consumed == "Dirty Water":
                self.health -= 15
            if self.thirst > 100:
                self.thirst = 100
            GameStats.update_text(self)
            GameStats.create_middle_buttons(self)
            self.drink_confirm_button.destroy()
            self.consume_menu.destroy()

    def drink_buttons(self):
        if self.location_player == graphics.forest and "Dirty Water" not in self.drinks:
            self.drinks.append("Dirty Water")
            self.update_text()
        if len(self.drinks) == 0:
            messagebox.showinfo("No Drinks", "You have no Drinks")
        else:
            GameStats.delete_buttons(self)
            self.consume_menu = Button(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=18)
            self.consume_menu.grid(column=1, row=1)
            self.drink_box = Listbox(self.canvas_bottom, height=(len(self.drinks)), width=20, font=60, bg="black",
                                     fg="white", highlightthickness=0)
            for drink_item in self.drinks:
                if drink_item in self.drinks:
                    self.drink_box.insert(self.drinks.index(drink_item), drink_item)
                    self.drink_box.bind("<<ListboxSelect>>", self.listbox_used_drink)
                    self.drink_box.grid(column=1, row=0)

    def listbox_used_meds(self, event):
        # Gets current selection from listbox
        try:
            self.med_confirm_button.destroy()
        except:
            None
        finally:
            self.med_consumed = (self.med_box.get(self.med_box.curselection()))
            self.med_confirm_button = Button(self.canvas_bottom, text=f"Use {self.med_consumed}?",
                                             command=self.use_meds, font=18)
            self.med_confirm_button.grid(column=1, row=2)

    def use_meds(self):
        self.no_health_loss = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("heal1.ogg"))
        self.meds.remove(self.med_consumed)
        self.med_box.destroy()
        self.med_confirm_button.destroy()
        if self.med_consumed in self.EXTRA_ADD:
            self.thirst += self.EXTRA_ADD[self.med_consumed]
        self.health += self.MED_ADD[self.med_consumed]
        if self.health > 100:
            self.health = 100
        GameStats.update_text(self)
        GameStats.create_middle_buttons(self)
        self.med_confirm_button.destroy()
        self.consume_menu.destroy()
        self.med_box.destroy()

    def med_buttons(self):
        if len(self.meds) == 0:
            messagebox.showinfo("No Meds", "You have no Meds")
        else:
            GameStats.delete_buttons(self)
            self.consume_menu = Button(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=18)
            self.consume_menu.grid(column=1, row=1)
            self.med_box = Listbox(self.canvas_bottom, height=(len(self.meds)), width=20, font=60, bg="black",
                                   fg="white", highlightthickness=0)
            for med_item in self.meds:
                if med_item in self.meds:
                    self.med_box.insert(self.meds.index(med_item), med_item)
                    self.med_box.bind("<<ListboxSelect>>", self.listbox_used_meds)
                    self.med_box.grid(column=1, row=0)

    def end_day(self):
        self.no_health_loss = False
        if self.days_left == 8:
            self.random_trader_loot()
        self.thirst -= random.randint(15, 25)
        self.hunger -= random.randint(10, 20)
        if self.hunger <= 0:
            self.hunger = 0
        if self.thirst <= 0:
            self.thirst = 0
        self.energy = 100
        self.days_left -= 1
        GameStats.update_text(self)
        GameStats.game_over(self)

    def exhausted(self):
        self.thirst -= random.randint(20, 30)
        self.hunger -= random.randint(15, 20)
        self.energy = 80
        self.days_left -= 1
        GameStats.update_text(self)
        GameStats.game_stats.delete_buttons(self)
        GameStats.game_over(self)

    def exit_game(self):
        sys.exit()

    def play(self):
        if self.checked_state.get() == 0:
            pygame.mixer.Channel(0).unpause()
        else:
            pygame.mixer.Channel(0).pause()


    def trader(self):
        if self.location_player == graphics.Scav_Camp:
            GameStats.delete_buttons(self)
            GameStats.create_center_window(self)
            self.no_health_loss = True
            button = Button(self.trader_window, text="Exit Trader", command=self.close_trader, font=18)
            button.grid(column=2, row=1)
            trader_image = Label(self.trader_window, text=trader, font=("Courier", 4), fg="green", bg="black")
            trader_image.grid(column=2, row=0)
            trader_text = Label(self.trader_window, text="Buy", font=("Courier", 14), fg="green", bg="black")
            trader_text.grid(column=3, row=1)
            if len(self.food) + len(self.drinks) + len(self.meds) + len(self.car_parts) + len(self.tools) > 0:
                trader_text2 = Label(self.trader_window, text="Sell", font=("Courier", 14), fg="green", bg="black")
                trader_text2.grid(column=1, row=1)
            self.create_trader_buybox()
            self.create_trader_sellbox()


    def create_trader_buybox(self):
        self.buy_box = Listbox(self.trader_window, height=8, width=20, font=10, bg="black",
                               fg="white", highlightthickness=0)
        scrollbar = Scrollbar(self.trader_window)
        scrollbar.grid(column=4, row=0)
        scrollbar.config(command=self.buy_box.yview)
        for item in self.trader_buy_list:
            self.buy_box.insert(self.trader_buy_list.index(item), item)
            self.buy_box.bind("<<ListboxSelect>>", self.listbox_bought_item)
            self.buy_box.grid(column=3, row=0)
            self.buy_box.config(yscrollcommand=scrollbar.set)

    def create_trader_sellbox(self):
        self.player_sell = []
        self.sell_box = Listbox(self.trader_window, height=8 , width=20, font=10, bg="black",fg="white", highlightthickness=0)
        if self.ammo >= 10:
            self.player_sell.append("Ammo")
        for item in self.food:
            self.player_sell.append(item)
        for item in self.drinks:
            self.player_sell.append(item)
        for item in self.meds:
            self.player_sell.append(item)
        for item in self.car_parts:
            self.player_sell.append(item)
        for item in self.tools:
            self.player_sell.append(item)
        for item in self.player_sell:
            self.sell_box.insert(self.player_sell.index(item), item)
            self.sell_box.bind("<<ListboxSelect>>", self.listbox_sold_item)
            self.sell_box.grid(column=1, row=0)
        if len(self.player_sell) >= 1:
            scrollbar1 = Scrollbar(self.trader_window)
            scrollbar1.grid(column=0, row=0)
            scrollbar1.config(command=self.sell_box.yview)
        try:
            self.sell_box.config(yscrollcommand=scrollbar1.set)
        except:
            None

    def listbox_sold_item(self, event):
        # Gets current selection from listbox
        try:
            self.sell_confirm_button.destroy()
            self.buy_confirm_button.destroy()
        except:
            None
        finally:
            self.sold_item = (self.sell_box.get(self.sell_box.curselection()))
            self.sell_confirm_button = Button(self.trader_window, text=f"Sell {self.sold_item} for ${round(self.MASTER_LIST[self.sold_item] // 2)}?", command=self.sell_item, font=10)
            self.sell_confirm_button.grid(column=1, row=1)

    def sell_item(self):
        self.no_health_loss = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sell1.ogg"))
        self.sell_box.destroy()
        self.sell_confirm_button.destroy()
        if self.sold_item in self.FOOD_FOREST or self.sold_item in self.FOOD:
            self.food.remove(self.sold_item)
        elif self.sold_item in self.MEDS:
            self.meds.remove(self.sold_item)
        elif self.sold_item in self.DRINKS:
            self.drinks.remove(self.sold_item)
        elif self.sold_item in self.PARTS2:
            self.car_parts.remove(self.sold_item)
        elif self.sold_item in self.TOOLS2:
            self.tools.remove(self.sold_item)
        elif self.sold_item == "Ammo":
            self.ammo -= 10
        self.money += round(self.MASTER_LIST[self.sold_item] // 2)
        self.player_sell.remove(self.sold_item)
        self.update_text()
        self.create_trader_sellbox()
    def listbox_bought_item(self, event):
        # Gets current selection from listbox
        try:
            self.buy_confirm_button.destroy()
            self.sell_confirm_button.destroy()
        except:
            None
        finally:
            self.bought_item = (self.buy_box.get(self.buy_box.curselection()))
            self.buy_confirm_button = Button(self.trader_window, text=f"Buy {self.bought_item} for ${self.MASTER_LIST[self.bought_item]}?", command=self.buy_item,
                                             font=10)
            self.buy_confirm_button.grid(column=3, row=1)

    def buy_item(self):
        self.no_health_loss = True
        if self.money >= self.MASTER_LIST[self.bought_item]:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("sell1.ogg"))
            self.buy_box.destroy()
            self.buy_confirm_button.destroy()
            if self.bought_item in self.FOOD_FOREST or self.bought_item in self.FOOD:
                self.food.append(self.bought_item)
            elif self.bought_item in self.MEDS:
                self.meds.append(self.bought_item)
            elif self.bought_item in self.DRINKS:
                self.drinks.append(self.bought_item)
            elif self.bought_item in self.PARTS2:
                self.car_parts.append(self.bought_item)
            elif self.bought_item in self.TOOLS2:
                self.tools.append(self.bought_item)
            self.trader_buy_list.remove(self.bought_item)
            self.money -= self.MASTER_LIST[self.bought_item]
            self.update_text()
            self.create_trader_buybox()
        else:
            messagebox.showinfo("Not Enough Money", "You do not have enough money.")


        # Variable to hold on to which radio button value is checked.

    def close_trader(self):

        self.trader_window.destroy()
        GameStats.create_middle_buttons(self)

    def create_middle_buttons(self):
        if self.location_player == graphics.forest and "Dirty Water" not in self.drinks:
            self.drinks.append("Dirty Water")
            self.no_health_loss = True
            self.update_text()
        self.no_health_loss = False
        self.next_day_button = Button(self.canvas_bottom, text="Next Day", command=self.end_day,
                                      font=('Helvetica 20 bold'))
        self.next_day_button.grid(column=1, row=1, padx=50, pady=50)
        self.version_label = Label(self.canvas_bottom, text="Version 0.8.9.2\nDeeksoft ©2023 ", fg="red", bg="black",
                                   font=("Courier", 10))
        self.version_label.grid(column=2, row=4)
        if self.times_looted < 3:
            self.scavenge_button = Button(self.canvas_bottom, text="Scavenge", font=('Helvetica 19 bold'), width=15,
                                          command=self.scavenge)
            self.scavenge_button.grid(column=2, row=3)
        self.eat_button = Button(self.canvas_bottom, text="Eat", font=('Helvetica 19 bold'), width=15,
                                 command=self.food_buttons)
        self.eat_button.grid(column=0, row=2)
        self.drink_button = Button(self.canvas_bottom, text="Drink", font=('Helvetica 19 bold'), width=15,
                                   command=self.drink_buttons)
        self.drink_button.grid(column=0, row=3)
        if self.location_player == graphics.Scav_Camp:
            self.trader_button = Button(self.canvas_bottom, text="Visit Trader", font=('Helvetica 19 bold'), width=15,
                                        command=self.trader)
            self.trader_button.grid(column=1, row=2)
        self.travel_button = Button(self.canvas_bottom, text="Travel", font=('Helvetica 19 bold'), width=15,
                                    command=self.travel)
        self.travel_button.grid(column=2, row=2)
        self.heal_button = Button(self.canvas_bottom, text="Heal", font=('Helvetica 19 bold'), width=15,
                                  command=self.med_buttons)
        self.heal_button.grid(column=1, row=4)
        if self.location_player == graphics.start_logo:
            self.repair_car_button = Button(self.canvas_bottom, text="Repair car", font=('Helvetica 19 bold'), width=15,
                                            command=self.repair_car)
            self.repair_car_button.grid(column=1, row=3)
            self.diagnose_car_button = Button(self.canvas_bottom, text="Diagnose Car", font=('Helvetica 19 bold'), width=15, command=self.diagnose_car)
            self.diagnose_car_button.grid(column=1, row=2)

    def delete_buttons(self):
        self.trader_button.destroy()
        self.scavenge_button.destroy()
        self.travel_button.destroy()
        self.next_day_button.destroy()
        self.eat_button.destroy()
        self.drink_button.destroy()
        self.heal_button.destroy()
        self.version_label.destroy()
        if self.location_player == graphics.start_logo:
            try:
                self.repair_car_button.destroy()
                self.diagnose_car_button.destroy()
            except:
                None

    def create_center_window(self):
        self.trader_window = Frame(self.canvas_bottom, bg="#113826")
        self.trader_window.grid(column=0, row=0)

    def check_dirty_water_inventory(self):
        if self.location_player != graphics.forest:
            try:
                self.drinks.remove("Dirty Water")
            except:
                None

    def travel(self):
        GameStats.delete_buttons(self)
        GameStats.create_center_window(self)
        self.button = Button(self.trader_window, text="Exit Travel", command=self.close_trader, font=22)
        self.button.grid(column=2, row=0)
        self.big_city_button = Button(self.trader_window, text=graphics.big_city, command=self.big_city,
                                      font=("Courier", 6), fg="green", bg="black")
        self.big_city_button.grid(column=0, row=1)
        self.forest_button = Button(self.trader_window, text=graphics.forest, command=self.forest, font=("Courier", 6),
                                    fg="green", bg="black", width=75, height=20)
        self.forest_button.grid(column=1, row=1)
        self.garage_button = Button(self.trader_window, text=graphics.start_logo, command=self.garage,
                                    font=("Courier", 5), fg="green", bg="black", width=88)
        self.garage_button.grid(column=0, row=2)
        self.scav_town_button = Button(self.trader_window, text=graphics.Scav_Camp, command=self.scav_town,
                                       font=("Courier", 7), fg="green", bg="black", width=75, height=13)
        self.scav_town_button.grid(column=1, row=2)
        travel_text = Label(self.trader_window, text="Where do you want to travel?", font=("Courier", 20), fg="white",
                            bg="black")
        travel_text.grid(column=1, row=0, pady=15)
        self.junk_yard_button = Button(self.trader_window, text=graphics.junkyard, command=self.junk_yard,
                                       font=("Courier", 5), fg="green", bg="black", width=84, height=20)
        self.junk_yard_button.grid(column=2, row=2)
        self.hospital_button = Button(self.trader_window, text=graphics.hospital, command=self.hospital,
                                      font=("Courier", 5), fg="green", bg="black", width=84, height=20)
        self.hospital_button.grid(column=2, row=1)
        if self.location_player == graphics.big_city:
            self.big_city_button.config(fg="red")
        elif self.location_player == graphics.Scav_Camp:
            self.scav_town_button.config(fg="red")
        elif self.location_player == graphics.hospital:
            self.hospital_button.config(fg="red")
        elif self.location_player == graphics.forest:
            self.forest_button.config(fg="red")
        elif self.location_player == graphics.junkyard:
            self.junk_yard_button.config(fg="red")
        elif self.location_player == graphics.start_logo:
            self.garage_button.config(fg="red")
        self.LOCATIONS = [self.big_city_button, self.forest_button, self.garage_button, self.scav_town_button,
                          self.junk_yard_button, self.hospital_button]

    def forest(self):
        if self.location_player == graphics.forest:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            if "Dirty Water" not in self.drinks:
                self.drinks.append("Dirty Water")
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.forest_button.config(fg="red")
            self.location_player = graphics.forest
            self.location_pic.config(text=self.location_player, font=("Courier", 8))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()

    def big_city(self):
        if self.location_player == graphics.big_city:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.big_city_button.config(fg="red")
            self.location_player = graphics.big_city
            self.location_pic.config(text=self.location_player, font=("Courier", 5))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()
            if random.randint(1, 100) <= 30:
                self.check_event()

    def garage(self):
        if self.location_player == graphics.start_logo:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.garage_button.config(fg="red")
            self.location_player = graphics.start_logo
            self.location_pic.config(text=self.location_player, font=("Courier", 4))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()

    def scav_town(self):
        if self.location_player == graphics.Scav_Camp:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.scav_town_button.config(fg="red")
            self.location_player = graphics.Scav_Camp
            self.location_pic.config(text=self.location_player, font=("Courier", 10))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()

    def junk_yard(self):
        if self.location_player == graphics.junkyard:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.junk_yard_button.config(fg="red")
            self.location_player = graphics.junkyard
            self.location_pic.config(text=self.location_player, font=("Courier", 5))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()

    def hospital(self):
        if self.location_player == graphics.hospital:
            messagebox.showerror('Travel Error', 'You are currently here already')
        else:
            GameStats.reset_color_green(self)
            self.times_looted = 0
            self.hospital_button.config(fg="red")
            self.location_player = graphics.hospital
            self.location_pic.config(text=self.location_player, font=("Courier", 5))
            self.energy -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.hunger -= random.randint(10, 20)
            self.check_dirty_water_inventory()
            self.update_text()

    def check_event(self):
        self.trader_window.destroy()
        self.create_center_window()
        self.test_event = Label(self.trader_window, text="You stumble upon the sound of a distant airplane flying overhead.\n"
                                                         "Moments later, you hear the unmistakable sound of an air drop being\n"
                                                         "deployed nearby. Excited at the prospect of finding useful supplies,\n"
                                                         " you head towards the location of the air drop, only to find that you are not alone.", fg="white", bg="black", font=('Helvetica 18 bold'))
        self.test_event.grid(column=0, row=0, pady=20, padx=20)
        button = Button(self.trader_window, text="Exit", command=self.close_trader, font=18)
        button.grid(column=0, row=2)
        self.test_info = Label(self.trader_window, text="This is a test event. It is not finished yet, Just exit", fg="red", bg="black", font=("Courier", 14))
        self.test_info.grid(column=0, row=1)


    def health_check(self):
        if self.no_health_loss == False:
            if self.thirst <= 0:
                self.thirst = 0
                self.health -= random.randint(10, 25)
            if self.hunger <= 0:
                self.hunger = 0
                self.health -= random.randint(10, 25)

    def reset_color_green(self):
        for location in self.LOCATIONS:
            location.config(fg="green")

    def scavenge(self):
        self.times_looted += 1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("rummage1.ogg"))
        self.energy -= random.randint(10, 30)
        self.hunger -= random.randint(5, 10)
        self.thirst -= random.randint(10, 15)
        loot = []
        # Loot table for each location
        if self.location_player == graphics.Scav_Camp:
            things_looted = random.randint(1, 130)
            if things_looted <= 25:
                drink_looted = random.randint(1, 2)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.config(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.config(text=f"Food: {len(self.food)}")
            elif 50 <= things_looted < 70:
                loot = self.random_food_drink(2, 2)
            elif 70 <= things_looted < 87:
                loot = random.choice(self.TOOLS)
                self.tools.append(loot)
                self.TOOLS.remove(loot)
            elif 87 <= things_looted < 100:
                loot = random.choice(self.PARTS)
                self.car_parts.append(loot)
                self.PARTS.remove(loot)
            elif 100 < things_looted <= 130:
                loot = "Nothing"

        elif self.location_player == graphics.start_logo:
            things_looted = random.randint(1, 115)
            if things_looted <= 25:
                drink_looted = random.randint(1, 2)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.config(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.config(text=f"Food: {len(self.food)}")
            elif 50 <= things_looted < 60:
                loot = random.choice(self.TOOLS)
                self.tools.append(loot)
                self.TOOLS.remove(loot)
            elif 60 <= things_looted < 70:
                loot = (self.random_food_drink(1, 1))
                loot1 = random.choice(self.PARTS)
                loot.append(loot1)
                self.car_parts.append(loot1)
                self.PARTS.remove(loot1)
            elif 70 <= things_looted < 83:
                loot = self.random_food_drink(2, 2)
            elif 83 <= things_looted <= 115:
                loot = "Nothing"

        elif self.location_player == graphics.big_city:
            things_looted = random.randint(1, 170)
            if things_looted <= 25:
                drink_looted = random.randint(1, 3)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.config(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.config(text=f"Food: {len(self.food)}")
            elif 50 <= things_looted < 75:
                loot = random.choice(self.TOOLS)
                self.tools.append(loot)
                self.TOOLS.remove(loot)
            elif 75 <= things_looted < 85:
                loot = random.choice(self.PARTS)
                self.car_parts.append(loot)
                self.PARTS.remove(loot)
            elif 85 <= things_looted < 100:
                loot = random.choice(self.MEDS)
                self.meds.append(loot)
            elif 100 <= things_looted <= 130:
                loot = self.random_food_drink(2, 2)
            elif 131 <= things_looted <= 170:
                loot = "Nothing"

        elif self.location_player == graphics.forest:
            things_looted = random.randint(1, 120)
            if things_looted <= 30:
                drink_looted = random.randint(1, 2)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.config(text=f"Drinks: { len(self.drinks)}")
            elif 30 < things_looted < 60:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD_FOREST)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.config(text=f"Food: {len(self.food)}")
            elif 60 <= things_looted <= 90:
                loot = self.random_food_drink(2, 2)
            elif 91 <= things_looted <= 120:
                loot = "Nothing"

        elif self.location_player == graphics.hospital:
            things_looted = random.randint(1, 100)
            if things_looted <= 20:
                drink_looted = random.randint(1, 3)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.config(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                meds_looted = (random.randint(1, 3))
                for _ in range(0, meds_looted):
                    random_loot = random.choice(self.MEDS)
                    self.meds.append(random_loot)
                    loot.append(random_loot)
                self.food_text.config(text=f"Food: {len(self.food)}")
            elif 50 <= things_looted < 75:
                loot = self.random_food_drink(2, 2)
            elif 75 <= things_looted <= 100:
                meds_looted = (random.randint(1, 3))
                for _ in range(0, meds_looted):
                    loot = (self.random_food_drink(2, 2))
                    random_loot = random.choice(self.MEDS)
                    loot.append(random_loot)
                    self.meds.append(random_loot)
                loot = "Nothing"


        elif self.location_player == graphics.junkyard:
            things_looted = random.randint(1, 100)
            if things_looted <= 20:
                loot = random.choice(self.PARTS)
                self.car_parts.append(loot)
                self.PARTS.remove(loot)
            elif 21 < things_looted < 37:
                loot = random.choice(self.TOOLS)
                self.tools.append(loot)
                self.TOOLS.remove(loot)
            elif 37 <= things_looted <= 50:
                loot = self.random_food_drink(1, 2)
            elif 51 <= things_looted <= 100:
                loot = "Nothing"

        GameStats.create_center_window(self)
        GameStats.delete_buttons(self)
        if 1 == random.randint(1, 2):
            self.found_ammo = True
            self.ammo_found = random.randint(1, 5)
            self.money_found = random.randint(1, 20)
            self.ammo += self.ammo_found
            self.money += self.money_found
        else:
            self.found_ammo = False
        loot = str(loot)
        loot = loot.replace('[', '').replace(']', '').replace("'", "")
        if self.found_ammo:
            loot_gained = Label(self.trader_window,
                                text=f"You have found {loot}\n{self.ammo_found} bullet(s), and ${self.money_found}",
                                font=("Courier", 20), fg="white", bg="black")
        else:
            loot_gained = Label(self.trader_window, text=f"You have found {loot}", font=("Courier", 20), fg="white",
                                bg="black")
        loot_gained.grid(column=0, row=0)
        button = Button(self.trader_window, text="Alright", command=self.close_trader, font=50, width=15)
        button.grid(column=0, row=1, pady=12)
        GameStats.game_over(self)
        GameStats.update_text(self)

    def random_food_drink(self, amount_food, amount_drink):
        loot = []
        food_looted = (random.randint(1, amount_food))
        for _ in range(0, food_looted):
            random_loot = random.choice(self.FOOD)
            self.food.append(random_loot)
            loot.append(random_loot)
        drink_looted = random.randint(1, amount_drink)
        for _ in range(0, drink_looted):
            random_loot = random.choice(self.DRINKS)
            self.drinks.append(random_loot)
            loot.append(random_loot)
        return loot

    def update_text(self):
        GameStats.health_check(self)
        # Updating Hunger,Thirst,Energy,Days
        hunger_color = self.color_change.hunger_change(self.hunger)
        energy_color = self.color_change.energy_change(self.energy)
        thirst_color = self.color_change.thirst_change(self.thirst)
        health_color = self.color_change.health_change(self.health)
        self.thirst_number.config(text=f"Thirst: {self.thirst}", fg=thirst_color)
        self.hunger_number.config(text=f"Hunger: {self.hunger}", fg=hunger_color)
        self.energy_number.config(text=f"Energy: {self.energy}", fg=energy_color)
        self.health_number.config(text=f"Health: {self.health}", fg=health_color)
        self.days_number.config(text=f"Days Left: {self.days_left}")
        self.ammo_have.config(text=f"Ammo: {self.ammo}")
        self.money_number.config(text=f"Money: ${self.money}")
        self.food_text.config(text=f"Food: {len(self.food)}")
        self.drinks_text.config(text=f"Drinks: {len(self.drinks)}")
        self.meds_text.config(text=f"Meds: {len(self.meds)}")

        GameStats.game_over(self)
        if len(self.tools) == 0:
            self.tools_owned.config(text=f"Tools: None", fg="white", font=('Helvetica 18 bold'))
        else:
            tools_formatted = str(self.tools)
            tools_formatted = tools_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.tools_owned.config(text=f"Tools: {tools_formatted}")
        if len(self.car_parts) == 0:
            self.car_parts_text.config(text=f"Car Parts: None")
        else:
            car_parts_formatted = str(self.car_parts)
            car_parts_formatted = car_parts_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.car_parts_text.config(text=f"Car Parts: {car_parts_formatted}")

    def game_over(self):
        if self.health <= 0 or self.days_left == -1:
            loot = str(self.parts_missing)
            loot = loot.replace('[', '').replace(']', '').replace("'", "")
            if self.days_left == -1:
                retry_button = Button(self.trader_window, text="Restart Game", command=self.restart_game, font=('Helvetica 20 bold'))
                retry_button.grid(column=0, row=1)
                exit_info = Label(self.canvas_bottom, text=f"You ran out of time and had the {loot} left to install.", bg="#113826",
                                     font=('Helvetica 20 bold'), fg="white")
                exit_info.grid(column=0, row=3)
            else:
                exit_info = Label(self.canvas_bottom, text=f"You died, you still had the {loot} left to install",font=('Helvetica 20 bold'), bg="#113826", fg="white")
                exit_info.grid(column=0, row=3)
            self.health_number.config(text=f"Health: 0", fg="red")
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("death1.ogg"))
            try:
                self.trader_window.destroy()
            finally:
                GameStats.delete_buttons(self)
                self.days_number.config(text="You Lose")
                exit_button = Button(self.canvas_bottom, text="Close Game", command=self.exit_game,
                                     font=('Helvetica 20 bold'))
                exit_button.grid(column=0, row=0)
                retry_button = Button(self.canvas_bottom, text="Restart Game", command=self.restart_game,
                                      font=('Helvetica 20 bold'))
                retry_button.grid(column=0, row=1)
            try:
                GameStats.close_trader(self)
                GameStats.delete_buttons(self)
            except:
                None
        if self.energy <= 0:
            messagebox.showinfo("Exhausted", "You passed out and awake groggy the next day.")
            GameStats.exhausted(self)
        if self.hunger > 80 and self.thirst > 80:
            self.health += 10
            if self.health > 100:
                self.health = 100

    def restart_game(self):
        self.window.destroy()
        GameStats()

    def diagnose_car(self):
        self.delete_buttons()
        self.create_center_window()
        loot = str(self.parts_missing)
        loot = loot.replace('[', '').replace(']', '').replace("'", "")
        car_text = Label(self.trader_window, text=f"Missing parts\n{loot}", font=("Courier", 14),
                         fg="green", bg="black")
        car_text.grid(column=0, row=0)
        button = Button(self.trader_window, text="Exit", command=self.close_trader, font=18)
        button.grid(column=0, row=1)

    def repair_car(self):
        if len(self.tools) >= 4 and len(self.car_parts) >= 1:
            self.create_center_window()
            button = Button(self.trader_window, text="Exit", command=self.close_trader, font=18)
            button.grid(column=0, row=1)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("repair1.mp3"))
            self.delete_buttons()
            repaired_car_text = Label(self.trader_window, text=f"You installed the {self.car_parts[0]}",
                                      font=("Courier", 14), fg="green", bg="black")
            repaired_car_text.grid(column=0, row=0)
            self.parts_missing.remove(self.car_parts[0])
            self.car_parts.remove(self.car_parts[0])
            self.energy -= random.randint(10, 30)
            self.hunger -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.no_health_loss = False
            self.update_text()
            self.game_over()
            if len(self.parts_missing) == 0:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("car_start.mp3"))
                self.days_number.config(text="You are Winner!!")
                retry_button = Button(self.canvas_bottom, text="Restart Game", command=self.restart_game,
                                      font=('Helvetica 20 bold'))
                retry_button.grid(column=0, row=1)
                try:
                    GameStats.close_trader(self)
                    GameStats.delete_buttons(self)
                except:
                    None
        else:
            messagebox.showinfo("Do not have all 4 tools", "You need all 4 tools or do not have a car part.")
