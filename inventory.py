import random
import matplotlib.pyplot as plt

# Parameters
RANDOM_SEED = 2
SIMULATION_TIME = 500  # Total time to simulate
INITIAL_INVENTORY = 50
s = 20  # Reorder point
S = 100  # Order up to level
LEAD_TIME = 5
DEMAND_RATE = 1  # Average demand per time unit
MONTH_DURATION = 30  # Duration of a month in time units

# Initialize the inventory and set the random seed
random.seed(RANDOM_SEED)
inventory_level = INITIAL_INVENTORY
history = []

# Simulation loop
for time in range(SIMULATION_TIME):
    # Generate random demand for the current time unit
    demand = random.expovariate(DEMAND_RATE)
    
    # Update inventory level based on demand
    if inventory_level > 0:
        inventory_level -= min(demand, inventory_level)
    
    # Check if it's the end of the month
    if time % MONTH_DURATION == 0:
        # Check if we need to reorder
        if inventory_level <= s:
            # Calculate order amount and simulate lead time
            order_amount = S - inventory_level
            # Simulate the arrival of the order after lead time
            for lead_time in range(LEAD_TIME):
                if time + lead_time < SIMULATION_TIME:
                    # During lead time, inventory remains the same
                    history.append((time + lead_time, inventory_level))
            # After lead time, update inventory level
            inventory_level += order_amount
    
    # Record the inventory level at the current time
    history.append((time, inventory_level))

# Plot the results
plt.figure(figsize=(10, 6))
times, levels = zip(*history)
plt.step(times, levels, where='post')
plt.xlabel('Time')
plt.ylabel('Inventory Level')
plt.title('Inventory Level Over Time')
plt.grid(True)
plt.show()