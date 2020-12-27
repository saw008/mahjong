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


class Tile(object):
    def __init__(self, count, kind):
        self.__count = str(count)
        self.__kind = kind

    @property
    def kind(self):
        return self.__kind

    def what(self):
        return self.__count + '_' + self.__kind

    def vis(self):
        return f"*---*\n| {self.__count} |\n| {self.__kind[0].upper()} |\n*---*"


class Player(object):
    # 原来想要继承Node类，现在感觉并不需要，直接把Node实例化之后把val设为Player实例就可以了。
    def __init__(self, name, score, if_dealer):
        self.__name = str(name)
        self.__score = score
        self.__if_dealer = if_dealer
        self.__my_tiles = list()
        self.__my_tiles_status = {}

    @property
    def score(self):
        return self.__score

    @property
    def if_dealer(self):
        return self.__if_dealer

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
        self.__my_tiles.append(temp_tile)
        self.sort_my_tiles()  # 在每次取牌之后整理手牌
        return now_tiles_on_board

    def discard_a_tile(self):
        # TODO: 目前是随机打出一张牌，显然不合理，但以后再改
        temp_tile = random.sample(self.__my_tiles, 1)[0]

        self.__my_tiles.remove(temp_tile)
        self.sort_my_tiles()  # 在每次打牌之后整理手牌
        return temp_tile

    def get_my_tiles(self):
        return self.__my_tiles

    def sort_my_tiles(self):
        # TODO: now too complicated
        sort_kind_count = operator.attrgetter('kind', 'count')
        self.__my_tiles.sort(key=sort_kind_count)
        tmp_w, tmp_b, tmp_t = 0, 0, 0
        for one_tile in self.__my_tiles:
            if one_tile.kind == 'wann':
                tmp_w += 1
            elif one_tile.kind == 'tiao':
                tmp_t += 1
            elif one_tile.kind == 'bing':
                tmp_b += 1
        self.__my_tiles_status.update({'w': tmp_w,
                                       'b': tmp_b,
                                       't': tmp_t})
        print(self.__my_tiles_status)
        return self.__my_tiles

    def vis_my_tiles(self):
        print(f"Player {self.__name}:\n" + tile_vis(self.get_my_tiles()))


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None


class Chain(object):
    def __init__(self):
        self._head = None
        self.cursor = None

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
        tmp = cur.value
        while cur.next != self._head:
            cur = cur.next
            print(cur.value)
        return tmp

    def go(self):
        if self.cursor is None:
            self.cursor = self._head
        tmp = self.cursor.value
        self.cursor = self.cursor.next
        return tmp  # 返回的是当前要出牌的玩家


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
    # 开始初始发牌
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
    circle = Chain()
    for p in tmp_player_list:
        if p.if_dealer:
            # 庄家取两张牌
            now_tiles = p.draw_a_tile(now_tiles)
            now_tiles = p.draw_a_tile(now_tiles)
        else:
            # 非庄家只取一张牌
            now_tiles = p.draw_a_tile(now_tiles)

    # 生成打牌方向
    # TODO: 现在的方法太过复杂，但可以用。
    # tmp_adding_list = [p1, p2, p3, p4, p1, p2, p3]
    tmp_adding_list = [p4, p3, p2, p1, p4, p3, p2]  # 逆打
    tmp_counter = 0
    for item in tmp_adding_list:
        if item.if_dealer:
            circle.append(item)
            tmp_counter += 1
        if (not item.if_dealer) and tmp_counter >= 1:
            circle.append(item)
            tmp_counter += 1
        if tmp_counter == 4:
            break
    return p1, p2, p3, p4, now_tiles, circle
