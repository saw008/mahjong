from mahjong import *

game = Board()
for _ in game.now_tiles:
    # print(_.vis())
    pass

print(len(game.now_tiles))
print(game.now_tiles.pop())
print(len(game.now_tiles))
