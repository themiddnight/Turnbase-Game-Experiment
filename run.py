import json
from core import arena, player

heroes  = [
    player.Archer(ch_name="Alex")
    ,player.Knight(ch_name="Belatrix")
    ,player.Priest(ch_name="Kevin")
]
enemies = [
    player.Dragon(ch_name="Kraken")
    ,player.Vampire(ch_name="Cyclops")
    ,player.Golem(ch_name="Garlik")
]

arenaA = arena.Arena(increase_hp = 0, increase_mp = 1.3)
arenaA.set_characters(heroes, enemies)

if __name__ == "__main__":
    arenaA.battle()