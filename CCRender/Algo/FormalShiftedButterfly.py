# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 20:14:29
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 23:52:58

from .Algorithm import Algorithm
from CCRender.Topo import UniformLayeredTopo, Flow
import math

class FormalShiftedButterfly(Algorithm):
    def __init__(self):
        self.name: str = 'UniShd'

    def commRecord(self, topo: UniformLayeredTopo) -> list(Flow(int, int, int)):
        nintraSteps: int = int(math.log2(topo.nintraRanks))
        ninterSteps: int = int(math.log2(topo.ninterRanks))
        miniNintraSteps: int = int(math.log2(ninterSteps))
        miniNinterSteps: int = 1 << miniNintraSteps
        stepCnt: int = 0
        res: list(Flow(int, int, int)) = []
        for intraRank in range(topo.nintraRanks - 1, (1 << nintraSteps) - 1, -1):
            for interRank in range(topo.ninterRanks):
                rank: int = topo.getRank(interRank, intraRank)
                peer: int = topo.getRank(interRank, intraRank - (1 << nintraSteps))
                res.append(Flow(stepCnt, rank, peer))
        if (1 << nintraSteps) != topo.nintraRanks:
            stepCnt += 1
        for step in range(nintraSteps):
            for intraRank in range(1 << nintraSteps):
                for interRank in range(topo.ninterRanks):
                    rank: int = topo.getRank(interRank, intraRank)
                    peer: int = topo.getRank(interRank, intraRank ^ (1 << step))
                    res.append(Flow(stepCnt, rank, peer))
            stepCnt += 1
        for interRank in range(topo.ninterRanks - 1, (1 << ninterSteps) - 1, -1):
            for intraRank in range(1 << nintraSteps):
                rank: int = topo.getRank(interRank, intraRank)
                destnInterRank: int = 1 << ninterSteps
                peer: int = topo.getRank((interRank - destnInterRank + intraRank) % destnInterRank, intraRank)
                res.append(Flow(stepCnt, rank, peer))
        if (1 << ninterSteps) != topo.ninterRanks:
            stepCnt += 1
        for step in range(miniNinterSteps):
            for intraRank in range(1 << nintraSteps):
                for interRank in range(1 << ninterSteps):
                    rank: int = topo.getRank(interRank, intraRank)
                    peer: int = topo.getRank(interRank ^ (1 << ((step + intraRank) % miniNinterSteps)), intraRank)
                    res.append(Flow(stepCnt, rank, peer))
            stepCnt += 1
        for step in range(ninterSteps - miniNinterSteps):
            for intraRank in range(1 << nintraSteps):
                for interRank in range(1 << ninterSteps):
                    rank: int = topo.getRank(interRank, intraRank)
                    peer: int = topo.getRank(interRank ^ (1 << (step + miniNinterSteps)), intraRank)
                    res.append(Flow(stepCnt, rank, peer))
            stepCnt += 1
        return res