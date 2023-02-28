# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:26:46
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 11:31:42

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flow
import math

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