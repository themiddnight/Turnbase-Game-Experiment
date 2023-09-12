import time
import os
import random
from . import char
from . import audio


class Arena:
    def __init__(self, increase_hp=0, increase_mp=0):
        self.increase_hp = increase_hp
        self.increase_mp = increase_mp
        self.heroes  = [char.Knight(ch_name = "Sir Placeholder")]
        self.enemies = [char.Dragon(ch_name = "The Placeholder")]
        self.ac = audio.PlayAudio()

    def __print_sfx(self, text, sound="pop"):
        print(text)
        self.ac.play_sfx(sound)

    def __select_choice(self, isRoot, prompt, choice_dict):
        """
        For showing actions or target list and validating user input. If invalid, loop until it valid.
            - isRoot: if isRoot is true, user can't input b for back
            - prompt: For showing input prompt.
            - action_dict: The dict for choices list. <- { "number": ["name", ... ] }
            - -> output: A validated string of input.
        """
        for choice in choice_dict:
            self.__print_sfx(f"  {choice}. {choice_dict[choice][0]}")
        check = True
        while check:
            selection = input(prompt)
            print()
            if isRoot:
                if selection == "q":
                    check = False
                elif selection == "b":
                    self.__print_sfx("No back! Try again", "fail")
                elif selection.isnumeric() == False:
                    self.__print_sfx("Invalid input! Try again", "fail")
                elif int(selection) > len(choice_dict):
                    self.__print_sfx("The input exceeds the list! Try again", "fail")
                else:
                    check = False
            else:
                if selection == "b" or selection == "q":
                    check = False
                elif selection.isnumeric() == False:
                    self.__print_sfx("Invalid input! Try again", "fail")
                elif int(selection) > len(choice_dict):
                    self.__print_sfx("The input exceeds the list! Try again", "fail")
                else:
                    check = False
        return selection

    def __create_char_dict(self, team, charObj_list):
        """
        Create char dict from char objects list for showing input command.
        Parameter:
            - team: Should be 'hero' or 'enemy'.
            - charObj_list: List of character's object.
            - -> Output: { "number": ["name", object] }
        """
        char_dict = {}
        num = 1
        for char in charObj_list:
            # if team == "enemy":
            #     if char.ch_hp_r > 0:
            #         # char_dict = {number : [Name, Object]}
            #         char_dict[f"{num}"] = [char.ch_name, char]
            #         num += 1
            # else:
            char_dict[f"{num}"] = [char.ch_name, char]
            num += 1
        return char_dict

    def set_characters(self, heroes:list, enemies:list):
        self.heroes  = heroes 
        self.enemies = enemies
        # shuffle the characters list
        random.shuffle(self.heroes)
        random.shuffle(self.enemies)

    def show_summary(self):
        """
        Clear screen and show updated status of characters.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # rotate table
        max_length = max(len(sublist) for sublist in [self.heroes, self.enemies])
        ch_disp = []
        for i in range(max_length):
            row = []
            for sublist in [self.heroes, self.enemies]:
                row.append(sublist[i]) if i < len(sublist) else row.append(None)
            ch_disp.append(row)
        # print
        j_val = 44
        print (f'{"  HEROES  ":=^{j_val}}' + '|' + f'{"  ENEMIES  ":=^{j_val}}')
        print (f' '.ljust(j_val) + '|' + f' '.ljust(j_val))
        for i in ch_disp:
            if i[0]:
                name0, statsymbol0 = i[0].get_title()
                title0 = f'  • {name0}'.ljust(j_val - statsymbol0)
                stats0 = f'    {i[0].ch_atk} / {i[0].ch_def} / {i[0].ch_acc} / {i[0].ch_luk}'.ljust(j_val)
                hpbar0 = f'    {i[0].get_hp_bar()}'.ljust(j_val)
                mpbar0 = f'    {i[0].get_mp_bar()}'.ljust(j_val)
            else: 
                title0 = ''.ljust(j_val)
                stats0 = ''.ljust(j_val)
                hpbar0 = ''.ljust(j_val)
                mpbar0 = ''.ljust(j_val)
            if i[1]: 
                name1, statsymbol1 = i[1].get_title()
                title1 = f'  • {name1}'.ljust(j_val - statsymbol1)
                stats1 = f'    {i[1].ch_atk} / {i[1].ch_def} / {i[1].ch_acc} / {i[1].ch_luk}'.ljust(j_val)
                hpbar1 = f'    {i[1].get_hp_bar()}'.ljust(j_val) 
                mpbar1 = f'    {i[1].get_mp_bar()}'.ljust(j_val) 
            else: 
                title1 = ''.ljust(j_val)
                stats1 = ''.ljust(j_val)
                hpbar1 = ''.ljust(j_val)
                mpbar1 = ''.ljust(j_val)

            print (f"{title0}|{title1}")
            print (f"{stats0}|{stats1}")
            print (f"{hpbar0}|{hpbar1}")
            print (f"{mpbar0}|{mpbar1}")
            print (f'   '.ljust(j_val) + '|' + f'   '.ljust(j_val))
            
        print (f'{"":=^{j_val*2+1}}')
        print("* Stats: ATK / DEF / ACC / LUK")
        print("* Input b to go back, q for quit.")
        print()

    def battle(self):
        self.ac.play_battle_music()
        enter_to_continue_tx = "Press Enter to continue..."
        user_continue = True  # for checking if user are not quit
        # game loop until one team is all dead
        while any(hero.ch_hp_r > 0 for hero in self.heroes) and \
            any(enemy.ch_hp_r > 0 for enemy in self.enemies):
            
            # increase hp/mp
            for hero in self.heroes:
                if hero.ch_hp_r > 0:
                    hero.ch_hp_r = round(hero.ch_hp_r + self.increase_hp, 2)
                    hero.ch_mp_r = round(hero.ch_mp_r + self.increase_mp, 2)
                    if hero.ch_hp_r > hero._ch_hp: hero.ch_hp_r = hero._ch_hp
                    if hero.ch_mp_r > hero._ch_mp: hero.ch_mp_r = hero._ch_mp
            for enemy in self.enemies:
                if enemy.ch_hp_r > 0:
                    enemy.ch_hp_r = round(enemy.ch_hp_r + self.increase_hp, 2)
                    enemy.ch_mp_r = round(enemy.ch_mp_r + self.increase_mp, 2)
                    if enemy.ch_hp_r > enemy._ch_hp: enemy.ch_hp_r = enemy._ch_hp
                    if enemy.ch_mp_r > enemy._ch_mp: enemy.ch_mp_r = enemy._ch_mp
            
            self.show_summary()

            # effects turn trigger
            isEffects = []
            for hero in self.heroes:
                isEffects.append(hero.effects_turn_trigger())
            for enemy in self.enemies:
                isEffects.append(enemy.effects_turn_trigger())
            if any(isEffects):
                self.ac.play_sfx("fail")
                time.sleep(0.5)
                input(f"\n{enter_to_continue_tx}")

            # iterate hero turns
            for hero in self.heroes:
                if hero.ch_hp_r > 0 and any(mons.ch_hp_r > 0 for mons in self.enemies):
                    self.show_summary()
                    print(f"-> {hero.ch_name}'s turn.\n")

                    # if stunned, report and skip action
                    if hero.isStun:
                        time.sleep(0.5)
                        self.__print_sfx(f"- {hero.ch_name} is stunned 🌀", "fail")
                        hero.stun_count -= 1
                        input(f"\n{enter_to_continue_tx}")
                        continue

                    # loop until the char's action success
                    while True:
                        sel_action_prompt = f"What will {hero.ch_name} do?: "
                        # select action
                        sel_action = self.__select_choice(True, sel_action_prompt, 
                                                          hero.skill_list)
                        if sel_action == "q":
                            user_continue = False
                            break

                        # check skill mode and setup 'char_dict' - the targets to be action with
                        # such as, if the action is 'attack', the list should be self.enemies
                        # and if 'heal', it shoud be self.heroes themselves
                        action_mode = hero.skill_list[sel_action][1]

                        # 0 Enemy individual, 1 Enemy team, 2 Hero individual, 3 Hero team
                        # more documents in 'CharClass.py'
                        if action_mode == 0:
                            sel_char_prompt = (f"Which enemy will {hero.ch_name} attack?: ")
                            char_dict = self.__create_char_dict("enemy", self.enemies)
                        elif action_mode == 1:
                            char_dict = self.__create_char_dict("enemy", self.enemies)
                        elif action_mode == 2:
                            sel_char_prompt = f"Which one will {hero.ch_name} heal?: "
                            char_dict = self.__create_char_dict("hero", self.heroes)
                        elif action_mode == 3:
                            char_dict = self.__create_char_dict("hero", self.heroes)

                        # select target
                        if action_mode == 0 or action_mode == 2:
                            sel_char = [self.__select_choice(False, sel_char_prompt, 
                                                             char_dict)]
                        elif action_mode == 1 or action_mode == 3:
                            sel_char = []
                            for i in char_dict:
                                sel_char.append(i)

                        if sel_char[0] == "b":
                            continue
                        elif sel_char[0] == "q":
                            user_continue = False
                            break
                        else:
                            time.sleep(0.5)
                            # get hero's methods to do action
                            # 'skill_list' attr: 
                            #   {skillNum: [skillName, skillMode, manaUsed, method]}
                            #   {"1": ["Attack", 0, 0, attack]}
                            #    ^^^                   ^^^^^^
                            #   sel_action             *[3]*
                            hero_action = getattr(hero, hero.skill_list[sel_action][3])
                            target = []
                            for i in sel_char:
                                # do action: _.action_method(target_obj)
                                # target_obj <- char_dict:
                                #   {"number": ["name", object]}
                                #    ^^^^^^^^           ^^^^^^
                                #    sel_char           *[1]*
                                target.append(char_dict[i][1])
                            success = hero_action(target)
                            print()
                            if success:
                                input(f"\n{enter_to_continue_tx}")
                                break
                            else:
                                self.__print_sfx("Try again!", "fail")
                    if user_continue == False:
                        break
                else:
                    continue
            if user_continue == False:
                break

            self.show_summary()

            # iterate enemy turns
            for enemy in self.enemies:
                if any(hero.ch_hp_r > 0 for hero in self.heroes):
                    # if stunned, report and skip action
                    if enemy.isStun:
                        time.sleep(1)
                        self.__print_sfx(f"- {enemy.ch_name} is stunned 🌀", "fail")
                        enemy.stun_count -= 1
                        print()
                        continue
                    if enemy.ch_hp_r > 0:
                        time.sleep(1)
                        # random only when 'skill_mana' > 'ch_mp_r'
                        enemy_action_choices = list(map(lambda x: x, enemy.skill_list))
                        enough_mp_check = True
                        while enough_mp_check:
                            enemy_action_choice = random.choice(enemy_action_choices)
                            if enemy.ch_mp_r >= enemy.skill_list[enemy_action_choice][2]:
                                enough_mp_check = False
                        enemy_action = getattr(enemy, enemy.skill_list[enemy_action_choice][3])
                        action_mode = enemy.skill_list[enemy_action_choice][1]
                        if action_mode == 0: #<- hero individual
                            alive_heroes_list = [hero for hero in self.heroes if hero.ch_hp_r > 0]
                            hero_target = random.choice(alive_heroes_list)
                            enemy_action(hero_target)
                        elif action_mode == 1: # <- hero team
                            enemy_action(self.heroes)
                        elif action_mode == 2: # <- self individual
                            alive_enemies_list = [enmy for enmy in self.enemies if enemy.ch_hp_r > 0]
                            enemy_target = random.choice(alive_enemies_list)
                            enemy_action(enemy_target)
                        elif action_mode == 3: # <- self team
                            enemy_action(self.enemies)
                        print()
                else:
                    break
            if any(enemy.ch_hp_r > 0 for enemy in self.enemies):
                time.sleep(1)
                input(f"\n{enter_to_continue_tx}")

        if user_continue == True:
            self.show_summary()
            if any(hero.ch_hp_r > 0 for hero in self.heroes):
                self.ac.play_win_music()
                self.__print_sfx("HEROES WIN!\n")
            else:
                self.ac.play_lose_music()
                self.__print_sfx("HEROES LOSE.\n")
            time.sleep(5)