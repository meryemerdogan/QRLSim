import gymnasium as gym
from gymnasium import spaces
import numpy as np

from qrlsim.core.QRLSimulator import QRLSimulator
from qrlsim.core.QueueModel import Markovian, Discipline


class MM1Env(gym.Env):
    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(2) # 0 -> keep 1-> drop
        self.observation_space = spaces.Box(low = np.array([0.0, 0.0]), high = np.array([1000.0, np.inf]), dtype=np.float32)

        self.state = np.array([0.0, 0.0], dtype=np.float32)
        self.size = 1 # trying to achieve reproducability

        self.packets_in_queue = [] # get from simulation
        self.curr_time = None # get from simulaiton
        self.prev_num_of_dropped_packets = 0
        self.num_of_dropped_packets = None
        self.curr_num_of_dropped_pakcets = 0

        arrival = Markovian(rate = 0.8)
        service = Markovian(rate = 1.0)

        self.sim = QRLSimulator(
            arrival_dist=arrival,
            service_dist=service,
            queueDiscipline=Discipline.FIFO,
            simulation_time=100
        )


    def compute_reward(self):
        eps = 1e-6
        key = 'arrival_time'
        enqueue_times = [element.get(key) for element in self.packets_in_queue if key in element]
        if len(enqueue_times) == 0:
            return 0.0
        sojourn_times = [max(self.curr_time-queue_time, eps) for queue_time in enqueue_times]
        avg_delay = np.mean(sojourn_times)
        reward_val = -avg_delay
        reward_val -= 2.0 *self.curr_num_of_dropped_pakcets
        return reward_val

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.sim.time = 0.0
        self.sim.packets_in_queue.clear()
        self.sim.arrival_index = 0
        self.sim.service_finish_times[:] = np.inf

        self.curr_time = 0.0
        self.packets_in_queue = []
        self.curr_num_of_dropped_pakcets = 0

        self.state = np.array([0.0, 0.0], dtype=np.float32)
        
        return self.state, {}
        
    def step(self, action):
        if action ==1 and len(self.sim.packets_in_queue) > 0:
            self.sim.packets_in_queue.pop()
            self.curr_num_of_dropped_pakcets += 1

        self.update_values()
        reward = self.compute_reward()

        terminated = False
        truncated = self.curr_time >= self.sim.simulation_time

        return self.state, reward, terminated, truncated, {}
    
    def update_values(self):
        self.sim.step_one_event()

        self.curr_time = self.sim.time
        self.packets_in_queue = list(self.sim.packets_in_queue)

        self.state = np.array( [len(self.packets_in_queue), self.curr_time], dtype=np.float32)
        
    