import CharClass as char, ArenaClass as arena

alex     = char.Archer(ch_name="Alex")
belatrix = char.Knight(ch_name="Belatrix")
kevin    = char.Priest(ch_name="Kevin")

kraken  = char.Dragon(ch_name="Kraken")
cyclops = char.Vampire(ch_name="Cyclops")
garlik  = char.Golem(ch_name="Garlik")

arenaA = arena.Arena(increase_hp = 0, increase_mp = 1.3)

if __name__ == "__main__":
    arenaA.battle(heroes  = [belatrix, alex, kevin], 
                  enemies = [cyclops, kraken, garlik])
