# QRLSim: Queueing System Simulation Framework (VERSION 1)

QRLSim is a Python-based simulation framework for modeling and analyzing queueing systems. Especially designed for training RL agents for computer networking problems.

## Features
- Simulate M/M/1 queueing systems with customizable parameters.
- Support for multiple servers and queue disciplines.
- Easy-to-use API for defining arrival and service distributions.
- Extendable framework for advanced queueing models.

## File Descriptions

### `QueueModel.py`
This file defines the core components of the simulation, including:
- **Queue Disciplines**: FIFO, LIFO, and SIRO.
- **Distribution Classes**: Abstract base class `Distribution` and its implementations:
  - `Markovian`: Generates inter-arrival or service times based on an exponential distribution.
  - `Deterministic`: Generates fixed inter-arrival or service times.

### `QRLSimulator.py`
This file implements the main simulation logic, including:
- **QRLSimulator**: Handles the simulation of queueing systems.
  - Simulates packet arrivals and service completions.
  - Supports multiple servers and queue disciplines.
  - Logs simulation events for debugging and analysis.

## Requirements
- Python 3.7+
- NumPy