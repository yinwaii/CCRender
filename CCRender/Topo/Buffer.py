# -*- coding: utf-8 -*-
# @Author: yinwai
# @Date:   2023-03-07 11:34:45
# @Last Modified by:   yinwai
# @Last Modified time: 2023-03-08 11:50:34

import numpy as np

class Buffer:
    def __init__(self, buffer: np.ndarray = None):
        self.buffer = buffer

    def setBuffer(self, nslices: int, nranks: int):
        self.buffer: np.ndarray = np.zeros((nslices, nranks), dtype=bool)

    def selectSlices(self, index: int):
        res: np.ndarray = np.zeros(self.buffer.shape, dtype=bool)
        res[index, :] = self.buffer[index, :]
        return Buffer(res)

    def selectSlices(self, begin: int, end: int):
        res: np.ndarray = np.zeros(self.buffer.shape, dtype=bool)
        if begin <= end:
            res[begin:end, :] = self.buffer[begin:end, :]
        else:
            res[end:, :] = self.buffer[end:, :]
            res[:begin, :] = self.buffer[:begin, :]
        return Buffer(res)

    def __repr__(self):
        return self.buffer.shape.__repr__()
