# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:26:17
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-09 06:46:09

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flows, Node, Buffer
import math

class BinaryBlock(Algorithm):
    def __init__(self, dual: bool = False, shifted: bool = False):
        self.dual: bool = dual
        self.shifted: bool = shifted
        self.name: str = 'Hd' + ('_dual' if dual else '') + ('_shifted' if shifted else '')

    def dualXor(self, rank: int, step: int, nranks: int, dual: bool) -> int:
        if (rank & (1 << step)) == 0:
            peer: int = rank - (1 << step) if dual else rank + (1 << step)
        else:
            peer: int = rank + (1 << step) if dual else rank - (1 << step)
        return (peer + nranks) % nranks

    def dualHalf(self, rank: int, step: int, dual: bool) -> bool:
        half: bool = (rank & (1 << step)) != 0
        return half ^ dual

    def initialize(self, topo: UniformLayeredTopo):
        topo.setBuffer(1 << (topo.nintersteps + topo.nintrasteps))

    def getFlow(self, node: Node, topo: UniformLayeredTopo, flow: Flows):
        sendOffset: int = 0
        recvOffset: int = 0

        # We must yield our send before recv
        # Intra Reduce to Power of 2
        if node.intraRank >= (1 << topo.nintrasteps):
            buffer: Buffer = node.buffer
            peer: int = topo.getRank(node.interRank, node.intraRank - (1 << topo.nintrasteps))
            node.send(topo.nodes[peer], buffer, flow)
        yield node.step
        if node.intraRank + (1 << topo.nintrasteps) < topo.nintraRanks:
            peer: int = topo.getRank(node.interRank, node.intraRank + (1 << topo.nintrasteps))
            node.recv(topo.nodes[peer], flow)
        yield node.step
        if (1 << topo.nintrasteps) < topo.nintraRanks:
            node.updateStep()

        # Intra Reduce Scatter
        for step in range(topo.nintrasteps):
            intraPeer: int = self.dualXor(node.intraRank, step, 1 << topo.nintrasteps, dual=False)
            peer: int = topo.getRank(node.interRank, intraPeer)
            halvingSlice: int = 1 << (topo.nintrasteps + topo.nintersteps - step - 1)
            if node.intraRank < (1 << topo.nintrasteps):
                sendOffset = recvOffset + (halvingSlice if node.intraRank < intraPeer else 0)
                buffer: Buffer = node.buffer.selectSlices(sendOffset, sendOffset + halvingSlice)
                node.send(topo.nodes[peer], buffer, flow)
            yield node.step
            if node.intraRank < (1 << topo.nintrasteps):
                recvOffset = recvOffset + (halvingSlice if node.intraRank >= intraPeer else 0)
                node.recv(topo.nodes[peer], flow)
            yield node.step
            node.updateStep()

        # Inter Reduce to Power of 2
        reducedInterSteps = 1 << topo.nintersteps
        if node.interRank >= (1 << topo.nintersteps):
            buffer: Buffer = node.buffer.selectSlices(begin, end)
            shiftedRank: int = (node.interRank + node.intraRank) if self.shifted else node.interRank
            peer: int = topo.getRank(shiftedRank % reducedInterSteps, node.intraRank)
            node.send(topo.nodes[peer], buffer, flow)
        yield node.step
        shiftedRank: int = (node.interRank - node.intraRank) % reducedInterSteps if self.shifted else node.interRank
        if node.interRank < reducedInterSteps and shiftedRank + (1 << topo.nintersteps) < topo.ninterRanks:
            peer: int = topo.getRank(shiftedRank + reducedInterSteps, node.intraRank)
            node.recv(topo.nodes[peer], flow)
        yield node.step
        if (1 << topo.nintersteps) < topo.ninterRanks:
            node.updateStep()

        # Inter Reduce Scatter
        dual: bool = self.dual and node.intraRank >= (1 << (topo.nintrasteps - 1))
        for step in range(topo.nintersteps):
            shiftedStep = (step + node.intraRank) % topo.nintersteps if self.shifted else step
            interPeer: int = self.dualXor(node.interRank, shiftedStep, 1 << topo.nintersteps, dual)
            peer: int = topo.getRank(interPeer, node.intraRank)
            halvingSlice: int = 1 << (topo.nintersteps - step - 1)
            if node.interRank < (1 << topo.nintersteps):
                sendOffset = recvOffset + (halvingSlice if self.dualHalf(node.interRank, shiftedStep, dual) else 0)
                buffer: Buffer = node.buffer.selectSlices(sendOffset, sendOffset + halvingSlice)
                node.send(topo.nodes[peer], buffer, flow)
                node.print(f'node send from {sendOffset} to {sendOffset + halvingSlice}')
            yield node.step
            if node.interRank < (1 << topo.nintersteps):
                recvOffset = recvOffset + (halvingSlice if not self.dualHalf(node.interRank, shiftedStep, dual) else 0)
                node.recv(topo.nodes[peer], flow)
                node.print(f'node recv from {recvOffset} to {recvOffset + halvingSlice}')
            yield node.step
            node.updateStep()
        # if node.rank < (1 << topo.nintersteps):
        #     print(f'node {node.rank}')
        #     print(node.buffer.buffer)
        if node.interRank < (1 << topo.nintersteps) and max(node.buffer.buffer.sum(axis=1)) < topo.nranks:
            node.print(f'{node.buffer}')
            print(node.log)
        yield