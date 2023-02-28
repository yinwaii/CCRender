# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 11:20:02
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 11:31:21

from .SimpleDiagram import SimpleDiagram
from CCRender.Topo import UniformLayeredTopo
from CCRender.Algo import Algorithm


class SimpleLayeredDiagram(SimpleDiagram):
    def __init__(self, topo: UniformLayeredTopo, algo: Algorithm):
        super().__init__(topo, algo)
        self.topo: UniformLayeredTopo = topo

    def genNode(self) -> str:
        calcIntraLabel = lambda interRank: '\n'.join(
            f'{self.genNodeInfo(self.topo.getRank(interRank, intraRank))}'
            for intraRank in range(self.topo.nintraRanks))
        calcCluster = lambda interRank: f'subgraph cluster_{interRank} {{\nlabel="server {interRank}";\n{calcIntraLabel(interRank)}\n}}'
        resList: list(str) = [
            calcCluster(interRank)
            for interRank in range(self.topo.ninterRanks)
        ]
        return '\n'.join(resList)