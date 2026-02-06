# QRLSim: Queueing System Simulation Framework (v1.1.0)

QRLSim is a Python based simulation framework for modeling and analyzing queueing systems, designed specifically for **reinforcement learning (RL) research in networking and active queue management (AQM)**.

## Features
- Simulate classic queueing systems such as **M/M/1** with customizable parameters.
- Built-in support for multiple servers and queue disciplines (FIFO, LIFO, SIRO).
- Modular API for defining arrival and service distributions.
- **Gymnasium-compatible RL environments** for training agents on queue control tasks.
- Includes ready-to-run **Deep RL training scripts** (DQN, PPO) using Stable-Baselines3.
- Extendable framework for advanced queueing models and networking experiments.

## File Descriptions

### `qrlsim/core/QueueModel.py`
Defines the core queueing system components, including:
- **Queue Disciplines**: FIFO, LIFO, and SIRO.
- **Distribution Classes**:
  - `Markovian`: Exponential inter-arrival/service times.
  - `Deterministic`: Fixed inter-arrival/service times.

### `qrlsim/core/QRLSimulator.py`
Implements the main simulation logic:
- Packet arrivals and service completions
- Multi-server support
- Queue discipline scheduling
- Event-based stepping via `step_one_event()`

### `qrlsim/aqm_envs/MM1_env.py`
Provides a Gymnasium-compatible M/M/1 environment for RL:
- Actions: keep or drop packets
- Reward: delay + drop penalty

### `train/`
Includes reinforcement learning training scripts:
- `train_dqn.py`
- `train_ppo.py`

### `QRLSimulator.py`
This file implements the main simulation logic, including:
- **QRLSimulator**: Handles the simulation of queueing systems.
  - Simulates packet arrivals and service completions.
  - Supports multiple servers and queue disciplines.
  - Logs simulation events for debugging and analysis.

## Requirements
- Python 3.7+
- NumPy
