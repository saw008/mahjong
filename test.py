from mahjong_list import *
import time


def main():
    start_time = time.time()

    player1, player2, player3, player4, now_tiles, rounder = init_game()
    # -------------------------------------------------------
    # print(tile_names(tmp_list))
    player1.vis_my_tiles()
    player2.vis_my_tiles()
    player3.vis_my_tiles()
    player4.vis_my_tiles()
    rounder.go().discard_a_tile()
    while len(now_tiles) is not 0:
        now_player = rounder.go()
        now_tiles = now_player.draw_a_tile(now_tiles)
        # print(len(now_tiles))
        now_player.discard_a_tile()
    print("---------end---------")
    player1.vis_my_tiles()
    player2.vis_my_tiles()
    player3.vis_my_tiles()
    player4.vis_my_tiles()
    end_time = time.time()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
