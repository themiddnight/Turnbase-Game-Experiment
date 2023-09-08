import time
import random
from MainClass import Human, Monster, Warrior

class Archer(Human, Warrior):
    def __init__(
        self, ch_name, ch_hp=10, ch_mp=10, ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5
    ):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Archer"
        self.ch_atk = self.ch_atk_i * 1.1
        self.ch_def = self.ch_def_i * 0.9
        self.ch_acc = self.ch_acc_i * 0.8
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Burst Shoot", 0, 3, "burst_shoot"],
        }
        """Key: {skillNumber: [skillName, skillMode, manaUsed, methodName]}.\n
        skillMode: \n
        0 Enemy individual \n
        1 Enemy team \n
        2 Hero individual \n
        3 Hero team"""

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
                                print(
                                    (
                                        f"- {self.ch_name} shot "
                                        f"{target.ch_name} #{num} 💥{attack} !"
                                    )
                                )
                            else:
                                print(
                                    (
                                        f"- {self.ch_name} shot "
                                        f"{target.ch_name} #{num} 🏹{attack}"
                                    )
                                )
                        else:
                            print(f"- {self.ch_name} missed 💨")
                            self.speak("Crap!!")
                        time.sleep(0.1)
                    self.ch_mp_r -= self.skill_list["2"][2]
                    print(f"- Total damage: {round(sum(attack_sum), 2)}.")
                    return True
                else:
                    print(
                        (f"- {target.ch_name} is dead ❌ " f"{self.ch_name} do nothing.")
                    )
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True

class Knight(Human, Warrior):
    def __init__(
        self, ch_name, ch_hp=10, ch_mp=10, ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5
    ):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Knight"
        self.ch_atk = self.ch_atk_i * 1.3
        self.ch_def = self.ch_def_i * 1.3
        self.ch_acc = self.ch_acc_i * 0.7
        # if 100%, critical chance = 1/5
        self.__critical_factor = self.ch_luk / 5
        self.skill_list = {
            "1": ["Attack", 0, 0, "attack"],
            "2": ["Hard Attack", 0, 3, "hard_attack"],
        }
        """Key: {Skill_number: [Skill_name, Skill_mode, Mana_used, Method_name]} \n
        Skill_mode: \n
        0 Enemy individual \n
        1 Enemy team \n
        2 Hero individual \n
        3 Hero team"""

    def hard_attack(self, target):
        if type(target) == list:
            target = target[0]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                if target.ch_hp_r > 0:
                    critical = random.random() < self.__critical_factor
                    acc_factor = random.uniform(0.8, 1)
                    attack = self.ch_atk / (target.ch_def * 0.3)
                    attack = round(attack * acc_factor, 2)
                    if acc_factor > 0.81:
                        attack = round(attack * acc_factor, 2)
                        if critical:
                            attack = round(attack * 1.2, 2)
                    else:
                        attack = 0
                    target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                    if target.ch_hp_r < 0:
                        target.ch_hp_r = 0
                    self.ch_mp_r -= self.skill_list["2"][2]
                    # print action
                    if attack:
                        if critical:
                            self.speak("Bring it on!!")
                            print(
                                (
                                    f"- {self.ch_name} hard attacks "
                                    f"{target.ch_name}! 💥💥{attack} !"
                                )
                            )
                        else:
                            print(
                                (
                                    f"- {self.ch_name} hard attacks "
                                    f"{target.ch_name}! 🔪🔪{attack}"
                                )
                            )
                    else:
                        print(f"- {self.ch_name} missed 💨")
                        self.speak("Crap!!")
                    return True
                else:
                    print(
                        (f"- {target.ch_name} is dead ❌ " f"{self.ch_name} do nothing.")
                    )
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Priest(Human, Warrior):
    def __init__(
        self, ch_name, ch_hp=10, ch_mp=10, ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5
    ):
        Human.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Priest"
        self.ch_atk = self.ch_atk_i * 0.6
        self.ch_def = self.ch_def_i * 1.2
        self.ch_acc = self.ch_acc_i * 0.7
        self.__heal_value = 3
        self.skill_list = {"1": ["Attack", 0, 0, "attack"], "2": ["Heal", 2, 3, "heal"]}
        """Key: {Skill_number: [Skill_name, Skill_mode, Mana_used, Method_name]} \n
        Skill_mode: \n
        0 Enemy individual \n
        1 Enemy team \n
        2 Hero individual \n
        3 Hero team"""

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
                    self.ch_mp_r -= self.skill_list["2"][2]
                    # print action
                    print(
                        (
                            f"- {self.ch_name} heals {target.ch_name} "
                            f"✨+{self.__heal_value}"
                        )
                    )
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
    def __init__(
        self, ch_name, ch_hp=10, ch_mp=10, ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5
    ):
        Monster.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Dragon"
        self.ch_atk = self.ch_atk_i * 1.5
        self.ch_def = self.ch_def_i * 2.2
        self.ch_acc = self.ch_acc_i * 0.6
        self.skill_list = {"1": ["Attack", 0, 0, "attack"], "2": ["Burn", 1, 4, "burn"]}
        """Key: {Skill_number: [Skill_name, Skill_mode, Mana_used, Method_name]} \n
        Skill_mode: \n
        0 Enemy individual \n
        1 Enemy team \n
        2 Hero individual \n
        3 Hero team"""

    def burn(self, target):
        if type(target) != list:
            target = [target]
        if self.ch_hp_r > 0:
            if self.ch_mp_r >= self.skill_list["2"][2]:
                for i in target:
                    if i.ch_hp_r > 0:
                        acc_factor = random.uniform(0.8, 1)
                        attack = self.ch_atk / (i.ch_def * 0.4)
                        attack = round(attack * acc_factor, 2)
                        i.ch_hp_r = round(i.ch_hp_r - attack, 2)
                        if i.ch_hp_r < 0:
                            i.ch_hp_r = 0
                        # print action
                        print(
                            (
                                f"- {self.ch_name} burns "
                                f"{i.ch_name}! 🔥🔥{attack}"
                            )
                            )
                    else:
                        print(
                            (f"- {i.ch_name} is dead ❌ " f"{self.ch_name} do nothing.")
                        )
                self.ch_mp_r -= self.skill_list["2"][2]
                return True
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True


