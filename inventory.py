import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 2
SIMULATION_TIME = 500  
INITIAL_INVENTORY = 50
s = 20  
S = 100  

LEAD_TIME = 5
DEMAND_LOW = 30  
DEMAND_HIGH = 80  
MONTH_DURATION = 30  

np.random.seed(RANDOM_SEED)
inventory_level = INITIAL_INVENTORY
history = []

for time in range(SIMULATION_TIME):
    if np.random.rand() < 0.1:  
        demand = np.random.uniform(DEMAND_LOW, DEMAND_HIGH)
        inventory_level -= demand  
    
    history.append((time, inventory_level))
    
    if time % MONTH_DURATION == 0:
        if inventory_level <= s:
            order_amount = S - inventory_level
            for lead_time in range(LEAD_TIME):
                if time + lead_time < SIMULATION_TIME:
                    history.append((time + lead_time, inventory_level))

            inventory_level += order_amount

print(history)

plt.figure(figsize=(10, 6))
times, levels = zip(*history)
plt.step(times, levels, where='post')
plt.xlabel('Time')
plt.ylabel('Inventory Level')
plt.title('Inventory Level Over Time with (s, S) Policy')
plt.grid(True)
plt.show()