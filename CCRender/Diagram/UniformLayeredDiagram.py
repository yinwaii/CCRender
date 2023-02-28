# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:20:28
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:20:45

from .Diagram import Diagram
from CCRender.Topo import UniformLayeredTopo
from CCRender.Algo import Algorithm
import math


class UniformLayeredDiagram(Diagram):
    def __init__(self, topo: UniformLayeredTopo, algo: Algorithm):
        super().__init__(topo, algo)
        self.topo: UniformLayeredTopo = topo
        self.name: str = 'Uniform'

    def genNode(self) -> str:
        radius: int = self.topo.ninterRanks // 2 * self.topo.nintraRanks // 4
        calcX = lambda x: round(
            math.cos(math.pi * 2 * x / self.topo.ninterRanks) * radius, 3)
        calcY = lambda y: round(
            math.sin(math.pi * 2 * y / self.topo.ninterRanks) * radius, 3)
        calcIntraLabel = lambda interRank, intraRank: f'<{self.topo.getRank(interRank, intraRank)}>{self.topo.getRank(interRank, intraRank)}'
        calcInterLabel = lambda interRank: '|'.join([
            calcIntraLabel(interRank, intraRank)
            for intraRank in range(self.topo.nintraRanks)
        ])
        calcStr = lambda interRank: f'node{interRank} [shape="record", label="{calcInterLabel(interRank)}", pos="{calcX(interRank)},{calcY(interRank)}!"]'
        resList: list(str) = [
            calcStr(interRank) for interRank in range(self.topo.ninterRanks)
        ]
        return '\n'.join(resList)

    def genEdge(self, step: int = None) -> str:
        calcStr = lambda flow: f'node{self.topo.getInterRank(flow.send)}:{flow.send}:s -> node{self.topo.getInterRank(flow.recv)}:{flow.recv}:s [color={(flow.step) % self.colorNum + 1}];'
        if step is not None:
            resList: list(str) = [
                calcStr(flow) for flow in self.flows if flow.step == step
            ]
        else:
            resList: list(str) = [calcStr(flow) for flow in self.flows]
        return '\n'.join(resList)