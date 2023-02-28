# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 16:28:28
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:29:12

from .Topo import Topo

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