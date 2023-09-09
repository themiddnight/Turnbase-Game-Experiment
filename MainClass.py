import random
import json

with open("settings.json", "r") as f:
    settings = json.load(f)
    battling = settings["battling"]


class Human:
    def __init__(self, ch_name):
        self.ch_type = "Human"
        self.ch_name = ch_name
        self.__ch_rel = {}

    def move(self, direction):
        print(f"{self.ch_name} moved {direction}.")

    def speak(self, words="Hi!", target=None):
        if target:
            print(f'{self.ch_name} talks to {target.ch_name}: "{words}"')
            self.increase_rel(target.ch_name)
            target.increase_rel(self.ch_name)
        else:
            print(f'{self.ch_name} said "{words}"')

    def increase_rel(self, name):
        if name not in self.__ch_rel:
            self.__ch_rel[name] = 0
        self.__ch_rel[name] += 1

    def get_relationship(self):
        return self.__ch_rel


class Monster:
    def __init__(self, ch_name):
        self.ch_type = "Monster"
        self.ch_name = ch_name

    def move(self, direction):
        print(f"{self.ch_name} moved {direction}.")

    def speak(self, words=None):
        print(f'{self.ch_name} said "WAAHHHHHGHHHH!!!"')


class Warrior:
    def __init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk):
        # r for remaining.
        self.ch_hp = ch_hp
        self.ch_hp_r = self.ch_hp
        self.ch_mp = ch_mp
        self.ch_mp_r = self.ch_mp
        # i for initial. it will be extra added in each class.
        self.ch_atk_i = ch_atk
        self.ch_def_i = ch_def
        self.ch_acc_i = ch_acc
        self.ch_luk_i = ch_luk
        self.ch_atk = self.ch_atk_i
        self.ch_def = self.ch_def_i
        self.ch_acc = self.ch_acc_i
        self.ch_luk = self.ch_luk_i
        self.poisoned = False
        self.burned = False
        self.stunned = False
        self.poisoned_count = 0
        self.burned_count = 0
        self.stunned_count = 0
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5

    def __generate_bar(self, max_value, value):
        bar = round((value * 20) / max_value)
        space = round(20 - bar)
        bar_str = "|" + "◼" * bar + "·" * space + "|"
        return bar_str

    def show_init_status(self):
        print(f"{f' {self.ch_name} : {self.ch_class} ':=^25}")
        print("HP:  ", round(self.ch_hp, 2))
        print("MP:  ", round(self.ch_mp, 2))
        print("ATK: ", round(self.ch_atk, 2))
        print("DEF: ", round(self.ch_def, 2))
        print("ACC: ", round(self.ch_acc * 100), "%")
        print("LUK: ", round(self.ch_luk * 100), "%")
        print()

    def get_title(self):
        """
        Return [Title, Symbol counts]\n
        emoji_char_count:
            - 'ljust' doesn't detect the emoji characters. 
            So we need to get the count of it to subtract the ljust when printed.
        """
        name = f"{self.ch_name} - {self.ch_class}"
        status_list = []
        emoji_char_count = 0
        if self.poisoned == True: 
            status_list.append("👿")
            emoji_char_count += 1
        if self.burned == True: 
            status_list.append("🔥")
            emoji_char_count += 1
        if self.stunned == True: 
            status_list.append("🌀")
            emoji_char_count += 1
        if status_list: title = f"{name} {''.join(status_list)}"
        else: title = name
        return title, emoji_char_count


    def get_hp_bar(self):
        bar_str = self.__generate_bar(self.ch_hp, self.ch_hp_r)
        if self.ch_hp_r > 0:
            return f"HP: {bar_str} {self.ch_hp_r}/{self.ch_hp}"
        else:
            return f"X {self.ch_name} is inactive."

    def get_mp_bar(self):
        bar_str = self.__generate_bar(self.ch_mp, self.ch_mp_r)
        if self.ch_hp_r > 0:
            return f"MP: {bar_str} {self.ch_mp_r}/{self.ch_mp}"
        else:
            return ""
        
    def turn_trigger(self):
        poison_dec_value = battling["hp_dec"]["poison_dec"]
        burn_dec_value = battling["hp_dec"]["burn_dec"]
        check = []
        if self.ch_hp_r > 0:
            if self.poisoned == True:
                check.append(True)
                self.ch_hp_r = round(self.ch_hp_r - poison_dec_value, 2)
                print(f"- {self.ch_name} is poisoned 👿-{poison_dec_value}")
                if self.ch_hp_r < 0:
                    self.ch_hp_r = 0
                self.poisoned_count -= 1
                if self.poisoned_count <= 0:
                    self.poisoned_count = 0
                    self.poisoned = False
            else:
                check.append(False)
            if self.burned == True:
                check.append(True)
                self.ch_hp_r = round(self.ch_hp_r - burn_dec_value, 2)
                print(f"- {self.ch_name} is burned 🔥-{burn_dec_value}")
                if self.ch_hp_r < 0:
                    self.ch_hp_r = 0
                self.burned_count -= 1
                if self.burned_count <= 0:
                    self.burned_count = 0
                    self.burned = False
            else:
                check.append(False)
            if self.stunned == True:
                if self.stunned_count <= 0:
                    self.stunned_count = 0
                    self.stunned = False
        else:
            self.burned = False
        return any(check)

    def attack(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if target.ch_hp_r > 0:
                critical = random.random() < self.__critical_factor
                acc_factor = random.uniform(self.ch_acc, 1)
                attack = self.ch_atk / (target.ch_def * 0.5)
                if acc_factor > 0.4:
                    attack = round(attack * acc_factor, 2)
                    if critical:
                        attack = round(attack * 1.5, 2)
                else:
                    attack = 0
                target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                if target.ch_hp_r < 0:
                    target.ch_hp_r = 0
                # print action
                if attack:
                    if critical:
                        self.speak("Bring it on!!")
                        print((f"- {self.ch_name} attacks "
                               f"{target.ch_name} 💥{attack} !"))
                    else:
                        print((f"- {self.ch_name} attacks " f"{target.ch_name} 🔪{attack}"))
                else:
                    print(f"- {self.ch_name} missed 💨")
                    self.speak("Crap!!")
                return True
            else:
                print((f"- {target.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True