# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:57
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 14:13:50

from CCRender.Topo import Topo
from CCRender.Algo import Algorithm
import os

class Diagram():
    def __init__(self, topo: Topo, algo: Algorithm):
        self.topo: Topo = topo
        self.algo: Algorithm = algo
        self.flows: list(Flow) = algo.commRecord(topo)
        self.maxStep: int = max([node.step for node in self.topo.nodes]) - 1
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

    def genPng(self, template: str, pathname: str, filename: str) -> str:
        if not os.path.exists(f'fig/{pathname}'):
            os.makedirs(f'fig/{pathname}')
        if not os.path.exists(f'log/{pathname}'):
            os.makedirs(f'log/{pathname}')
        os.system(f"echo '{template}' > log/{pathname}/{filename}.dot")
        os.system(f"echo '{template}' | neato -Tpdf -o fig/{pathname}/{filename}.pdf &")

    def visual(self, withStep: bool = False) -> None:
        template = self.genDot(self.genNode(), self.genEdge())
        filename = f'{self.algo.name}_{self.topo.name}_{self.name}'
        pathname = f'{self.topo.name}/{self.name}/'
        self.genPng(template, pathname, filename)
        if withStep:
            pathname = f'{pathname}/steps/{self.algo.name}'
            for step in range(self.maxStep + 1):
                template = self.genDot(self.genNode(), self.genEdge(step))
                self.genPng(template, pathname, f'{filename}_{step}')
