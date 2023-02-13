import requests
import random
import numpy as np

def PSO(npop, max_iter, c1, c2, w, wdamp):
    # Generate random PV and battery module size between 1 and 50
    particles = np.random.randint(1, 51, size=(npop, 2))

    # Initialize velocities
    velocities = np.zeros((npop, 2))

    # Initialize particle best positions and best costs
    pbest_positions = particles
    pbest_costs = np.zeros(npop)

    # Initialize global best position and global best cost
    gbest_position = np.zeros(2)
    gbest_cost = np.inf

    # Perform iterations
    for i in range(max_iter):
        # Calculate total PV and BESS power outputs and energy needed from grid
        total_pv_output, total_bess_output, energy_needed = energy_management(particles)
        costs = calc_total_cost(total_pv_output, total_bess_output, energy_needed)

        # Update particle best positions and costs
        for j in range(npop):
            if costs[j] < pbest_costs[j]:
                pbest_costs[j] = costs[j]
                pbest_positions[j] = particles[j]

        # Update global best position and cost
        best_index = np.argmin(pbest_costs)
        if pbest_costs[best_index] < gbest_cost:
            gbest_cost = pbest_costs[best_index]
            gbest_position = pbest_positions[best_index]

        # Update velocities and particle positions
        for j in range(npop):
            r1 = random.random()
            r2 = random.random()
            velocities[j] = w * velocities[j] + c1 * r1 * (pbest_positions[j] - particles[j]) + c2 * r2 * (gbest_position - particles[j])
            particles[j] = particles[j] + velocities[j]

        # Update w using wdamp
        w = w * wdamp

    return gbest_position, gbest_cost

def energy_management(particles):
    # Calculate total PV and BESS power outputs and energy needed from grid
    total_pv_output = np.sum(particles[:, 0])
    total_bess_output = np.sum(particles[:, 1])
    energy_needed = calc_energy_needed(total_pv_output, total_bess_output)

    return total_pv_output, total_bess_output, energy_needed

def calc_total_cost(total_pv_output, total_bess_output, energy_needed):
    # Assuming that the cost is proportional to the energy needed from the grid
    costs = energy_needed * 0.1
    return costs


def calc_energy_needed(total_pv_output, total_bess_output):
    # Make a call to flexmeasures API to get the energy needed from the grid
    API_KEY = "token"
    API_URL = "http://localhost:5000/assets/3/"
