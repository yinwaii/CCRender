# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:26:17
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 11:31:31

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flow
import math

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
