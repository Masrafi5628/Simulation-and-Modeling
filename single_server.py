import random
import simpy
import matplotlib.pyplot as plt

# Parameters
RANDOM_SEED = 42
INTERARRIVAL_TIME = 12  # Average time between arrivals (minutes)
SERVICE_TIME = 8       # Average service time per customer (minutes)
NUM_CUSTOMERS = 10    # Number of customers to complete service

# Metrics to track
wait_times = []        # Waiting times of each customer who completes service
queue_lengths = []     # Queue length at each time step
time_steps = []        # Corresponding time steps for queue lengths

def customer(env, name, barber, arrival_times):
    """Customer arrives, waits in queue if needed, and receives service."""
    arrival_time = env.now
    arrival_times.append(arrival_time)
    
    # Request service from the barber
    with barber.request() as request:
        yield request  # Wait in queue if barber is busy

        # Calculate waiting time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        # Perform service
        service_duration = random.expovariate(1.0 / SERVICE_TIME)
        yield env.timeout(service_duration)  # Service time

def customer_arrival(env, barber, arrival_times):
    """Generate customers at random intervals until NUM_CUSTOMERS are served."""
    for i in range(NUM_CUSTOMERS):
        interarrival = random.expovariate(1.0 / INTERARRIVAL_TIME)
        yield env.timeout(interarrival)
        env.process(customer(env, f"Customer {i + 1}", barber, arrival_times))

def track_queue_length(env, barber):
    """Track the number of customers in the queue over time."""
    while len(wait_times) < NUM_CUSTOMERS:
        queue_length = len(barber.queue)  # Current number waiting in queue
        queue_lengths.append(queue_length)
        time_steps.append(env.now)
        yield env.timeout(1)  # Record queue length every minute

# Set up the simulation environment
random.seed(RANDOM_SEED)
env = simpy.Environment()
barber = simpy.Resource(env, capacity=1)

# Start the arrival process and tracking
arrival_times = []
env.process(customer_arrival(env, barber, arrival_times))
env.process(track_queue_length(env, barber))

# Run the simulation
env.run()

# Calculate metrics
average_delay_in_queue = sum(wait_times) / NUM_CUSTOMERS if wait_times else 0
average_queue_length = sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0

# Display the results
print(f"Expected average delay in queue, d(n): {average_delay_in_queue:.2f} minutes")
print(f"Expected average number in queue, q(n): {average_queue_length:.2f} customers")

# Plot the queue lengths over time
plt.figure(figsize=(10, 6))
plt.plot(time_steps, queue_lengths, label="Queue Length")
plt.xlabel("Time (minutes)")
plt.ylabel("Number of Customers in Queue")
plt.title("Queue Length Over Time in Barber Shop Simulation")
plt.legend()
plt.grid()
plt.show()
