# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-02-28 10:24:52
# @Last Modified by:   yinwai
# @Last Modified time: 2023-02-28 16:28:50

class Topo():
    def __init__(self, nranks: int):
        self.nranks: int = nranks
        self.name: str = f'{self.nranks}'

