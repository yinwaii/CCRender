# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-03-06 11:22:14
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 13:22:03

from .Buffer import Buffer
from .Flow import Flows
import numpy as np

class Node:
    def __init__(self, rank: int):
        self.rank: int = rank
        self.step: int = 0
        self.buffer: Buffer = Buffer()
        self.log: str = ''
        np.set_printoptions(threshold=np.inf, linewidth=np.inf)

    def __repr__(self) -> str:
        return f'Node {self.rank}'

    def send(self, peer: 'Node', buffer: Buffer, flow: Flows):
        self.print(f'send: {self.rank} -> {peer.rank}')
        flow.addFlow(self.step, self.rank, peer.rank, buffer)

    def recv(self, peer: 'Node', flow: Flows):
        self.print(f'recv: {self.rank} <- {peer.rank}')
        buffer: np.ndarray = flow.checkFlow(self.step, peer.rank, self.rank)
        self.buffer.buffer += buffer.buffer

    def print(self, str: str):
        self.log += str + '\n'

    def updateStep(self):
        self.step += 1
        self.print(f'node {self.rank} in step {self.step}')
        self.print(f'{self.buffer.buffer.astype(int)}')