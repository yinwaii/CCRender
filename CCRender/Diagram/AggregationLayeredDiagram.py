# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:42:53
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 18:54:07

from .Diagram import Diagram
from CCRender.Topo import UniformLayeredTopo, Flow
from CCRender.Algo import Algorithm
import math
import numpy as np


class AggregationLayeredDiagram(Diagram):
    def __init__(self, topo: UniformLayeredTopo, algo: Algorithm):
        super().__init__(topo, algo)
        self.topo: UniformLayeredTopo = topo
        self.name: str = 'Aggregation'

    def genNode(self) -> str:
        radius: int = self.topo.ninterRanks // 2
        calcX = lambda x: round(math.cos(math.pi * 2 * x / self.topo.ninterRanks) * radius, 3)
        calcY = lambda y: round(math.sin(math.pi * 2 * y / self.topo.ninterRanks) * radius, 3)
        calcStr = lambda interRank: f'node{interRank} [pos="{calcX(interRank)},{calcY(interRank)}!"]'
        resList: list(str) = [calcStr(interRank) for interRank in range(self.topo.ninterRanks)]
        return '\n'.join(resList)

    def genEdge(self, step: int = None) -> str:
        flowMatrix: np.array(np.int) = np.zeros((self.topo.ninterRanks, self.topo.ninterRanks, self.maxStep + 1), dtype=np.int)
        for flow in self.flows:
            flowMatrix[self.topo.getInterRank(flow.send), self.topo.getInterRank(flow.recv), flow.step] += 1
        calcStr = lambda flow, freq: f'node{flow.send} -> node{flow.recv} [color={flow.step % self.colorNum + 1}, penwidth={freq}, label="{freq}", fontsize="30", fontcolor={flow.step % self.colorNum + 1},labelfloat="true"];'
        flowSlice = flowMatrix.max(axis=2) if step is None else flowMatrix[:, :, step]
        selectStep = lambda send, recv: flowMatrix.argmax(axis=2)[send, recv] if step is None else step
        resList: list(str) = [calcStr(Flow(selectStep(send, recv), send, recv), flowSlice[send, recv]) for send in range(self.topo.ninterRanks) for recv in range(self.topo.ninterRanks) if flowSlice[send, recv] > 0 and send != recv]
        return '\n'.join(resList)