import numpy as np
import random

# Objective function to minimize
def objective_function(x):
    # Define objective function that takes the size of PV and BESS as input and returns the cost
    # of the system that we want to minimize
    bess_size = random.randint(1, 50)
    pv_size = random.randint(1, 50)
    # Assume a linear cost function for simplicity
    cost = 1000 * pv_size + 500 * bess_size
    return cost

# Define PSO algorithm
def pso(objective_function, bounds, max_iter=100, swarm_size=100, c1=2, c2=2, w=0.5):
    dim = len(bounds)
    # Initialize the swarm with random positions and velocities within the given bounds
    swarm = np.zeros((swarm_size, dim))
    swarm_best_position = np.zeros((swarm_size, dim))
    swarm_best_fitness = np.ones(swarm_size) * np.inf
    global_best_position = np.zeros(dim)
    global_best_fitness = np.inf
    velocity = np.zeros((swarm_size, dim))
    for i in range(swarm_size):
        for j in range(dim):
            swarm[i,j] = random.uniform(bounds[j][0], bounds[j][1])
            swarm_best_position[i,j] = swarm[i,j]
        fitness = objective_function(swarm[i])
        if fitness < swarm_best_fitness[i]:
            swarm_best_fitness[i] = fitness
            swarm_best_position[i] = swarm[i]
        if fitness < global_best_fitness:
            global_best_fitness = fitness
            global_best_position = swarm[i]
    # Update the swarm and velocities based on PSO equations
    for i in range(max_iter):
        for j in range(swarm_size):
            r1 = np.random.uniform(size=dim)
            r2 = np.random.uniform(size=dim)
            velocity[j] = w * velocity[j] + c1 * r1 * (swarm_best_position[j] - swarm[j]) + c2 * r2 * (global_best_position - swarm[j])
            swarm[j] = swarm[j] + velocity[j]
            for k in range(dim):
                if swarm[j,k] < bounds[k][0]:
                    swarm[j,k] = bounds[k][0]
                    velocity[j,k] = -velocity[j,k]
                if swarm[j,k] > bounds[k][1]:
                    swarm[j,k] = bounds[k][1]
                    velocity[j,k] = -velocity[j,k]
            fitness = objective_function(swarm[j])
            if fitness < swarm_best_fitness[j]:
                swarm_best_fitness[j] = fitness
                swarm_best_position[j] = swarm[j]
            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = swarm[j]
    return global_best_position, global_best_fitness

# Define the bounds for PV and BESS sizes (e.g., between 0 and 10 kW)
bounds = [(0, 10), (0, 10)]

# Call the PSO algorithm with the objective function and bounds
result = pso(objective_function, bounds)


# Print the optimized PV and BESS sizes and the minimum cost
print('Optimized PV size:', round(result[0][0]), 'kW')
print('Optimized BESS size:', round(result[0][1]), 'kWh')
print('Minimum cost:', result[1], 'USD')