class Vampire(Monster, Warrior):
    def __init__(
        self, ch_name, ch_hp=10, ch_mp=10, ch_atk=10, ch_def=10, ch_acc=1, ch_luk=0.5
    ):
        Monster.__init__(self, ch_name)
        Warrior.__init__(self, ch_hp, ch_mp, ch_atk, ch_def, ch_acc, ch_luk)
        self.ch_class = "Vampire"
        self.ch_atk = self.ch_atk_i * 1.0
        self.ch_def = self.ch_def_i * 1.1
        self.ch_acc = self.ch_acc_i * 0.8
        self.skill_list = {"1": ["Attack", 0, 0, "attack"], "2": ["Bite", 0, 3, "bite"]}
        """Key: {Skill_number: [Skill_name, Skill_mode, Mana_used, Method_name]} \n
        Skill_mode: \n
        0 Enemy individual \n
        1 Enemy team \n
        2 Hero individual \n
        3 Hero team"""

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
                    if target.ch_hp_r < 0:
                        target.ch_hp_r = 0
                    # print action
                    print(
                        (f"- {self.ch_name} bites " f"{target.ch_name} 🔪{attack}")
                    )
                    self.ch_mp_r -= self.skill_list["2"][2]
                    return True
                else:
                    print((f"- {target.ch_name} is dead ❌ " f"{self.ch_name} do nothing."))
                    return False
            else:
                print(f"- {self.ch_name} has not enough MP.")
                return False
        else:
            self.ch_hp_r = 0
            print(f"- {self.ch_name} can't do anything ❌")
            return True