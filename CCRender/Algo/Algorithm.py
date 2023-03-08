# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:25:36
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 11:02:30

from CCRender.Topo import Topo, Flows, Node

class Algorithm():
    def getFlow(self, node: Node, topo: Topo, flow: Flows):
        yield

    def initialize(self, topo: Topo):
        pass

    def commRecord(self, topo: Topo) -> list((int, int, int)):
        self.flow: Flows = Flows()
        self.initialize(topo)
        generators = [self.getFlow(topo.nodes[i], topo, self.flow) for i in range(topo.nranks)]
        while True:
            for i in range(topo.nranks):
                step: int = next(generators[i])
            if step == None:
                break
        return list(self.flow.flows.keys())




