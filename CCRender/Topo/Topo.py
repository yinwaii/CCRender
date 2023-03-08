# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:24:52
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 10:15:38

from .Node import Node
from .Flow import Flow

class Topo():
    def __init__(self, nranks: int):
        self.nranks: int = nranks
        self.name: str = f'{self.nranks}'
        self.nodes: list(Node) = [Node(i) for i in range(self.nranks)]

    def setBuffer(self, nslices: int):
        for node in self.nodes:
            node.buffer.setBuffer(nslices, self.nranks)
            node.buffer.buffer[:, node.rank] = True
            node.step = 0
        self.slice = nslices