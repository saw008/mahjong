"""
This program is a simulation of the Chinese board game called Mahjong.

Author: Hao Li
Email: hxl1033@case.edu
Created: 2020-11-26 20:00
Last modified: now
"""
# TODO: 目前的程序，每个人的手牌是以 list() 格式存储的，暂时不确定是list()还是set()更合理。
import operator
import random
import time


class Tile(object):
    def __init__(self, count, kind):
        self.count = str(count)
        self.kind = kind

    def what(self):
        return self.count + '_' + self.kind

    def vis(self):
        return f"*---*\n| {self.count} |\n| {self.kind[0].upper()} |\n*---*"


class Player(object):
    def __init__(self, name, score, if_dealer):
        self.name = str(name)
        self.score = score
        self.if_dealer = if_dealer
        self.my_tiles = list()

    def get_score(self):
        return self.score

    def draw_a_tile(self, now_tiles_on_board):
        """
        Draw a tile from the stack of current tiles on board.

        :param now_tiles_on_board: a List of Tile objects.
        :returns: now_tiles_on_board is the stack of current tiles on board after drawing one tile.
        """
        # TD: 加入每次摸牌之后sort的功能 -- 已实现
        # TD: 目前是随机取一张牌，不合理，应该是取最前一张牌 -- 暂时觉着没问题
        temp_tile = random.sample(now_tiles_on_board, 1)[0]
        now_tiles_on_board.remove(temp_tile)
        self.my_tiles.append(temp_tile)
        self.sort_my_tiles()  # 在每次取牌之后整理手牌
        return now_tiles_on_board

    def discard_a_tile(self):
        # TODO: 目前是随机打出一张牌，显然不合理，但以后再改
        temp_tile = random.sample(self.my_tiles, 1)[0]
        self.my_tiles.remove(temp_tile)
        self.sort_my_tiles()  # 在每次打牌之后整理手牌
        return temp_tile

    def get_my_tiles(self):
        return self.my_tiles

    def sort_my_tiles(self):
        # TODO: now too complicated
        sort_kind_count = operator.attrgetter('kind', 'count')
        self.my_tiles.sort(key=sort_kind_count)
        return self.my_tiles

    def vis_my_tiles(self):
        print(f"Player {self.name}:\n" + tile_vis(self.get_my_tiles()))


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None


class Chain(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def add(self, value):
        # 添加至头部
        tmp_node = Node(value)
        if self.is_empty():
            self._head = tmp_node
            tmp_node.next = self._head
        else:
            tmp_node.next = self._head
            cur = self._head
            while cur.next != self._head:
                cur = cur.next
            cur.next = tmp_node
            self._head = tmp_node

    def append(self, value):
        # 添加至尾部
        tmp_node = Node(value)
        if self.is_empty():
            self._head = tmp_node
            tmp_node.next = self._head
        else:
            cur = self._head
            while cur.next != self._head:
                cur = cur.next
            cur.next = tmp_node
            tmp_node.next = self._head

    def travel(self):
        if self.is_empty():
            return
        cur = self._head
        print(cur.value)
        while cur.next != self._head:
            cur = cur.next
            print(cur.value)


def helper_generate_one_kind_tiles(kind):
    """
    Simply generate all tiles of one individual kind.

    :param kind: can be bing/ tiao/ wan
    :returns: temp_list is the list of all tiles in one kind.
    """
    temp_list = []
    for i in range(0, 36):
        temp_count = int(i / 4) + 1
        temp_list.append(Tile(temp_count, kind))
        # temp_list.append(Tile(temp_count, kind).what())
    return temp_list


def tile_vis(tiles):
    vis_str_l1 = ""
    vis_str_l2 = ""
    vis_str_l3 = ""
    vis_str_l4 = ""
    for item in tiles:
        tmp_str = item.vis().split('\n')
        vis_str_l1 = vis_str_l1 + tmp_str[0] + '  '
        vis_str_l2 = vis_str_l2 + tmp_str[1] + '  '
        vis_str_l3 = vis_str_l3 + tmp_str[2] + '  '
        vis_str_l4 = vis_str_l4 + tmp_str[3] + '  '
    vis_str = vis_str_l1 + '\n' + vis_str_l2 + '\n' + vis_str_l3 + '\n' + vis_str_l4
    return vis_str


def tile_names(tiles):
    if isinstance(tiles, list):
        tmp_tiles_list = []
        for item in tiles:
            tmp_tiles_list.append(item.what())
        return tmp_tiles_list
    elif isinstance(tiles, Tile):
        return tiles.what()
    else:
        print('Invalid data type!')


def toss_a_dice():
    # TODO: 用来定义摸牌位置和换牌方向，暂时没用。
    return random.randint(1, 6)


def init_game():
    """
    This function initializes 4 Player objects with 100 points each, and all of the tiles. There
    are 3*4*9 = 108 tiles in total.

    :returns: p1 ~ p4 are the four players.
    :returns: all_tiles is the list of every Tile objects in one game.
    """
    # TODO: 目前先设定为游戏只可以进行一局。
    kinds = ['bing', 'tiao', 'wann']
    tmp_dealer_list = [False, False, False, False]
    # 决定谁是庄家
    tmp_dealer_list[random.randint(0, 3)] = True
    p1 = Player(1, 100, tmp_dealer_list[0])
    p2 = Player(2, 100, tmp_dealer_list[1])
    p3 = Player(3, 100, tmp_dealer_list[2])
    p4 = Player(4, 100, tmp_dealer_list[3])
    # 生成好所有的牌
    all_tiles = helper_generate_one_kind_tiles(kinds[0]) + \
                helper_generate_one_kind_tiles(kinds[1]) + \
                helper_generate_one_kind_tiles(kinds[2])
    # 开始第一轮发牌
    now_tiles = all_tiles
    for i in range(3):
        for j in range(4):
            now_tiles = p1.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = p2.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = p3.draw_a_tile(now_tiles)
        for j in range(4):
            now_tiles = p4.draw_a_tile(now_tiles)
    # 跳牌
    tmp_player_list = [p1, p2, p3, p4]
    for p in tmp_player_list:
        if p.if_dealer:
            # 庄家取两张牌
            now_tiles = p.draw_a_tile(now_tiles)
            now_tiles = p.draw_a_tile(now_tiles)
        else:
            # 非庄家只取一张牌
            now_tiles = p.draw_a_tile(now_tiles)
    return p1, p2, p3, p4, now_tiles


def main():
    start_time = time.time()

    player1, player2, player3, player4, now_tiles = init_game()
    # -------------------------------------------------------
    # print(tile_names(tmp_list))
    # player1.vis_my_tiles()
    # player2.vis_my_tiles()
    # player3.vis_my_tiles()
    # player4.vis_my_tiles()
    while len(now_tiles) is not 0:
        now_tiles = player4.draw_a_tile(now_tiles)
        # print(len(now_tiles))
        print(player4.discard_a_tile().vis())
    end_time = time.time()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
