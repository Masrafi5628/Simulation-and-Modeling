import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 2
SIMULATION_TIME = 50  
INITIAL_INVENTORY = 50
s = 20  
S = 100  
LEAD_TIME = 5
np.random.seed(RANDOM_SEED)


inventory_level = INITIAL_INVENTORY
history = []

num_demands = int(input("Enter the number of demands: "))

demand_times = np.random.randint(0, SIMULATION_TIME, size=num_demands)
demand_sizes = np.random.randint(30, 80, size=num_demands)

demands = sorted(zip(demand_times, demand_sizes))
cp_demands = demands

print(cp_demands)
current_order={"arrival_times":[],"amounts":[]}

for time in range(SIMULATION_TIME):
    if(len(current_order['arrival_times']) and time==current_order['arrival_times'][0]):
        inventory_level+=current_order['amounts'][0]
        current_order['arrival_times'].pop(0)
        current_order['amounts'].pop(0)

    if len(cp_demands) and cp_demands[0][0] == time:
        inventory_level -= cp_demands[0][1]
        cp_demands.pop(0)
        # print(cp_demands)

    history.append((time, inventory_level))
    

    if time % 30 == 0:
        if inventory_level <= s:
            order_amount = S - inventory_level
            current_order['arrival_times'].append(time+LEAD_TIME)
            current_order['amounts'].append(order_amount)

            # for lead_time in range(LEAD_TIME):
            #     if time + lead_time < SIMULATION_TIME:
            #         history.append((time + lead_time, inventory_level))
                    
            # inventory_level += order_amount

print(history)

plt.figure(figsize=(10, 6))
times, levels = zip(*history)
plt.step(times, levels)
plt.xlabel('Time')
plt.ylabel('Inventory Level')
plt.title('Inventory Level Over Time with (s, S) Policy')
plt.grid(True)
plt.show()