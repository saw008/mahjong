"""
This program is a simulation of the Chinese board game called Mahjong.

Author: Hao Li, Qi Zhao
Email: hxl1033@case.edu, molitsta@gmail.com
Created: 2020-12-25 23:00
Last modified: now
"""
import random


class Tile(object):
    def __init__(self, count, kind):
        self.count = str(count)
        self.kind = kind

    def what(self):
        return self.count + '_' + self.kind

    def vis(self):
        return f"*---*\n| {self.count} |\n| {self.kind[0].upper()} |\n*---*"


class TileWall(object):
    def __init__(self):
        self.pair = None
        self.winning_tile = None
        self.triplet = None
        self.sequence = None


class Player(object):
    def __init__(self, name, score, if_dealer):
        self.name = str(name)
        self.score = score
        self.if_dealer = if_dealer
        self.my_tiles = []

    def win(self):
        pass

    def draw(self, now_tiles: list):
        self.my_tiles.append(now_tiles.pop())

    def discard(self):
        pass

    def exposed_gang(self):
        pass

    def concealed_gang(self):
        pass

    def peng(self):
        pass

    def gang(self):
        pass


class Board(object):
    def __init__(self):
        self.__now_tiles = self.__one_kind_tiles('wann') + \
                         self.__one_kind_tiles('tiao') + \
                         self.__one_kind_tiles('bing')
        random.shuffle(self.__now_tiles)

    @property
    def now_tiles(self):
        return self.__now_tiles

    @now_tiles.setter
    def now_tiles(self, new_now_tiles):
        self.__now_tiles = new_now_tiles

    def fa_pai(self):
        pass

    # 荒局，没有人赢
    def huang_ju(self):
        pass

    @staticmethod
    def __one_kind_tiles(kind):
        """
            Simply generate all tiles of one individual kind.

            :param kind: can be bing/ tiao/ wann
            :returns: temp_list is the list of all tiles in one kind.
            """
        temp_list = []
        for i in range(0, 36):
            temp_count = int(i / 4) + 1
            temp_list.append(Tile(temp_count, kind))
            # temp_list.append(Tile(temp_count, kind).what())
        return temp_list
