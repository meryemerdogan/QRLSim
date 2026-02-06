from qrlsim.core.QueueModel import Discipline, Deterministic, Markovian, Distribution
import logging
import numpy as np
from collections import deque

class QRLSimulator:
    def __init__(self, arrival_dist: Distribution, service_dist: Distribution, queueDiscipline:Discipline = Discipline.FIFO,  simulation_time =100, num_of_servers =1, seed =42, gui = False):
        logging.basicConfig(level=logging.INFO, format= '%(levelname)s: %(message)s')
        self.arrival_dist = arrival_dist
        self.service_dist = service_dist
        self.simulation_time = simulation_time
        self.queueDiscipline = queueDiscipline
        arrival_rate = arrival_dist.rate()
        if arrival_rate <= 0.0:
            raise ValueError("Incorrect arrival rate / arrival rate absent!")
        expected_arrivals = int(arrival_rate * simulation_time)
        size = max(expected_arrivals * 2, 1000)
        self.arrival_times = deque(np.cumsum(arrival_dist.next_times(size)))
        
        seed_sequence = np.random.SeedSequence(seed)
        seeds = seed_sequence.spawn(num_of_servers)
        self.all_service_times = [[] for _ in range(num_of_servers)]

        for i in range (num_of_servers):
            service_dist.set_seed(seeds[i])
            self.all_service_times[i] = service_dist.next_times(size)

        self.time = 0.0
        self.num_of_servers = num_of_servers
        self.service_durations = np.array(self.all_service_times).T
        self.service_finish_times = np.full(num_of_servers, np.inf)
        self.service_finish_times_index = num_of_servers * [0]
        self.num_of_packets_in_queue = 0
        self.packets_in_queue = deque()
        self.arrival_index = 0
        self.gui = gui

    def _simulate_terminal(self):
        while self.time < self.simulation_time:
            self.step_one_event()

    def _simulaye_gui(self):
        pass # TODO

    def _simulate(self):
        if self.gui:
            self._simulaye_gui()
        else:
            self._simulate_terminal()

    def _serve(self ):
        if len(self.packets_in_queue) > 0 and np.any(self.service_finish_times == np.inf):
            if self.queueDiscipline == Discipline.FIFO:
                self._serveFIFO()
            elif self.queueDiscipline == Discipline.LIFO:
                self._serveLIFO()
            elif self.queueDiscipline == Discipline.SIRO:
                self._serveSIRO()
            else:
                logging.error("Unknown queue discipline!")

    def _finish_service(self):
        server = np.argmin(self.service_finish_times)
        self.time = self.service_finish_times[server]
        self.service_finish_times[server] = np.inf

    def _serveFIFO(self):
        logging.info(f"Simulation is at time {self.time}")
        if len(self.packets_in_queue) == 0:
            return -1
        packet = self.packets_in_queue.popleft()
        idle_servers = np.where(self.service_finish_times == np.inf)[0]
        if len(idle_servers) == 0:
            return -1

        server = idle_servers[0]
        logging.info(f"Server #{server} is processing packet #{packet['packet_id']} arrived at {packet['arrival_time']}")
        # update service finish times
        k = self.service_finish_times_index[server]
        self.service_finish_times_index[server] += 1
        self.service_finish_times[server] = self.time + self.service_durations[k, server]
        self.num_of_packets_in_queue -= 1

    def _packet_arrival(self):
        if self.arrival_index < len(self.arrival_times):
            arrival_time = self.arrival_times[self.arrival_index]
            self.time = arrival_time
            logging.info(f"Simulation is at time {self.time}")
            new_packet_info = {"packet_id" : self.arrival_index, "arrival_time" : arrival_time}
            self.arrival_index += 1
            self.packets_in_queue.append(new_packet_info)
            logging.info(f"New packet arrives! Packet id #{new_packet_info['packet_id']}.")
            self.num_of_packets_in_queue += 1
        else:
            raise IndexError("Number of pre-generated packets are inefficent")
        
    def _serveLIFO(self):
        logging.info(f"Simulation is at time {self.time}")
        if len(self.packets_in_queue) == 0:
            return -1
        packet = self.packets_in_queue.pop()
        idle_servers = np.where(self.service_finish_times == np.inf)[0]
        if len(idle_servers) == 0:
            return -1

        server = idle_servers[0]
        logging.info(f"Server #{server} is processing packet #{packet['packet_id']} arrived at {packet['arrival_time']}")
        # update service finish times
        k = self.service_finish_times_index[server]
        self.service_finish_times_index[server] += 1
        self.service_finish_times[server] = self.time + self.service_durations[k, server]
        self.num_of_packets_in_queue -= 1

    def _serveSIRO(self):
        logging.info(f"Simulation is at time {self.time}")
        if len(self.packets_in_queue) == 0:
            return -1
        random_index = np.random.randint(0, len(self.packets_in_queue))
        packet = self.packets_in_queue[random_index]
        self.packets_in_queue[random_index] = self.packets_in_queue[-1]
        self.packets_in_queue.pop()
        idle_servers = np.where(self.service_finish_times == np.inf)[0]
        if len(idle_servers) == 0:
            return -1

        server = idle_servers[0]
        logging.info(f"Server #{server} is processing packet #{packet['packet_id']} arrived at {packet['arrival_time']}")
        # update service finish times
        k = self.service_finish_times_index[server]
        self.service_finish_times_index[server] += 1
        self.service_finish_times[server] = self.time + self.service_durations[k, server]
        self.num_of_packets_in_queue -= 1
    
    def step_one_event(self):
        next_arrival_time = np.inf
        next_service_finish_time = np.inf

        if self.arrival_index < len(self.arrival_times):
            next_arrival_time = self.arrival_times[self.arrival_index]

        if self.service_finish_times is not None:
            next_service_finish_time = np.min(self.service_finish_times)

        if next_arrival_time == np.inf and next_service_finish_time == np.inf:
            self.time = self.simulation_time
            return
        
        if next_arrival_time <= next_service_finish_time:
            self._packet_arrival()
            self._serve()
        else:
            self._finish_service()
            self._serve()
