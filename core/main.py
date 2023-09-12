import json
from . import skill
from . import audio

with open("settings.json", "r") as f:
    settings = json.load(f)
    battling = settings["battling"]


class Human:
    def __init__(self, ch_name):
        self.ch_type = "Human"
        self.ch_name = ch_name
        self.__ch_rel = {}
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound="pop"):
        print(text)
        self.ac.play_sfx(sound)

    def move(self, direction):
        self.__print_sfx(f"{self.ch_name} moved {direction}.")

    def speak(self, words="Hi!", target=None):
        if target:
            self.__print_sfx(f'{self.ch_name} talks to {target.ch_name}: "{words}"')
            self.increase_rel(target.ch_name)
            target.increase_rel(self.ch_name)
        else:
            self.__print_sfx(f'{self.ch_name} said "{words}"')

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
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound="pop"):
        print(text)
        self.ac.play_sfx(sound)

    def move(self, direction):
        self.__print_sfx(f"{self.ch_name} moved {direction}.")

    def speak(self, words=None):
        self.__print_sfx(f'{self.ch_name} said "WAAHHHHHGHHHH!!!"')


class Warrior:
    def __init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk):
        # r for remaining.
        self._ch_hp = ch_hp
        self._ch_mp = ch_mp
        self.ch_hp_r = self._ch_hp
        self.ch_mp_r = self._ch_mp
        # i for initial. it will be extra added in each class.
        self._ch_atk_i = ch_atk
        self._ch_def_i = ch_def
        self._ch_acc_i = ch_acc
        self._ch_luk_i = ch_luk
        self.ch_atk = self._ch_atk_i
        self.ch_def = self._ch_def_i
        self.ch_acc = self._ch_acc_i
        self.ch_luk = self._ch_luk_i
        self.isPoison = False
        self.isBurn = False
        self.isStun = False
        self.poison_count = 0
        self.burn_count = 0
        self.stun_count = 0
        self.__sk_attack = skill.Attack(self)
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound="pop"):
        print(text)
        self.ac.play_sfx(sound)

    def __generate_bar(self, max_value, value):
        bar = round((value * 20) / max_value)
        space = round(20 - bar)
        bar_str = "|" + "◼" * bar + "·" * space + "|"
        return bar_str

    def show_init_status(self):
        print(f"{f' {self.ch_name} : {self.ch_class} ':=^25}")
        print("HP:  ", round(self._ch_hp, 2))
        print("MP:  ", round(self._ch_mp, 2))
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
        effects_list = []
        emoji_count = 0
        if self.isPoison == True: 
            effects_list.append("👿")
            emoji_count += 1
        if self.isBurn == True: 
            effects_list.append("🔥")
            emoji_count += 1
        if self.isStun == True: 
            effects_list.append("🌀")
            emoji_count += 1
        if effects_list: title = f"{name} {''.join(effects_list)}"
        else: title = name
        return title, emoji_count


    def get_hp_bar(self):
        bar_str = self.__generate_bar(self._ch_hp, self.ch_hp_r)
        if self.ch_hp_r > 0:
            return f"HP: {bar_str} {self.ch_hp_r}/{self._ch_hp}"
        else:
            return f"X {self.ch_name} is inactive."

    def get_mp_bar(self):
        bar_str = self.__generate_bar(self._ch_mp, self.ch_mp_r)
        if self.ch_hp_r > 0:
            return f"MP: {bar_str} {self.ch_mp_r}/{self._ch_mp}"
        else:
            return ""
        
    def effects_turn_trigger(self):
        poison_dec_value = battling["hp_dec"]["poison_dec"]
        burn_dec_value = battling["hp_dec"]["burn_dec"]
        check = []
        if self.ch_hp_r > 0:
            if self.isPoison == True:
                check.append(True)
                self.ch_hp_r = round(self.ch_hp_r - poison_dec_value, 2)
                print(f"- {self.ch_name} is poisoned 👿-{poison_dec_value}")
                if self.ch_hp_r < 0:
                    self.ch_hp_r = 0
                self.poison_count -= 1
                if self.poison_count <= 0:
                    self.poison_count = 0
                    self.isPoison = False
            else:
                check.append(False)
            if self.isBurn == True:
                check.append(True)
                self.ch_hp_r = round(self.ch_hp_r - burn_dec_value, 2)
                print(f"- {self.ch_name} is burned 🔥-{burn_dec_value}")
                if self.ch_hp_r < 0:
                    self.ch_hp_r = 0
                self.burn_count -= 1
                if self.burn_count <= 0:
                    self.burn_count = 0
                    self.isBurn = False
            else:
                check.append(False)
            if self.isStun == True:
                print(f"- {self.ch_name} is stunned 🌀")
                if self.stun_count <= 0:
                    self.stun_count = 0
                    self.isStun = False
        else:
            self.isBurn = False
            self.isPoison = False
            self.isStun = False
        return any(check)

    def attack(self, target):
        result = self.__sk_attack.attack(target)
        return result