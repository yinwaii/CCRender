# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 16:28:28
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-07 15:42:07

from .Topo import Topo
from .Node import Node

class UniformLayeredTopo(Topo):
    def __init__(self, ninterRanks: int, nintraRanks: int):
        self.ninterRanks: int = ninterRanks
        self.nintraRanks: int = nintraRanks
        self.nranks: int = ninterRanks * nintraRanks
        self.name: str = f'{self.ninterRanks}x{self.nintraRanks}'
        self.nodes: list(Node) = [Node(i) for i in range(self.nranks)]

    def getIntraRank(self, rank: int) -> int:
        return rank % self.nintraRanks

    def getInterRank(self, rank: int) -> int:
        return rank // self.nintraRanks

    def getRank(self, interRank: int, intraRank: int) -> int:
        return interRank * self.nintraRanks + intraRank