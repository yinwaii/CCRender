# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:26:17
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 19:23:06

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flow
import math

class Butterfly(Algorithm):
    def __init__(self):
        self.name: str = 'Hd'

    def commRecord(self, topo: UniformLayeredTopo) -> list(Flow(int, int, int)):
        nintersteps: int = int(math.log2(topo.ninterRanks))
        nintrasteps: int = int(math.log2(topo.nintraRanks))
        stepCnt: int = 0
        res: list(Flow(int, int, int)) = []
        for intraRank in range(topo.nintraRanks - 1, (1 << nintrasteps) - 1, -1):
            for interRank in range(topo.ninterRanks):
                rank: int = topo.getRank(interRank, intraRank)
                peer: int = topo.getRank(interRank, intraRank - (1 << nintrasteps))
                res.append(Flow(stepCnt, rank, peer))
        if (1 << nintrasteps) != topo.nintraRanks:
            stepCnt += 1
        for step in range(nintrasteps):
            for intraRank in range(1 << nintrasteps):
                for interRank in range(topo.ninterRanks):
                    rank: int = topo.getRank(interRank, intraRank)
                    peer: int = topo.getRank(interRank, intraRank ^ (1 << step))
                    res.append(Flow(stepCnt, rank, peer))
            stepCnt += 1
        for interRank in range(topo.ninterRanks - 1, (1 << nintersteps) - 1, -1):
            for intraRank in range(1 << nintrasteps):
                rank: int = topo.getRank(interRank, intraRank)
                peer: int = topo.getRank(interRank - (1 << nintersteps), intraRank)
                res.append(Flow(stepCnt, rank, peer))
        if (1 << nintersteps) != topo.ninterRanks:
            stepCnt += 1
        for step in range(nintersteps):
            for intraRank in range(1 << nintrasteps):
                for interRank in range(1 << nintersteps):
                    rank: int = topo.getRank(interRank, intraRank)
                    peer: int = topo.getRank(interRank ^ (1 << step), intraRank)
                    res.append(Flow(stepCnt, rank, peer))
            stepCnt += 1
        return res
