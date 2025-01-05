import random
import matplotlib.pyplot as plt

minInterarrivalTime = 3
maxInterarrivalTime = 6

minServicetime = 10
maxServicetime = 15

arrivalList = []
servicetimeList = []
completiontimeList = []
waitingtimeList = []
queuelengthList = []

NumberofCustomer = int(input())

for i in range(NumberofCustomer):
    val = random.uniform(minInterarrivalTime, maxInterarrivalTime)
    arrivalList.append(val)
    val = random.uniform(minServicetime, maxServicetime)
    servicetimeList.append(val)

for i in range(1,NumberofCustomer):
    arrivalList[i] += arrivalList[i-1]

lastDispatch = 0.0
for i in range(NumberofCustomer):
    startingtime = max(lastDispatch,arrivalList[i])
    lastDispatch = startingtime + servicetimeList[i]
    completiontimeList.append(lastDispatch)

totalWaitingTime = 0.0
for i in range(NumberofCustomer):
    waitingtimeList.append(completiontimeList[i]-servicetimeList[i]-arrivalList[i])
    totalWaitingTime += waitingtimeList[i]

startingtime = 0
lastDispatch = 0.0
iArrival = 0
currentQueueLength = 0

for i in range(NumberofCustomer):
    startingtime = max(arrivalList[i],lastDispatch)
    lastDispatch = startingtime + servicetimeList[i]
    temlist = []
    while(iArrival < NumberofCustomer and arrivalList[iArrival]<lastDispatch):
        temlist.append(arrivalList[iArrival])
        if(iArrival == i):
            temlist.pop()
        iArrival += 1
    # print(temlist)
    for i in temlist:
        queuelengthList.append([startingtime, i, currentQueueLength])
        currentQueueLength += 1
        startingtime = i
    queuelengthList.append([startingtime, lastDispatch, currentQueueLength])
    currentQueueLength -= 1

print(arrivalList)
print(servicetimeList)
print(completiontimeList)
print(waitingtimeList)
print(totalWaitingTime/NumberofCustomer)
print(queuelengthList)

x_data = []
y_data = []
timeofLengths = {}
for lis in queuelengthList:
    x_data.append(lis[0])
    x_data.append(lis[1])
    y_data.append(lis[2])
    y_data.append(lis[2])
    if lis[2] in timeofLengths:
        timeofLengths[lis[2]] += (lis[1] - lis[0])
    else:
        timeofLengths[lis[2]] = (lis[1] - lis[0])
# Calculate and display the average waiting time (delay in queuindexofArrivalListe)

averageDelay = totalWaitingTime / NumberofCustomer
print(f'Average Delay in Queue is: {averageDelay}')

# Calculate and display the average queue length
sumofQueuetime = 0.0
for i in timeofLengths:
    sumofQueuetime += (i * timeofLengths[i])
averageQueueLength = sumofQueuetime / completiontimeList[-1]
print(f'Average Queue Length is: {averageQueueLength}')

# Plot the queue length graph with customizations
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, color='blue', linestyle='--', marker='o', markersize=6, label="Queue Length")
plt.title("Queue Length Over Time", fontsize=14)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Queue Length", fontsize=12)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Annotate the exact times and queue lengths
for x, y in zip(x_data, y_data):
    plt.text(x, y + 0.1, f"({x:.2f}, {y})", fontsize=8, ha="center", va="bottom")

# Display the plot
plt.tight_layout()
plt.show()
