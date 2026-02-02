from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
from numpy import random
class Discipline(Enum):
    FIFO = "FIFO" # first in first out
    LIFO = "LIFO" # last in first out
    SIRO = "SIRO" # random order

class Distribution(ABC):
    @abstractmethod
    def next_times(self, size):
        return []
    @abstractmethod
    def rate(self): # events per unit time (second)
        return -1
    @abstractmethod
    def set_seed(self, seed =42):
        self.rng = np.random.default_rng(seed)
class Markovian(Distribution):
    def __init__(self, rate):
        self._rate = rate
        self.rng = None
    def set_seed(self, seed =42):
        self.rng = np.random.default_rng(seed)
    def next_times(self, size):
        if self.rng == None:
            self.rng = np.random.default_rng(42)
        return self.rng.exponential(scale=(1 / self._rate), size = size)
    def rate(self):
        return self._rate
class Deterministic(Distribution):
    def __init__(self, rate):
        self._rate = rate   
    def next_times(self , size):
        return [(1/self._rate) for _ in range(size)]
    def rate(self):
        return self._rate
    def set_seed(self, seed =42):
        pass
