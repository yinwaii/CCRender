# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-03-06 11:22:14
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 10:43:34

from .Buffer import Buffer
from .Flow import Flows
import numpy as np

class Node:
    def __init__(self, rank: int):
        self.rank: int = rank
        self.step: int = 0
        self.buffer: Buffer = Buffer()

    def __repr__(self) -> str:
        return f'Node {self.rank}'
        
    def send(self, peer: 'Node', buffer: Buffer, flow: Flows):
        print(f'send: {self.rank} -> {peer.rank}')
        flow.addFlow(self.step, self.rank, peer.rank, buffer)

    def recv(self, peer: 'Node', flow: Flows):
        print(f'recv: {self.rank} <- {peer.rank}')
        buffer: np.ndarray = flow.checkFlow(self.step, peer.rank, self.rank)
        self.buffer.buffer += buffer.buffer

    def updateStep(self):
        self.step += 1
        # print(f'node {self.rank} in step {self.step}')
        # print(self.buffer.buffer)