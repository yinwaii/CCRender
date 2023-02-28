# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:57
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 11:23:53

from CCRender.Topo import Topo
from CCRender.Algo import Algorithm
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
        os.system(f"echo '{template}' > log/{filename}.dot")
        os.system(f"echo '{template}' | neato -Tpng -o fig/{filename}.png")

    def visual(self, withStep: bool = False) -> None:
        template = self.genDot(self.genNode(), self.genEdge())
        self.genPng(template, f'{self.algo.name}_{self.topo.nranks}')
        if withStep:
            for step in range(self.maxStep + 1):
                template = self.genDot(self.genNode(), self.genEdge(step))
                self.genPng(
                    template,
                    f'{self.algo.name}_{self.topo.nranks}_{step}')
