# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:25:48
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 11:31:39

from .Algorithm import Algorithm
from CCRender.Topo import Topo, Flow

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