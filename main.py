# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:26:38
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 14:10:21

from CCRender.Topo import *
from CCRender.Algo import *
from CCRender.Diagram import *

if __name__ == '__main__':
    topo = UniformLayeredTopo(ninterRanks=16, nintraRanks=8)
    for algo in [Butterfly(), Butterfly(shifted=True), Butterfly(dual=True), Butterfly(shifted=True, dual=True)]:
        for diagram in [SimpleLayeredDiagram(topo, algo), UniformLayeredDiagram(topo, algo), AggregationLayeredDiagram(topo, algo)]:
            withStep = algo.name != 'Ring'
            diagram.visual(withStep)