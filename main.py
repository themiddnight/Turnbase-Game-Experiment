import CharClass as char, ArenaClass as arena

alex     = char.Archer(ch_name="Alex")
belatrix = char.Knight(ch_name="Belatrix")
kevin    = char.Priest(ch_name="Kevin")

kraken  = char.Dragon(ch_name="Kraken")
cyclops = char.Vampire(ch_name="Cyclops")

arenaA = arena.Arena()

if __name__ == "__main__":
    arenaA.battle(heroes  = [kraken], 
                  enemies = [cyclops, belatrix, alex])
