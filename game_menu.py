import random
from tkinter import *
import sys
import pygame
import graphics
from tkinter import messagebox
from graphics import Scav_Camp
from graphics import trader
from status_check import color_changer
from customtkinter import CTk, CTkButton, CTkFrame, CTkCanvas, CTkLabel, CTkFont, CTkCheckBox, CTkScrollbar, CTkComboBox, CTkTextbox, CTkScrollableFrame

MAX_DAYS = 14
STARTING_MONEY = random.randint(85, 150)
STARTING_HUNGER = 100
STARTING_THIRST = 100
STARTING_HEALTH = 100
STARTING_ENERGY = 100
Font_tuple = ("Helvetica", 30, "bold")
Font_tuple_button = ("Helvetica", 40, "bold")
STARTING_LOCATION = Scav_Camp
pygame.mixer.init()


class GameStats:
    def __init__(self):
        # Define game variables
        self.trader_buy_list = None
        self.window = CTk(fg_color="black")
        self.window.iconbitmap("favicon.ico")
        self.window.title("Deekokolypse")
        self.color_change = color_changer()
        self.times_looted = 0
        self.height = self.window.winfo_screenheight()
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
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
        if self.height < 800:
            self.canvas_bottom = CTkScrollableFrame(self.window, border_color="White", fg_color="#113826", border_width=3, corner_radius=0, orientation="vertical")
            self.canvas_bottom.grid(row=1, column=0, columnspan=3, sticky="nswe")

        else:
            self.canvas_bottom = CTkFrame(self.window, border_color="White", fg_color="#113826", border_width=3)
            self.canvas_bottom.grid(row=1, column=1, sticky='')
            self.canvas_bottom.grid_columnconfigure(0, weight=1)
        self.canvas_top = CTkFrame(self.window, border_color="White", border_width=4, fg_color="#245953")
        self.canvas_text = CTkFrame(self.window, fg_color="#2D2727", border_width=4, border_color="White")
        self.canvas_text_middle = CTkFrame(self.window, fg_color="black", border_width=2, border_color="red")



        self.canvas_text.grid(row=0, column=0, sticky='')
        self.canvas_top.grid(row=0, column=2, padx=(50, 0), pady=(0, 50), sticky='e')
        self.canvas_text_middle.grid(row=0, column=1, sticky='')
        self.health_number = CTkLabel(self.canvas_text, text=f"Health: {self.health}",
                                   font=Font_tuple)
        self.health_number.grid(column=0, row=0, padx=(15,0), pady=26, sticky='')
        self.hunger_number = CTkLabel(self.canvas_text, text=f"Hunger: {self.hunger}",
                                   font=Font_tuple)
        self.hunger_number.grid(column=0, row=1, padx=(15,0), pady=26, sticky='')
        self.ammo_have = CTkLabel(self.canvas_text, text=f"Ammo: {self.ammo}",
                               font=Font_tuple)
        self.ammo_have.grid(column=0, row=3, columnspan=1, pady=26, sticky='')
        self.money_number = CTkLabel(self.canvas_text, text=f"Money: ${self.money}",
                                  font=Font_tuple)
        self.money_number.grid(column=1, row=3, padx=15, pady=26, sticky='')
        self.thirst_number = CTkLabel(self.canvas_text, text=f"Thirst: {self.thirst}",
                                   font=Font_tuple)
        self.thirst_number.grid(column=1, row=1, padx=15, pady=26)
        self.energy_number = CTkLabel(self.canvas_text, text=f"Energy: {self.energy}",
                                   font=Font_tuple)
        self.energy_number.grid(column=1, row=0, padx=15, pady=26)
        self.days_number = CTkLabel(self.canvas_text_middle, text=f"Days Left: {self.days_left}",
                                 font=Font_tuple)
        self.days_number.grid(column=3, row=0, pady=(0, 120), padx=25)
        self.current_location = CTkLabel(self.canvas_top, text=f"Current Location:",
                                      font=("Helvetica", 25, "bold"))
        self.current_location.grid(column=1, row=6, padx=10)
        self.location_pic = CTkLabel(self.canvas_top, text=self.location_player,
                                  font=("Courier", 10))
        self.location_pic.grid(column=1, row=5, pady=30, padx=30)
        self.checked_state = IntVar()
        self.mute_button = CTkCheckBox(self.canvas_top, text="Mute Sound?", variable=self.checked_state,
                                       command=self.play)
        self.mute_button.grid(column=1, row=3, pady=(10, 0))
        if len(self.tools) == 0:
            self.tools_owned = CTkLabel(self.canvas_top, text=f"Tools: None",
                                 font=("Helvetica", 20, "bold"))
        else:
            tools_formatted = str(self.tools)
            tools_formatted = tools_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.tools_owned = CTkLabel(self.canvas_top, text=f"Tools: {tools_formatted}",
                                     font=("Helvetica", 20, "bold"), wraplength=400)
        self.tools_owned.grid(column=1, row=7, pady=20, padx=10)
        if len(self.car_parts) == 0:
            self.car_parts_text = CTkLabel(self.canvas_top, text=f"Car Parts: None",
                                        font=("Helvetica", 20, "bold"))
        else:
            self.car_parts_text = CTkLabel(self.canvas_top, text=f"Car Parts: {self.car_parts}",
                                        font=("Helvetica", 20, "bold"), wraplength=400)
        self.car_parts_text.grid(column=1, row=9, padx=10, pady=(0, 10))

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
            self.weapons_number = CTkLabel(self.canvas_top, text=f"Weapons: None",
                                        font=("Helvetica", 20, "bold"))
        else:
            weapons_formatted = str(self.weapons)
            weapons_formatted = weapons_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.weapons_number = CTkLabel(self.canvas_top, text=f"Weapons: {weapons_formatted}",
                                        font=("Helvetica", 20, "bold"))
        self.weapons_number.grid(column=1, row=8)
        self.drinks_text = CTkLabel(self.canvas_text_middle, text=f"Drinks: {len(self.drinks)}",
                                 font=Font_tuple)
        self.drinks_text.grid(column=3, row=1)
        self.food_text = CTkLabel(self.canvas_text_middle, text=f"Food: {len(self.food)}",
                               font=Font_tuple)
        self.food_text.grid(column=3, row=2)
        self.meds_text = CTkLabel(self.canvas_text_middle, text=f"Meds: {len(self.meds)}",
                               font=Font_tuple)
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
        self.eat_confirm_button = CTkButton(self.canvas_bottom, text=f"Eat {self.food_eaten}?", command=self.eat_food, font=Font_tuple)
        self.eat_confirm_button.grid(column=1, row=2, pady=20, padx=20)

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
        self.scrollbar.destroy()
        self.game_over()
        GameStats.create_middle_buttons(self)

    def food_buttons(self):
        if len(self.food) == 0:
            messagebox.showinfo("No food", "You have no food")
        else:
            GameStats.delete_buttons(self)
            self.consume_menu = CTkButton(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=Font_tuple)
            self.consume_menu.grid(column=1, row=1, pady=(0, 10))
            self.food_list = Listbox(self.canvas_bottom, height=6, width=20, font=("Arial", 20), bg="black",
                                     fg="white", highlightthickness=0)
            self.scrollbar = CTkScrollbar(self.canvas_bottom)
            self.scrollbar.grid(column=4, row=0, padx=5)
            self.scrollbar.configure(command=self.food_list.yview)
            for food_item in self.food:
                if food_item in self.food:
                    self.food_list.insert(self.food.index(food_item), food_item)
                    self.food_list.bind("<<ListboxSelect>>", self.listbox_used_food)
                    self.food_list.grid(column=1, row=0, pady=20, padx=10)
                    self.food_list.configure(yscrollcommand=self.scrollbar.set)

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
        self.scrollbar.destroy()
        GameStats.create_middle_buttons(self)

    def listbox_used_drink(self, event):
        # Gets current selection from listbox
        try:
            self.drink_confirm_button.destroy()
        except:
            None
        finally:
            self.drink_consumed = (self.drink_box.get(self.drink_box.curselection()))
            self.drink_confirm_button = CTkButton(self.canvas_bottom, text=f"Drink {self.drink_consumed}?",
                                               command=self.drink_liquid, font=Font_tuple)
            self.drink_confirm_button.grid(column=1, row=2, pady=20, padx=20)

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
            self.scrollbar.destroy()
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
            self.consume_menu = CTkButton(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=Font_tuple)
            self.consume_menu.grid(column=1, row=1, pady=(0, 10))
            self.drink_box = Listbox(self.canvas_bottom, height=6, width=20, font=("Arial", 20), bg="black",
                                     fg="white", highlightthickness=0)
            self.scrollbar = CTkScrollbar(self.canvas_bottom)
            self.scrollbar.grid(column=4, row=0, padx=5)
            self.scrollbar.configure(command=self.drink_box.yview)
            for drink_item in self.drinks:
                if drink_item in self.drinks:
                    self.drink_box.insert(self.drinks.index(drink_item), drink_item)
                    self.drink_box.bind("<<ListboxSelect>>", self.listbox_used_drink)
                    self.drink_box.grid(column=1, row=0, pady=20, padx=10)
                    self.drink_box.configure(yscrollcommand=self.scrollbar.set)

    def listbox_used_meds(self, event):
        # Gets current selection from listbox
        try:
            self.med_confirm_button.destroy()
        except:
            None
        finally:
            self.med_consumed = (self.med_box.get(self.med_box.curselection()))
            self.med_confirm_button = CTkButton(self.canvas_bottom, text=f"Use {self.med_consumed}?",
                                             command=self.use_meds, font=Font_tuple)
            self.med_confirm_button.grid(column=1, row=2, pady=20, padx=20)

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
        self.scrollbar.destroy()
        self.consume_menu.destroy()
        self.med_box.destroy()

    def med_buttons(self):
        if len(self.meds) == 0:
            messagebox.showinfo("No Meds", "You have no Meds")
        else:
            GameStats.delete_buttons(self)
            self.consume_menu = CTkButton(self.canvas_bottom, text="Exit", command=self.exit_eat_drink, font=Font_tuple)
            self.consume_menu.grid(column=1, row=1, pady=(0, 10))
            self.med_box = Listbox(self.canvas_bottom, height=4, width=20, font=("Arial", 20), bg="black",
                                   fg="white", highlightthickness=0)
            self.scrollbar = CTkScrollbar(self.canvas_bottom)
            self.scrollbar.grid(column=4, row=0, padx=5)
            self.scrollbar.configure(command=self.med_box.yview)
            for med_item in self.meds:
                if med_item in self.meds:
                    self.med_box.insert(self.meds.index(med_item), med_item)
                    self.med_box.bind("<<ListboxSelect>>", self.listbox_used_meds)
                    self.med_box.grid(column=1, row=0, pady=20, padx=10)
                    self.med_box.configure(yscrollcommand=self.scrollbar.set)

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
            button = CTkButton(self.trader_window, text="Exit Trader", command=self.close_trader, font=Font_tuple)
            button.grid(column=2, row=1, pady=(0, 10))
            trader_image = Label(self.trader_window, text=trader, font=("Courier", 4), fg="green", bg="black")
            trader_image.grid(column=2, row=0, pady=(15,50), padx=20)
            trader_text = CTkLabel(self.trader_window, text="Buy", font=("Courier", 25))
            trader_text.grid(column=3, row=1)
            if len(self.food) + len(self.drinks) + len(self.meds) + len(self.car_parts) + len(self.tools) > 0:
                trader_text2 = CTkLabel(self.trader_window, text="Sell", font=("Courier", 25))
                trader_text2.grid(column=1, row=1)
            self.create_trader_buybox()
            self.create_trader_sellbox()


    def create_trader_buybox(self):
        self.buy_box = Listbox(self.trader_window, height=8, width=20, font=("Courier", 14), bg="black",
                               fg="white", highlightthickness=0)
        scrollbar = CTkScrollbar(self.trader_window)
        scrollbar.grid(column=4, row=0, padx=5)
        scrollbar.configure(command=self.buy_box.yview)
        for item in self.trader_buy_list:
            self.buy_box.insert(self.trader_buy_list.index(item), item)
            self.buy_box.bind("<<ListboxSelect>>", self.listbox_bought_item)
            self.buy_box.grid(column=3, row=0)
            self.buy_box.configure(yscrollcommand=scrollbar.set)

    def create_trader_sellbox(self):
        self.player_sell = []
        self.sell_box = Listbox(self.trader_window, height=8, width=20, font=("Courier", 14), bg="black",fg="white", highlightthickness=0)
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
            scrollbar1 = CTkScrollbar(self.trader_window)
            scrollbar1.grid(column=0, row=0, padx=5)
            scrollbar1.configure(command=self.sell_box.yview)
        try:
            self.sell_box.configure(yscrollcommand=scrollbar1.set)
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
            self.sell_confirm_button = CTkButton(self.trader_window, text=f"Sell {self.sold_item} for ${round(self.MASTER_LIST[self.sold_item] // 2)}?",
                                                 command=self.sell_item, font=("Helvetica", 20, "bold"))
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
            self.buy_confirm_button = CTkButton(self.trader_window, text=f"Buy {self.bought_item} for ${self.MASTER_LIST[self.bought_item]}?", command=self.buy_item,
                                             font=("Helvetica", 20, "bold"))
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
        self.next_day_button = CTkButton(self.canvas_bottom, text="Next Day", command=self.end_day,
                                      font=Font_tuple_button, width=100, fg_color="#AA5656")
        self.next_day_button.grid(column=1, row=1, padx=50, pady=50)
        self.version_label = CTkLabel(self.canvas_bottom, text="Version 0.8.9.3\nDeeksoft ©2023 ", fg_color="#113826", text_color="Black",
                                   font=("Courier", 15, "bold"))
        self.version_label.grid(column=2, row=4)
        if self.times_looted < 3:
            self.scavenge_button = CTkButton(self.canvas_bottom, text="Scavenge", font=Font_tuple_button, width=175,
                                          command=self.scavenge)
            self.scavenge_button.grid(column=2, row=3, pady=10, padx=10)
        self.eat_button = CTkButton(self.canvas_bottom, text="Eat", font=Font_tuple_button, width=195,
                                 command=self.food_buttons)
        self.eat_button.grid(column=0, row=2, pady=10, padx=10)
        self.drink_button = CTkButton(self.canvas_bottom, text="Drink", width=195,
                                   command=self.drink_buttons, font=Font_tuple_button)
        self.drink_button.grid(column=0, row=3, pady=10, padx=10)
        if self.location_player == graphics.Scav_Camp:
            self.trader_button = CTkButton(self.canvas_bottom, text="Visit Trader", font=Font_tuple_button, width=195,
                                        command=self.trader)
            self.trader_button.grid(column=1, row=2, pady=10)
        self.travel_button = CTkButton(self.canvas_bottom, text="Travel", font=Font_tuple_button, width=195,
                                    command=self.travel)
        self.travel_button.grid(column=2, row=2, pady=10, padx=10)
        self.heal_button = CTkButton(self.canvas_bottom, text="Heal", font=Font_tuple_button, width=195,
                                  command=self.med_buttons)
        self.heal_button.grid(column=1, row=4, pady=15)
        if self.location_player == graphics.start_logo:
            self.repair_car_button = CTkButton(self.canvas_bottom, text="Repair car", font=Font_tuple_button, width=15,
                                            command=self.repair_car)
            self.repair_car_button.grid(column=1, row=3, pady=10)
            self.diagnose_car_button = CTkButton(self.canvas_bottom, text="Diagnose Car", font=Font_tuple_button, width=15, command=self.diagnose_car)
            self.diagnose_car_button.grid(column=1, row=2, pady=10)

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
        self.trader_window = CTkFrame(self.canvas_bottom, border_width=2, border_color="white")
        self.trader_window.grid(column=0, row=0, sticky='nwse', columnspan=4)




    def check_dirty_water_inventory(self):
        if self.location_player != graphics.forest:
            try:
                self.drinks.remove("Dirty Water")
            except:
                None

    def travel(self):
        GameStats.delete_buttons(self)
        GameStats.create_center_window(self)
        self.button = CTkButton(self.trader_window, text="Exit Travel", command=self.close_trader, font=Font_tuple)
        self.button.grid(column=2, row=0)
        self.big_city_button = CTkButton(self.trader_window, text=graphics.big_city, command=self.big_city,
                                      font=("Courier", 6),  height=150, width=350, fg_color="Black")
        self.big_city_button.grid(column=2, row=2)
        self.forest_button = CTkButton(self.trader_window, text=graphics.forest, command=self.forest, font=("Courier", 8) , height=150, width=350, fg_color="Black")
        self.forest_button.grid(column=1, row=1)
        self.garage_button = CTkButton(self.trader_window, text=graphics.start_logo, command=self.garage,
                                    font=("Courier", 5),  height=150, width=350, fg_color="Black")
        self.garage_button.grid(column=0, row=2)
        self.scav_town_button = CTkButton(self.trader_window, text=graphics.Scav_Camp, command=self.scav_town,
                                       font=("Courier", 9), height=150, width=350, fg_color="Black")
        self.scav_town_button.grid(column=1, row=2)
        travel_text = Label(self.trader_window, text="Where do you want to travel?", font=("Courier", 20))
        travel_text.grid(column=1, row=0, pady=15)
        self.junk_yard_button = CTkButton(self.trader_window, text=graphics.junkyard, command=self.junk_yard,
                                       font=("Courier", 5),  height=150, width=465, fg_color="Black")
        self.junk_yard_button.grid(column=0, row=1)
        self.hospital_button = CTkButton(self.trader_window, text=graphics.hospital, command=self.hospital,
                                      font=("Courier", 5), height=150, width=350, fg_color="Black")
        self.hospital_button.grid(column=2, row=1)
        if self.location_player == graphics.big_city:
            self.big_city_button.configure(text_color="red")
        elif self.location_player == graphics.Scav_Camp:
            self.scav_town_button.configure(text_color="red")
        elif self.location_player == graphics.hospital:
            self.hospital_button.configure(text_color="red")
        elif self.location_player == graphics.forest:
            self.forest_button.configure(text_color="red")
        elif self.location_player == graphics.junkyard:
            self.junk_yard_button.configure(text_color="red")
        elif self.location_player == graphics.start_logo:
            self.garage_button.configure(text_color="red")
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
            self.forest_button.configure(text_color="red")
            self.location_player = graphics.forest
            self.location_pic.configure(text=self.location_player, font=("Courier", 9))
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
            self.big_city_button.configure(text_color="red")
            self.location_player = graphics.big_city
            self.location_pic.configure(text=self.location_player, font=("Courier", 6))
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
            self.garage_button.configure(text_color="red")
            self.location_player = graphics.start_logo
            self.location_pic.configure(text=self.location_player, font=("Courier", 5))
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
            self.scav_town_button.configure(text_color="red")
            self.location_player = graphics.Scav_Camp
            self.location_pic.configure(text=self.location_player, font=("Courier", 10))
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
            self.junk_yard_button.configure(text_color="red")
            self.location_player = graphics.junkyard
            self.location_pic.configure(text=self.location_player, font=("Courier", 5))
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
            self.hospital_button.configure(text_color="red")
            self.location_player = graphics.hospital
            self.location_pic.configure(text=self.location_player, font=("Courier", 5))
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
        button = CTkButton(self.trader_window, text="Exit", command=self.close_trader, font=Font_tuple)
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
            location.configure(text_color="green")

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
                self.drinks_text.configure(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.configure(text=f"Food: {len(self.food)}")
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
                self.drinks_text.configure(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.configure(text=f"Food: {len(self.food)}")
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
                self.drinks_text.configure(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.configure(text=f"Food: {len(self.food)}")
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
                self.drinks_text.configure(text=f"Drinks: { len(self.drinks)}")
            elif 30 < things_looted < 60:
                food_looted = (random.randint(1, 2))
                for _ in range(0, food_looted):
                    random_loot = random.choice(self.FOOD_FOREST)
                    self.food.append(random_loot)
                    loot.append(random_loot)
                self.food_text.configure(text=f"Food: {len(self.food)}")
            elif 60 <= things_looted <= 90:
                loot = self.random_food_drink(2, 2)
            elif 91 <= things_looted <= 120:
                loot = "Nothing"

        elif self.location_player == graphics.hospital:
            things_looted = random.randint(1, 100)
            if things_looted <= 25:
                drink_looted = random.randint(1, 3)
                for _ in range(0, drink_looted):
                    random_loot = random.choice(self.DRINKS)
                    self.drinks.append(random_loot)
                    loot.append(random_loot)
                self.drinks_text.configure(text=f"Drinks: {len(self.drinks)}")
            elif 25 < things_looted < 50:
                meds_looted = (random.randint(1, 3))
                for _ in range(0, meds_looted):
                    random_loot = random.choice(self.MEDS)
                    self.meds.append(random_loot)
                    loot.append(random_loot)
                self.food_text.configure(text=f"Food: {len(self.food)}")
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
            loot_gained = CTkLabel(self.trader_window,
                                text=f"You have found {loot}\n{self.ammo_found} bullet(s), and ${self.money_found}",
                                font=("Courier", 25))
        else:
            loot_gained = CTkLabel(self.trader_window, text=f"You have found {loot}", font=("Courier", 25))
        loot_gained.grid(column=0, row=0, pady=15, padx=15)
        button = CTkButton(self.trader_window, text="Alright", command=self.close_trader, font=Font_tuple, width=15)
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
        self.thirst_number.configure(text=f"Thirst: {self.thirst}", text_color=thirst_color)
        self.hunger_number.configure(text=f"Hunger: {self.hunger}", text_color=hunger_color)
        self.energy_number.configure(text=f"Energy: {self.energy}", text_color=energy_color)
        self.health_number.configure(text=f"Health: {self.health}", text_color=health_color)
        self.days_number.configure(text=f"Days Left: {self.days_left}")
        self.ammo_have.configure(text=f"Ammo: {self.ammo}")
        self.money_number.configure(text=f"Money: ${self.money}")
        self.food_text.configure(text=f"Food: {len(self.food)}")
        self.drinks_text.configure(text=f"Drinks: {len(self.drinks)}")
        self.meds_text.configure(text=f"Meds: {len(self.meds)}")

        GameStats.game_over(self)
        if len(self.tools) == 0:
            self.tools_owned.configure(text=f"Tools: None",font=("Helvetica", 18, "bold"))
        else:
            tools_formatted = str(self.tools)
            tools_formatted = tools_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.tools_owned.configure(text=f"Tools: {tools_formatted}")
        if len(self.car_parts) == 0:
            self.car_parts_text.configure(text=f"Car Parts: None")
        else:
            car_parts_formatted = str(self.car_parts)
            car_parts_formatted = car_parts_formatted.replace('[', '').replace(']', '').replace("'", "")
            self.car_parts_text.configure(text=f"Car Parts: {car_parts_formatted}")

    def game_over(self):
        if self.health <= 0 or self.days_left == -1:
            loot = str(self.parts_missing)
            loot = loot.replace('[', '').replace(']', '').replace("'", "")
            if self.days_left == -1:
                retry_button = CTkButton(self.trader_window, text="Restart Game", command=self.restart_game, font=Font_tuple)
                retry_button.grid(column=0, row=1)
                exit_info = Label(self.canvas_bottom, text=f"You ran out of time and had the {loot} left to install.", bg="#113826",
                                     font=('Helvetica 20 bold'), text_color="white")
                exit_info.grid(column=0, row=3, pady=15, padx=10)
            else:
                exit_info = Label(self.canvas_bottom, text=f"You died, you still had the {loot} left to install",font=('Helvetica 20 bold'), bg="#113826", fg="white", wraplength=620)
                exit_info.grid(column=0, row=3, padx=10, pady=5)
            self.health_number.configure(text=f"Health: 0", text_color="red")
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("death1.ogg"))
            try:
                self.trader_window.destroy()
            finally:
                GameStats.delete_buttons(self)
                self.days_number.configure(text="You Lose")
                exit_button = CTkButton(self.canvas_bottom, text="Close Game", command=self.exit_game,
                                     font=Font_tuple)
                exit_button.grid(column=0, row=0, pady=10)
                retry_button = CTkButton(self.canvas_bottom, text="Restart Game", command=self.restart_game,
                                      font=Font_tuple)
                retry_button.grid(column=0, row=1, pady=15)
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
        button = CTkButton(self.trader_window, text="Exit", command=self.close_trader, font=Font_tuple)
        button.grid(column=0, row=1)

    def repair_car(self):
        if len(self.tools) >= 4 and len(self.car_parts) >= 1:
            if self.car_parts[0] in self.parts_missing:
                part_repaired = self.car_parts[0]
            elif self.car_parts[1] in self.parts_missing:
                part_repaired = self.car_parts[1]
            else:
                part_repaired = self.car_parts[2]
            self.create_center_window()
            button = CTkButton(self.trader_window, text="Exit", command=self.close_trader, font=Font_tuple)
            button.grid(row=1)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("repair1.mp3"))
            self.delete_buttons()
            repaired_car_text = Label(self.trader_window, text=f"You installed the {part_repaired}",
                                      font=("Courier", 14), fg="green", bg="black")
            repaired_car_text.grid(column=0, row=0)
            self.parts_missing.remove(part_repaired)
            self.car_parts.remove(part_repaired)
            if len(self.parts_missing) == 0:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("car_start.mp3"))
                self.days_number.configure(text="You are Winner!!")
                retry_button = CTkButton(self.canvas_bottom, text="Restart Game", command=self.restart_game,
                                      font=Font_tuple)
                retry_button.grid(column=0, row=1, pady=15)
                try:
                    GameStats.close_trader(self)
                    GameStats.delete_buttons(self)
                except:
                    None
            self.energy -= random.randint(10, 30)
            self.hunger -= random.randint(10, 25)
            self.thirst -= random.randint(10, 20)
            self.no_health_loss = False
            self.update_text()
            self.game_over()

        else:
            messagebox.showinfo("Do not have all 4 tools", "You need all 4 tools or do not have a car part.")
