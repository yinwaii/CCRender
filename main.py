# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:26:38
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 10:33:20

from CCRender.Topo import *
from CCRender.Algo import *
from CCRender.Diagram import *

if __name__ == '__main__':
    topo = UniformLayeredTopo(4, 4)
    algo = ShiftedButterfly()
    diagram = SimpleLayeredDiagram(topo, algo)
    diagram.visual(withStep=True)