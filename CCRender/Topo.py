# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:24:52
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:17:27

import math

class Topo():
    def __init__(self, nranks: int):
        self.nranks: int = nranks
        self.name: str = f'{self.nranks}'


class UniformLayeredTopo(Topo):
    def __init__(self, ninterRanks: int, nintraRanks: int):
        self.ninterRanks: int = ninterRanks
        self.nintraRanks: int = nintraRanks
        self.nranks: int = ninterRanks * nintraRanks
        self.name: str = f'{self.ninterRanks}x{self.nintraRanks}'

    def getIntraRank(self, rank: int) -> int:
        return rank % self.nintraRanks

    def getInterRank(self, rank: int) -> int:
        return rank // self.nintraRanks

    def getRank(self, interRank: int, intraRank: int) -> int:
        return interRank * self.nintraRanks + intraRank


class Flow():
    def __init__(self, step: int, send: int, recv: int):
        self.step: int = step
        self.send: int = send
        self.recv: int = recv

    def __iter__(self):
        return iter((self.step, self.send, self.recv))

    def __next__(self):
        return next((self.step, self.send, self.recv))

    def __hash__(self):
        return hash(self.step) ^ hash(self.send) ^ hash(self.recv)

    def __eq__(self, other):
        return self.step == other.step and self.send == other.send and self.recv == other.recv

    def __repr__(self):
        return f'Flow({self.step}, {self.send}, {self.recv})'