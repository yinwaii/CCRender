# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 16:28:41
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:28:52


class Flow():
    def __init__(self, step: int, send: int, recv: int):
        self.step: int = step
        self.send: int = send
        self.recv: int = recv

    def __iter__(self):
        return iter((self.step, self.send, self.recv))

    def __next__(self):
        return next((self.step, self.send, self.recv))

    def __hash__(self):
        return hash(self.step) ^ hash(self.send) ^ hash(self.recv)

    def __eq__(self, other):
        return self.step == other.step and self.send == other.send and self.recv == other.recv

    def __repr__(self):
        return f'Flow({self.step}, {self.send}, {self.recv})'