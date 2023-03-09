# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:26:38
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-09 12:49:54

from CCRender.Topo import *
from CCRender.Algo import *
from CCRender.Diagram import *

if __name__ == '__main__':
    for rank in range(16, 17):
        topo = UniformLayeredTopo(ninterRanks=rank, nintraRanks=8)
        for algo in [Butterfly(shifted = False, dual=False), Butterfly(shifted=True, dual=False), Butterfly(shifted=False, dual=True), Butterfly(shifted=True, dual=True)]:
            for diagram in [UniformLayeredDiagram(topo, algo)]:
                withStep = algo.name != 'Ring'
                diagram.visual(withStep)