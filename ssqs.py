import random
import matplotlib.pyplot as plt

minInterarrivalRate = 3
maxInterarrivalRate = 6

minServicetime = 10
maxServicetime = 15

arrivalList = []
servicetimeList = []
completiontimeList = []
waitingtimeList = []
queuelengthList = []

NumberofCustomer = int(input("Enter the Number of Customer : "))

for i in range(NumberofCustomer):
    val = random.uniform(minInterarrivalRate, maxInterarrivalRate)
    arrivalList.append(val)
    val = random.uniform(minServicetime, maxServicetime)
    servicetimeList.append(val)

for i in range(1,NumberofCustomer):
    arrivalList[i] += arrivalList[i-1]

lastdispatcher = 0.0
for i in range(NumberofCustomer):
    startingtime = max(lastdispatcher,arrivalList[i])
    lastdispatcher = startingtime + servicetimeList[i]
    completiontimeList.append(lastdispatcher)

totalWaitingTime = 0.0
for i in range(NumberofCustomer):
    waitingtimeList.append(completiontimeList[i]-arrivalList[i]-servicetimeList[i])
    totalWaitingTime += waitingtimeList[i]

startingtime = 0
lastdispatcher = 0.0
indexofArrivalList = 0
currentQueueLength = 0

for i in range(NumberofCustomer):
    startingtime = max(arrivalList[i],lastdispatcher)
    lastdispatcher = startingtime + servicetimeList[i]
    temlist = []
    while(indexofArrivalList < NumberofCustomer and arrivalList[indexofArrivalList]<lastdispatcher):
        temlist.append(arrivalList[indexofArrivalList])
        if(indexofArrivalList == i):
            temlist.pop()
        indexofArrivalList += 1
    # print(temlist)
    for ele in temlist:
        queuelengthList.append([startingtime, ele, currentQueueLength])
        currentQueueLength += 1
        startingtime = ele
    queuelengthList.append([startingtime, lastdispatcher, currentQueueLength])
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
# Calculate and display the average waiting time (delay in queue)

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
