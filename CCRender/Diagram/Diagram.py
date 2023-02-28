# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:57
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:19:54

from CCRender.Topo import Topo
from CCRender.Algo import Algorithm
import os

class Diagram():
    def __init__(self, topo: Topo, algo: Algorithm):
        self.topo: Topo = topo
        self.algo: Algorithm = algo
        self.flows: list(Flow(int, int, int)) = algo.commRecord(topo)
        self.maxStep: int = max([flow.step for flow in self.flows])
        self.colorNum: int = 8
        self.name: str = ''

    def genDot(self, nodeStr: str, edgeStr: str) -> str:
        template = f'''
digraph G {{
edge [colorscheme=dark28]
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
        filename = f'{self.algo.name}_{self.topo.name}_{self.name}'
        self.genPng(template, filename)
        if withStep:
            for step in range(self.maxStep + 1):
                template = self.genDot(self.genNode(), self.genEdge(step))
                self.genPng(template, f'{filename}_{step}')
