import random
import simpy
import matplotlib.pyplot as plt

# Parameters
RANDOM_SEED = 42
SIMULATION_TIME = 50  # Total time to simulate
INITIAL_INVENTORY = 50
s = 20  # Reorder point
S = 100  # Order up to level
LEAD_TIME = 5
DEMAND_RATE = 1  # Units per time unit

# Initialize the inventory and set up the environment
random.seed(RANDOM_SEED)
env = simpy.Environment()
inventory = simpy.Container(env, init=INITIAL_INVENTORY, capacity=S)

def demand_process(env, inventory):
    """Process to simulate demand, decrementing inventory."""
    while True:
        demand = random.expovariate(DEMAND_RATE)
        yield env.timeout(1)  # Demand occurs every time unit
        if inventory.level > 0:
            inventory.get(min(demand, inventory.level))

def inventory_control(env, inventory):
    """Inventory control process using (s, S) policy."""
    while True:
        if inventory.level <= s:
            # Calculate order amount and place order
            order_amount = S - inventory.level
            yield env.timeout(LEAD_TIME)  # Wait for lead time
            inventory.put(order_amount)  # Receive order and restock
        yield env.timeout(1)  # Check inventory every time unit

# Start processes
env.process(demand_process(env, inventory))
env.process(inventory_control(env, inventory))

# Run the simulation
env.run(until=SIMULATION_TIME)

# Plot the results
plt.figure(figsize=(10, 6))
times = []
levels = []
for (time, level) in inventory.get_queue:
    times.append(time)
    levels.append(level)
plt.step(times, levels, where='post')
plt.xlabel('Time')
plt.ylabel('Inventory Level')
plt.title('Inventory Level Over Time')
plt.grid(True)
plt.show()
