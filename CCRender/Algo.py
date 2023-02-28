# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:36
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 10:29:16

from CCRender.Topo import *

class Algorithm():
    def commRecord(self, topo: Topo) -> list(Flow(int, int, int)):
        return list()


class Ring(Algorithm):
    def __init__(self):
        self.name: str = 'Ring'

    def commRecord(self, topo: Topo) -> list(Flow(int, int, int)):
        res: list(Flow(int, int, int)) = []
        for rank in range(topo.nranks):
            for step in range(topo.nranks):
                peer: int = (rank + 1) % topo.nranks
                res.append(Flow(step, rank, peer))
        return res


class Butterfly(Algorithm):
    def __init__(self):
        self.name: str = 'Hd'

    def commRecord(self,
                   topo: UniformLayeredTopo) -> list(Flow(int, int, int)):
        assert (2**int(math.log2(topo.ninterRanks)) == topo.ninterRanks)
        assert (2**int(math.log2(topo.nintraRanks)) == topo.nintraRanks)
        res: list(Flow(int, int, int)) = []
        for rank in range(topo.nranks):
            for step in range(int(math.log2(topo.nranks))):
                peer: int = rank ^ (1 << step)
                res.append(Flow(step, rank, peer))
        return res


class ShiftedButterfly(Algorithm):
    def __init__(self):
        self.name: str = 'Shd'

    def commRecord(self,
                   topo: UniformLayeredTopo) -> list(Flow(int, int, int)):
        assert (2**int(math.log2(topo.ninterRanks)) == topo.ninterRanks)
        assert (2**int(math.log2(topo.nintraRanks)) == topo.nintraRanks)
        res: list(Flow(int, int, int)) = []
        nintraSteps = int(math.log2(topo.nintraRanks))
        ninterSteps = int(math.log2(topo.ninterRanks))
        for rank in range(topo.nranks):
            for step in range(nintraSteps):
                peer: int = rank ^ (1 << step)
                res.append(Flow(step, rank, peer))
            for step in range(ninterSteps):
                peer: int = rank ^ (1 << (
                    (step + topo.getIntraRank(rank)) % ninterSteps +
                    nintraSteps))
                res.append(Flow(step + nintraSteps, rank, peer))
        return res