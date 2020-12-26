"""
This program is a simulation of the Chinese board game called Mahjong.

Author: Hao Li
Email: hxl1033@case.edu
Created: 2020-11-26 20:00
Last modified: now
"""
# TODO: 目前的程序，每个人的手牌是以 set() 格式存储的，暂时不确定是list()还是set()更合理。
import operator
import random
import time


class Tile:
    def __init__(self, count, kind):
        self.count = str(count)
        self.kind = kind

    def what(self):
        return self.count + '_' + self.kind


class Player:
    def __init__(self, name, score, if_dealer):
        self.name = str(name)
        self.score = score
        self.if_dealer = if_dealer
        self.my_tiles = set()

    def get_score(self):
        return self.score

    def draw_a_tile(self, now_board_tiles):
        """
        Draw a tile

        :param now_board_tiles: can be bing/tiao/wan
        :returns: temp_list is the list of all tiles in one kind.
        """
        # TODO: 加入每次摸牌之后sort的功能
        # TODO: 目前是随机取一张牌，不合理，应该是取最前一张牌
        temp_tile = random.sample(now_board_tiles, 1)[0]
        now_board_tiles.remove(temp_tile)
        self.my_tiles.add(temp_tile)
        return now_board_tiles

    def discard_a_tile(self):
        # TODO: 目前是随机打出一张牌，显然不合理，但以后再改
        temp_tile = random.sample(self.my_tiles, 1)[0]
        self.my_tiles.remove(temp_tile)
        return temp_tile

    def get_my_tiles(self):
        return self.my_tiles

    def sort_my_tiles(self):
        # TODO: now too complicated
        sort_kind_count = operator.attrgetter('kind', 'count')
        tmp_list = list(self.my_tiles)
        tmp_list.sort(key=sort_kind_count)
        return tmp_list
        # for item in self.my_tiles:


class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None


def helper_generate_one_kind_tiles(kind):
    """
    Simply generate all tiles of one individual kind.

    :param kind: can be bing/ tiao/ wan
    :returns: temp_list is the list of all tiles in one kind.
    """
    temp_list = set([])
    for i in range(0, 36):
        temp_count = int(i / 4) + 1
        temp_list.add(Tile(temp_count, kind))
        # temp_list.append(Tile(temp_count, kind).what())
    return temp_list


def toss_a_dice():
    # TODO: 用来定义摸牌位置和换牌方向，暂时没用。
    return random.randint(1, 6)


def init_game():
    """
    This function initializes 4 Player objects with 100 points each, and all of the tiles. There
    are 3*4*9 = 108 tiles in total.

    :returns: p1 ~ p4 are the four players, all_tiles is the list of every Tile objects in one game.
    """
    kinds = ['bing', 'tiao', 'wann']
    tmp_dealer_list = [False, False, False, False]
    tmp_dealer_list[random.randint(0, 3)] = True
    p1 = Player(1, 100, tmp_dealer_list[0])
    p2 = Player(2, 100, tmp_dealer_list[1])
    p3 = Player(3, 100, tmp_dealer_list[2])
    p4 = Player(4, 100, tmp_dealer_list[3])
    all_tiles = helper_generate_one_kind_tiles(kinds[0]) | \
                helper_generate_one_kind_tiles(kinds[1]) | \
                helper_generate_one_kind_tiles(kinds[2])
    return p1, p2, p3, p4, all_tiles


def tile_names(tiles_in_set):
    if isinstance(tiles_in_set, Tile):
        tiles_in_set = {tiles_in_set}

    if len(tiles_in_set) > 1:
        tmp_tiles_list = []
        for item in tiles_in_set:
            tmp_tiles_list.append(item.what())
        return tmp_tiles_list
    elif len(tiles_in_set) == 1:
        return tiles_in_set.pop().what()
    else:
        print('error occurred!')


# def sort_deck(tiles_in_set):
#     temp


def main():
    start_time = time.time()

    player1, player2, player3, player4, now_tiles = init_game()
    for i in range(3):
        for j in range(4):
            now_tiles = player1.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = player2.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = player3.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = player4.draw_a_tile(now_tiles)

    tmp_player_list = [player1, player2, player3, player4]
    for p in tmp_player_list:
        if p.if_dealer:
            now_tiles = p.draw_a_tile(now_tiles)
    print(tile_names(player1.sort_my_tiles()))
    print(tile_names(player1.discard_a_tile()))
    print(tile_names(player1.get_my_tiles()))

    # print(tile_names(tmp_list))
    print('Player 1: ', tile_names(player1.get_my_tiles()))
    print('Player 2: ', tile_names(player2.get_my_tiles()))
    print('Player 3: ', tile_names(player3.get_my_tiles()))
    print('Player 4: ', tile_names(player4.get_my_tiles()))
    end_time = time.time()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
