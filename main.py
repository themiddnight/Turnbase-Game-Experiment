import CharClass as char, ArenaClass as arena

if __name__ == "__main__":
    alex     = char.Archer(ch_name="Alex")
    belatrix = char.Knight(ch_name="Belatrix")
    kevin    = char.Priest(ch_name="Kevin")

    kraken  = char.Dragon(ch_name="Kraken")
    cyclops = char.Vampire(ch_name="Cyclops")

    arenaA = arena.Arena()
    arenaA.battle(heroes=[kevin, alex, belatrix], 
                 enemies=[kraken, cyclops])
