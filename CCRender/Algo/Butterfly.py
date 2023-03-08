# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:26:17
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 14:12:21

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flows, Node, Buffer
import math

class Butterfly(Algorithm):
    def __init__(self, dual: bool = False, shifted: bool = False):
        self.dual: bool = dual
        self.shifted: bool = shifted
        self.name: str = 'Hd' + ('_dual' if dual else '') + ('_shifted' if shifted else '')

    def dualXor(self, rank: int, step: int, nranks: int, dual: bool) -> int:
        if rank & (1 << step) == 0:
            peer: int = rank - (1 << step) if dual else rank + (1 << step)
        else:
            peer: int = rank + (1 << step) if dual else rank - (1 << step)
        return (peer + nranks) % nranks

    def dualHalf(self, rank: int, step: int, dual: bool) -> bool:
        return rank & (1 << step) == (1 if dual else 0)

    def initialize(self, topo: UniformLayeredTopo):
        nintersteps: int = int(math.log2(topo.ninterRanks))
        nintrasteps: int = int(math.log2(topo.nintraRanks))
        topo.setBuffer(1 << (nintersteps + nintrasteps))

    def getFlow(self, node: Node, topo: UniformLayeredTopo, flow: Flows):
        intraRank: int = topo.getIntraRank(node.rank)
        interRank: int = topo.getInterRank(node.rank)
        nintersteps: int = int(math.log2(topo.ninterRanks))
        nintrasteps: int = int(math.log2(topo.nintraRanks))
        sendOffset: int = 0
        recvOffset: int = 0
        begin: int = 0
        end: int = 1 << (nintrasteps + nintersteps)

        # We must yield our send before recv

        # Intra Reduce to Power of 2
        if intraRank >= (1 << nintrasteps):
            buffer: Buffer = node.buffer
            peer: int = topo.getRank(interRank, intraRank - (1 << nintrasteps))
            node.send(topo.nodes[peer], buffer, flow)
        yield node.step
        if intraRank + (1 << nintrasteps) < topo.nintraRanks:
            peer: int = topo.getRank(interRank, intraRank + (1 << nintrasteps))
            node.recv(topo.nodes[peer], flow)
        yield node.step
        if (1 << nintrasteps) < topo.nintraRanks:
            node.updateStep()

        # Intra Reduce Scatter
        for step in range(nintrasteps):
            intraPeer: int = self.dualXor(intraRank, step, 1 << nintrasteps, dual=False)
            peer: int = topo.getRank(interRank, intraPeer)
            halvingSlice: int = 1 << (nintrasteps + nintersteps - step - 1)
            if intraRank < (1 << nintrasteps):
                sendOffset = recvOffset + (halvingSlice if intraRank < intraPeer else 0)
                buffer: Buffer = node.buffer.selectSlices(sendOffset, sendOffset + halvingSlice)
                node.send(topo.nodes[peer], buffer, flow)
            yield node.step
            if intraRank < (1 << nintrasteps):
                recvOffset = recvOffset + (halvingSlice if intraRank >= intraPeer else 0)
                node.recv(topo.nodes[peer], flow)
            yield node.step
            node.updateStep()

        # Inter Reduce to Power of 2
        reducedInterSteps = 1 << nintersteps
        if interRank >= (1 << nintersteps):
            buffer: Buffer = node.buffer.selectSlices(begin, end)
            shiftedRank: int = (interRank + intraRank) if self.shifted else interRank
            peer: int = topo.getRank(shiftedRank % reducedInterSteps, intraRank)
            node.send(topo.nodes[peer], buffer, flow)
        yield node.step
        shiftedRank: int = (interRank - intraRank) % reducedInterSteps if self.shifted else interRank
        if interRank < reducedInterSteps and shiftedRank + (1 << nintersteps) < topo.ninterRanks:
            peer: int = topo.getRank(shiftedRank + reducedInterSteps, intraRank)
            node.recv(topo.nodes[peer], flow)
        yield node.step
        if (1 << nintersteps) < topo.ninterRanks:
            node.updateStep()

        # Inter Reduce Scatter
        dual: bool = self.dual and intraRank >= (1 << (nintrasteps - 1))
        for step in range(nintersteps):
            shiftedStep = (step + intraRank) % nintersteps if self.shifted else step
            interPeer: int = self.dualXor(interRank, shiftedStep, 1 << nintersteps, dual)
            peer: int = topo.getRank(interPeer, intraRank)
            halvingSlice: int = 1 << (nintersteps - step - 1)
            if interRank < (1 << nintersteps):
                sendOffset = recvOffset + (halvingSlice if self.dualHalf(interRank, shiftedStep, dual) else 0)
                buffer: Buffer = node.buffer.selectSlices(sendOffset, sendOffset + halvingSlice)
                node.print(f'node send from {sendOffset} to {sendOffset + halvingSlice}')
                node.send(topo.nodes[peer], buffer, flow)
            yield node.step
            if interRank < (1 << nintersteps):
                recvOffset = recvOffset + (halvingSlice if not self.dualHalf(interRank, shiftedStep, dual) else 0)
                node.print(f'node recv from {recvOffset} to {recvOffset + halvingSlice}')
                node.recv(topo.nodes[peer], flow)
            yield node.step
            node.updateStep()
        # if node.rank < (1 << nintersteps):
        #     print(f'node {node.rank}')
        #     print(node.buffer.buffer)
        if (dual and node.rank % 2):
            print(node.log)
        yield