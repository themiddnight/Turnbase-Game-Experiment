import CharClass as char, ArenaClass as arena

alex     = char.Archer(ch_name="Alex")
belatrix = char.Knight(ch_name="Belatrix")
kevin    = char.Priest(ch_name="Kevin")

kraken  = char.Dragon(ch_name="Kraken")
cyclops = char.Vampire(ch_name="Cyclops")

arenaA = arena.Arena()

kraken.ch_mp_r = 1
cyclops.ch_mp_r = 1
if __name__ == "__main__":
    arenaA.battle(heroes  = [belatrix, alex, kevin], 
                  enemies = [cyclops, kraken])
