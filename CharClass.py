"""
For "self.skill_list": {skillNumber: [skillName, skillMode, manaUsed, methodName]}
    - skillMode:
        - 0 Enemy individual
        - 1 Enemy team
        - 2 Hero individual
        - 3 Hero team
"""
import json
import time
import random
from MainClass import Human, Monster, Warrior

with open("settings.json", "r") as f:
    settings = json.load(f)
    class_stats_mlp = settings["class_stats_mlp"]
    battling = settings["battling"]


class Archer(Human, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Archer"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Burst Shoot (3)", 0, 3, "burst_shoot"],}
        print(battling)

    def burst_shoot(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r > 0:
                    attack_sum = []
                    for num in range(1, 4):
                        critical = random.random() < self.__critical_factor
                        acc_factor = random.uniform(self.ch_acc, 1)
                        attack = self.ch_atk / (target.ch_def * 0.75)
                        if acc_factor > 0.4:
                            attack = round(attack * acc_factor, 2)
                            if critical:
                                attack = round(attack * 1.5, 2)
                        else:
                            attack = 0
                        target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                        if target.ch_hp_r < 0:
                            target.ch_hp_r = 0
                        attack_sum.append(attack)
                        # print action
                        if attack:
                            if critical:
                                print((f"- {self.ch_name} shot "
                                       f"{target.ch_name} #{num} 💥{attack} !"))
                            else:
                                print((f"- {self.ch_name} shot "
                                       f"{target.ch_name} #{num} 🏹{attack}"))
                        else:
                            print(f"- {self.ch_name} missed 💨")
                            self.speak("Crap!!")
                        time.sleep(0.1)
                    self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                    print(f"- Total damage: {round(sum(attack_sum), 2)}.")
                    return True
                else:
                    print((f"- {target.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True

class Knight(Human, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Knight"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Hard Attack (3)", 0, 3, "hard_attack"],}

    def hard_attack(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r > 0:
                    critical = random.random() < self.__critical_factor
                    acc_factor = random.uniform(self.ch_acc, 1) > self.ch_acc + 0.05
                    stun_factor = random.uniform(0, 1) < 0.3
                    attack = self.ch_atk / (target.ch_def * 0.3)
                    attack = round(attack * acc_factor, 2)
                    if acc_factor:
                        attack = round(attack * acc_factor, 2)
                        if critical:
                            attack = round(attack * 1.2, 2)
                            target.stunned = True
                            target.stunned_count = battling["stat_turn"]["stun_count"]
                    else:
                        attack = 0
                    target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                    if stun_factor:
                        if attack:
                            target.stunned = True
                            target.stunned_count = battling["stat_turn"]["stun_count"]
                    if target.ch_hp_r < 0:
                        target.ch_hp_r = 0
                    self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                    # print action
                    if attack:
                        if critical:
                            self.speak("Bring it on!!")
                            print((f"- {self.ch_name} hard attacks "
                                   f"{target.ch_name}! 💥💥{attack} !"))
                        else:
                            print((f"- {self.ch_name} hard attacks "
                                   f"{target.ch_name}! 🔪🔪{attack}"))
                    else:
                        print(f"- {self.ch_name} missed 💨")
                        self.speak("Crap!!")
                    return True
                else:
                    print((f"- {target.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Priest(Human, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Priest"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.__heal_value = 4
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Heal (3)", 2, 3, "heal"]}

    def heal(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r >= target.ch_hp:
                    print(f"{target.ch_name}'s has fulled already.")
                    return False
                elif target.ch_hp_r > 0:
                    target.ch_hp_r = round(target.ch_hp_r + self.__heal_value, 2)
                    if target.ch_hp_r > target.ch_hp:
                        target.ch_hp_r = target.ch_hp
                    self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                    # print action
                    print((f"- {self.ch_name} heals {target.ch_name} "
                           f"✨+{self.__heal_value}"))
                    return True
                else:
                    print(f"- {target.ch_name} died. Can't do anything ❌")
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Dragon(Monster, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Monster.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Dragon"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Burn (4)", 1, 4, "burn"]}

    def burn(self, target):
        if type(target) != list:
            target = [target]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                for i in target:
                    if i.ch_hp_r > 0:
                        acc_factor = random.uniform(self.ch_acc, 1)
                        burn_factor = random.uniform(0, 1) < 0.7
                        attack = self.ch_atk / (i.ch_def * 0.4)
                        attack = round(attack * acc_factor, 2)
                        i.ch_hp_r = round(i.ch_hp_r - attack, 2)
                        if burn_factor:
                            i.burned = True
                            i.burned_count = battling["stat_turn"]["burn_count"]
                        if i.ch_hp_r < 0:
                            i.ch_hp_r = 0
                        # print action
                        print((f"- {self.ch_name} burns "
                               f"{i.ch_name}! 🔥🔥{attack}"))
                    else:
                        print((f"- {i.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                return True
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Vampire(Monster, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Monster.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Vampire"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Bite (3)", 0, 3, "bite"]}

    def bite(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r > 0:
                    acc_factor = random.uniform(self.ch_acc, 1)
                    attack = self.ch_atk / (target.ch_def * 0.3)
                    attack = round(attack * acc_factor, 2)
                    target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                    target.poisoned = True
                    target.poisoned_count = battling["stat_turn"]["poison_count"]
                    if target.ch_hp_r < 0:
                        target.ch_hp_r = 0
                    # print action
                    print((f"- {self.ch_name} bites " f"{target.ch_name} 🔪{attack}"))
                    self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                    return True
                else:
                    print((f"- {target.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Golem(Monster, Warrior):
    def __init__(self, ch_name, ch_hp=20, ch_mp=10, 
                 ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5):
        Monster.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Golem"
        self.ch_atk = self.ch_atk_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_atk"]
        self.ch_def = self.ch_def_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_def"]
        self.ch_acc = self.ch_acc_i * class_stats_mlp[self.ch_type][self.ch_class]["ch_acc"]
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"], 
            "2": ["Smash (4)", 0, 4, "smash"]}

    def smash(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r > 0:
                    critical = random.random() < self.__critical_factor
                    acc_factor = random.uniform(self.ch_acc, 1)
                    stun_factor = random.uniform(0, 1) < 0.35
                    attack = self.ch_atk / (target.ch_def * 0.3)
                    attack = round(attack * acc_factor, 2)
                    if acc_factor > 0.81:
                        attack = round(attack * acc_factor, 2)
                        if critical:
                            attack = round(attack * 1.2, 2)
                            target.stunned = True
                            target.stunned_count = battling["stat_turn"]["stun_count"]
                    else:
                        attack = 0
                    target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                    if stun_factor:
                        if attack:
                            target.stunned = True
                            target.stunned_count = battling["stat_turn"]["stun_count"]
                    if target.ch_hp_r < 0:
                        target.ch_hp_r = 0
                    self.ch_mp_r = round(self.ch_mp_r - self.skill_list["2"][2], 2)
                    # print action
                    if attack:
                        if critical:
                            self.speak("Bring it on!!")
                            print((f"- {self.ch_name} hard attacks "
                                   f"{target.ch_name}! 💥💥{attack} !"))
                        else:
                            print((f"- {self.ch_name} hard attacks "
                                   f"{target.ch_name}! 🗯️🗯️{attack}"))
                    else:
                        print(f"- {self.ch_name} missed 💨")
                        self.speak("Crap!!")
                    return True
                else:
                    print((f"- {target.ch_name} is inactive ❌ " f"{self.ch_name} do nothing."))
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True