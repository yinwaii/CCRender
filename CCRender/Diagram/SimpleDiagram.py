# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:19:29
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 18:54:40

from .Diagram import Diagram
from CCRender.Topo import Topo
from CCRender.Algo import Algorithm
import math

class SimpleDiagram(Diagram):
    def __init__(self, topo: Topo, algo: Algorithm):
        super().__init__(topo, algo)
        self.name: str = 'Simple'

    def genNodeInfo(self, rank: int) -> str:
        radius: int = self.topo.nranks // 4
        calcX = lambda rank: round(math.cos(math.pi * 2 * rank / self.topo.nranks) * radius, 3)
        calcY = lambda rank: round(math.sin(math.pi * 2 * rank / self.topo.nranks) * radius, 3)
        calcStr = lambda rank: f'{rank} [label="{rank}", pos="{calcX(rank)},{calcY(rank)}!"]'
        return calcStr(rank)

    def genNode(self) -> str:
        resList: list(str) = [self.genNodeInfo(rank) for rank in range(self.topo.nranks)]
        return '\n'.join(resList)

    def genEdge(self, step: int = None) -> str:
        calcStr = lambda flow: f'{flow.send} -> {flow.recv} [color={(flow.step) % self.colorNum + 1}];'
        if step is not None:
            resList: list(str) = [calcStr(flow) for flow in self.flows if flow.step == step]
        else:
            resList: list(str) = [calcStr(flow) for flow in self.flows]
        return '\n'.join(resList)