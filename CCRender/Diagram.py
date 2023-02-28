# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:57
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 10:30:20

from CCRender.Topo import *
from CCRender.Algo import *
import os

class Diagram():
    def __init__(self, topo: Topo, algo: Algorithm):
        self.topo: Topo = topo
        self.algo: Algorithm = algo
        self.flows: list(Flow(int, int, int)) = algo.commRecord(topo)
        self.maxStep = max([flow.step for flow in self.flows])

    def genDot(self, nodeStr: str, edgeStr: str) -> str:
        template = f'''
          digraph G {{
          edge [colorscheme=set19]
          labeljust=l
          {nodeStr}
          {edgeStr}
          }}
          '''
        return template

    def genPng(self, template: str, filename: str) -> str:
        os.system(f"echo '{template}' | fdp -Tpng -o {filename}")

    def visual(self, withStep: bool = False) -> None:
        template = self.genDot(self.genNode(), self.genEdge())
        self.genPng(template, f'fig/{self.algo.name}_{self.topo.nranks}.png')
        if withStep:
            for step in range(self.maxStep + 1):
                template = self.genDot(self.genNode(), self.genEdge(step))
                self.genPng(
                    template,
                    f'fig/{self.algo.name}_{self.topo.nranks}_{step}.png')


class SimpleDiagram(Diagram):
    def __init__(self, topo: Topo, algo: Algorithm):
        super().__init__(topo, algo)

    def genNode(self) -> str:
        radius: int = self.topo.nranks // 4
        calcX = lambda rank: round(
            math.cos(math.pi * 2 * rank / self.topo.nranks) * radius, 3)
        calcY = lambda rank: round(
            math.sin(math.pi * 2 * rank / self.topo.nranks) * radius, 3)
        calcOrientation = lambda rank: 360 * rank / self.topo.nranks
        calcStr = lambda rank: f'{rank} [label="{rank}", pos="{calcX(rank)},{calcY(rank)}!", orientation={calcOrientation(rank)}]'
        resList: list(str) = [
            calcStr(rank) for rank in range(self.topo.nranks)
        ]
        return '\n'.join(resList)

    def genEdge(self, step: int = None) -> str:
        calcStr = lambda flow: f'{flow.send} -> {flow.recv} [color={(flow.step) % 9 + 1}];'
        if step is not None:
            resList: list(str) = [
                calcStr(flow) for flow in self.flows if flow.step == step
            ]
        else:
            resList: list(str) = [calcStr(flow) for flow in self.flows]
        return '\n'.join(resList)


class SimpleLayeredDiagram(SimpleDiagram):
    def __init__(self, topo: UniformLayeredTopo, algo: Algorithm):
        super().__init__(topo, algo)
        self.topo: UniformLayeredTopo = topo

    def genNode(self) -> str:
        nodeStr = super().genNode()
        calcIntraLabel = lambda interRank: '\n'.join(
            f'{self.topo.getRank(interRank, intraRank)}'
            for intraRank in range(self.topo.nintraRanks))
        calcCluster = lambda interRank: f'subgraph cluster_{interRank} {{\nlabel="server {interRank}";\n{calcIntraLabel(interRank)}\n}}'
        resList: list(str) = [
            calcCluster(interRank)
            for interRank in range(self.topo.ninterRanks)
        ]
        return nodeStr + '\n' + '\n'.join(resList)


class UniformLayeredDiagram(Diagram):
    def __init__(self, topo: UniformLayeredTopo, algo: Algorithm):
        super().__init__(topo, algo)
        self.topo: UniformLayeredTopo = topo

    def genNode(self) -> str:
        radius: int = self.topo.ninterRanks // 2 * self.topo.nintraRanks // 4
        calcX = lambda x: round(
            math.cos(math.pi * 2 * x / self.topo.ninterRanks) * radius, 3)
        calcY = lambda y: round(
            math.sin(math.pi * 2 * y / self.topo.ninterRanks) * radius, 3)
        calcOrientation = lambda rank: 360 * rank / self.topo.ninterRanks
        calcIntraLabel = lambda interRank, intraRank: f'<{self.topo.getRank(interRank, intraRank)}>{self.topo.getRank(interRank, intraRank)}'
        calcInterLabel = lambda interRank: '|'.join([
            calcIntraLabel(interRank, intraRank)
            for intraRank in range(self.topo.nintraRanks)
        ])
        calcStr = lambda interRank: f'node{interRank} [shape="record", label="{calcInterLabel(interRank)}", pos="{calcX(interRank)},{calcY(interRank)}!", orientation={calcOrientation(interRank)}]'
        resList: list(str) = [
            calcStr(interRank) for interRank in range(self.topo.ninterRanks)
        ]
        return '\n'.join(resList)

    def genEdge(self, step: int = None) -> str:
        calcStr = lambda flow: f'node{self.topo.getInterRank(flow.send)}:{flow.send}:s -> node{self.topo.getInterRank(flow.recv)}:{flow.recv}:s [color={(flow.step) % 9 + 1}];'
        if step is not None:
            resList: list(str) = [
                calcStr(flow) for flow in self.flows if flow.step == step
            ]
        else:
            resList: list(str) = [calcStr(flow) for flow in self.flows]
        return '\n'.join(resList)