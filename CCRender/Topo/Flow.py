# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 16:28:41
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 09:53:04

from .Buffer import Buffer
import numpy as np

class Flow():
    def __init__(self, step: int, send: int, recv: int):
        assert(type(send) == int and type(recv) == int)
        self.step: int = step
        self.send: int = send
        self.recv: int = recv

    def __iter__(self):
        return iter((self.step, self.send, self.recv))

    def __next__(self):
        return next((self.step, self.send, self.recv))

    def __hash__(self):
        return hash((self.step, self.send, self.recv))

    def __eq__(self, other):
        return self.step == other.step and self.send == other.send and self.recv == other.recv

    def __repr__(self):
        return f'Flow({self.step}, {self.send}, {self.recv})'

class Flows:
    def __init__(self):
        self.flows: map(Flow, (bool, Buffer)) = {}

    def addFlow(self, step: int, send: int, recv: int, buffer: Buffer):
        assert(self.flows.get(Flow(step, send, recv)) == None)
        self.flows[Flow(step, send, recv)] = (False, buffer)

    def checkFlow(self, step: int, send: int, recv: int) -> Buffer:
        assert(self.flows.get(Flow(step, send, recv)) != None)
        (record, buffer) = self.flows[Flow(step, send, recv)]
        assert(record == False)
        self.flows[Flow(step, send, recv)] = (True, buffer)
        return buffer

    def __repr__(self):
        return self.flows.__repr__()