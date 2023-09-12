"""
For "self.skill_list": {skillNumber: [skillName, skillMode, manaUsed, methodName]}
    - skillMode:
        - 0 Enemy individual
        - 1 Enemy team
        - 2 Hero individual
        - 3 Hero team
"""
import random
import time
from . import audio


class Attack:
    def __init__(self, user, sk_name="Attack", sk_mana=0, burst_count=1, 
                 target_def_factor = 0.5, target_fx = None, target_fx_count = 3, 
                 target_fx_prob = 0.3, atk_word="attack", atk_icon="🔪"):
        self.user = user
        self.sk_name = sk_name
        self.sk_mana = sk_mana
        self.burst_count = burst_count
        self.target_def_factor = target_def_factor
        self.target_fx = target_fx
        self.target_fx_count = target_fx_count
        self.target_fx_prob = target_fx_prob
        self.atk_word = atk_word
        self.atk_icon = atk_icon
        self.user_crit_words = ["Bring it on!!"]
        self.user_missed_words = ["Crap!"]
        if self.target_fx == "burn":
            self.target_fx_attr = "isBurn"
            self.target_fx_count_attr = "burn_count"
            self.target_fx_dec = "burn_dec"
        elif self.target_fx == "poison":
            self.target_fx_attr = "isPoison"
            self.target_fx_count_attr = "poison_count"
            self.target_fx_dec = "poison_dec"
        elif self.target_fx == "stun":
            self.target_fx_attr = "isStun"
            self.target_fx_count_attr = "stun_count"
            self.target_fx_dec = "stun_dec"
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound=None):
        print(text)
        self.ac.play_sfx(sound)

    def attack(self, targets):
        if type(targets) != list:
            targets = [targets]
        if self.user.ch_hp_r > 0:
            if self.user.ch_mp_r >= self.sk_mana:
                # for group attack
                for target in targets:
                    if target.ch_hp_r > 0:
                        critical = random.random() < self.user.ch_luk / 5
                        if critical and type(targets) != list:
                            self.user.speak(random.choice(self.user_crit_words))
                            time.sleep(1)
                        attack_sum = []
                        # for burst attack
                        for num in range(self.burst_count):
                            if self.burst_count > 1:
                                time.sleep(0.1)
                                count = f"#{num+1}"
                            else:
                                count =  ""
                            # if 100%, critical chance = 1/5
                            acc_factor = random.uniform(self.user.ch_acc, 1)
                            attack = self.user.ch_atk / (target.ch_def * self.target_def_factor)
                            effect_factor = random.uniform(0, 1) <= self.target_fx_prob
                            if acc_factor > 0.3:
                                attack = round(attack * acc_factor, 2)
                                # critical only individual attack
                                if critical and type(targets) != list:
                                    attack = round(attack * 1.5, 2)
                                    if self.target_fx:
                                        setattr(target, self.target_fx_attr, True)
                                        setattr(target, self.target_fx_count_attr, 
                                                self.target_fx_count)
                            else:
                                attack = 0
                            target.ch_hp_r = round(target.ch_hp_r - attack, 2)
                            if self.target_fx and effect_factor and attack:
                                setattr(target, self.target_fx_attr, True)
                                setattr(target, self.target_fx_count_attr, self.target_fx_count)
                            if target.ch_hp_r < 0:
                                target.ch_hp_r = 0
                            attack_sum.append(attack)
                            # print action
                            if attack:
                                if critical:
                                    self.__print_sfx((f"- {self.user.ch_name} {self.atk_word} "
                                                      f"{target.ch_name} {count} 💥{attack} !"),
                                                      "attack")
                                else:
                                    self.__print_sfx((f"- {self.user.ch_name} {self.atk_word} " 
                                                      f"{target.ch_name} {count} {self.atk_icon}{attack}"),
                                                      "attack")
                            else:
                                self.__print_sfx(f"- {self.user.ch_name} missed 💨", "fail")
                                self.user.speak(random.choice(self.user_missed_words))
                        if self.burst_count > 1:
                            print(f"- Total damage: {round(sum(attack_sum), 2)}")
                    else:
                        self.__print_sfx((f"- {target.ch_name} is inactive ❌ " 
                                          f"{self.user.ch_name} do nothing."), "fail")
                        if len(targets) == 1:
                            return False
                self.user.ch_mp_r = round(self.user.ch_mp_r - self.sk_mana, 2)
                return True
            else:
                self.__print_sfx(f"- {self.user.ch_name} has not enough MP.", "fail")
                return False
        else:
            self.user.ch_hp_r = 0
            self.__print_sfx(f"- {self.user.ch_name} can't do anything ❌", "fail")
            return True


class Heal:
    def __init__(self, user, sk_name="Heal", sk_mana=3, 
                 heal_value = 4, heal_buff = False, heal_buff_count = 0, 
                 heal_word="heal", heal_icon="✨"):
        self.user = user
        self.sk_name = sk_name
        self.sk_mana = sk_mana
        self.heal_value = heal_value
        self.heal_buff = heal_buff
        self.heal_buff_count = heal_buff_count
        self.heal_word = heal_word
        self.heal_icon = heal_icon
        self.speak_words = ["With the bless of godness!!"]
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound=None):
        print(text)
        self.ac.play_sfx(sound)

    def heal(self, targets):
        if type(targets) != list:
            targets = [targets]
        if self.user.ch_hp_r > 0:
            if self.user.ch_mp_r >= self.sk_mana:
                for target in targets:
                    if target.ch_hp_r >= target._ch_hp:
                        self.__print_sfx(f"- {target.ch_name}'s has fulled already.", "fail")
                        return False
                    elif target.ch_hp_r > 0:
                        target.ch_hp_r = round(target.ch_hp_r + self.heal_value, 2)
                        if target.ch_hp_r > target._ch_hp:
                            target.ch_hp_r = target._ch_hp
                        # print action
                        self.__print_sfx((f"- {self.user.ch_name} {self.heal_word} {target.ch_name} " 
                                          f"{self.heal_icon}+{self.heal_value}"), "heal")
                    else:
                        self.__print_sfx((f"- {target.ch_name} is inactive ❌ " 
                                          f"{self.user.ch_name} do nothing."), "heal")
                        if len(targets) == 1:
                            return False
                self.user.ch_mp_r = round(self.user.ch_mp_r - self.sk_mana, 2)
                return True
            else:
                self.__print_sfx(f"- {self.user.ch_name} has not enough MP.", "fail")
                return False
        else:
            self.user.ch_hp_r = 0
            self.__print_sfx(f"- {self.user.ch_name} can't do anything ❌", "fail")
            return True