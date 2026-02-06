
from qrlsim.core.QRLSimulator import Markovian, QRLSimulator, Discipline
if __name__ == "__main__":
    # Simple M/M/1 test

    arrival_rate = 0.8
    service_rate = 1.0 
    arrival_dist = Markovian(arrival_rate)
    service_dist = Markovian(service_rate)

    sim = QRLSimulator(
        arrival_dist=arrival_dist,
        service_dist=service_dist,
        queueDiscipline=Discipline.FIFO,
    )

    sim._simulate()

    print("Simulation finished.")
    print(f"Final time: {sim.time}")
    print(f"Packets left in queue: {sim.num_of_packets_in_queue}")
    print(f"Server finish times: {sim.service_finish_times}")
