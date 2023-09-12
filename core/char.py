"""
For "self.skill_list": {skillNumber: [skillName, skillMode, manaUsed, methodName]}
    - skillMode:
        - 0 Enemy individual
        - 1 Enemy team
        - 2 Hero individual
        - 3 Hero team
"""
import json
from . import main
from . import skill

with open("settings.json", "r") as f:
    settings = json.load(f)
    class_stats_mlp = settings["class_stats_mlp"]
    battling = settings["battling"]


class Archer(main.Human, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Human.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Archer"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Burst Shoot (3)", 0, 3, "burst_shoot"]}
        self.__sk_burst_shoot = skill.Attack(self, 
            sk_name = self.skill_list["2"][0],
            sk_mana = self.skill_list["2"][2],
            burst_count = 3,
            target_def_factor = 0.75,
            atk_word = "shoot",
            atk_icon = "🏹")

    def burst_shoot(self, target):
        result = self.__sk_burst_shoot.attack(target)
        return result
    

class Knight(main.Human, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Human.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Knight"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Hard Attack (3)", 0, 3, "hard_attack"]}
        self.__sk_hard_attack = skill.Attack(self, 
            sk_mana = self.skill_list["2"][2],
            target_def_factor = 0.3,
            target_fx = "stun",
            target_fx_count = 1,
            target_fx_prob  = 0.4,
            atk_word = "hard attack",
            atk_icon = "🔪🔪")

    def hard_attack(self, target):
        result = self.__sk_hard_attack.attack(target)
        return result


class Priest(main.Human, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Human.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Priest"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Heal (3)", 2, 3, "heal"]}
        self.__sk_heal = skill.Heal(self, 
            sk_mana = self.skill_list["2"][2],
            heal_value = 4)

    def heal(self, target):
        result = self.__sk_heal.heal(target)
        return result


class Dragon(main.Monster, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Monster.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Dragon"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Burn (4)", 1, 4, "burn"]}
        self.__sk_burn = skill.Attack(self, 
            sk_mana = self.skill_list["2"][2],
            target_def_factor = 0.4,
            target_fx = "burn",
            target_fx_count = 3,
            target_fx_prob  = 0.7,
            atk_word = "burn",
            atk_icon = "🔥🔥")

    def burn(self, target):
        result = self.__sk_burn.attack(target)
        return result


class Vampire(main.Monster, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Monster.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Vampire"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Bite (3)", 0, 3, "bite"]}
        self.__sk_bite = skill.Attack(self, 
            sk_mana = self.skill_list["2"][2],
            target_def_factor = 0.3,
            target_fx = "poison",
            target_fx_count = 4,
            target_fx_prob = 1,
            atk_word = "bite",
            atk_icon = "🧛🏻")

    def bite(self, target):
        result = self.__sk_bite.attack(target)
        return result


class Golem(main.Monster, main.Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        main.Monster.__init__(self, ch_name)
        main.Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Golem"
        self.ch_atk = self._ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self._ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self._ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Smash (4)", 0, 4, "smash"]}
        self.__sk_smash = skill.Attack(self, 
            sk_mana = self.skill_list["2"][2],
            target_def_factor = 0.3,
            target_fx = "stun",
            target_fx_count = 1,
            target_fx_prob  = 0.4,
            atk_word = "smash",
            atk_icon = "🗯️")

    def smash(self, target):
        result = self.__sk_smash.attack(target)
        return result