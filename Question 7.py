import matplotlib.pyplot as pyplot
import numpy as np
import scipy.stats as sp
import random


def shit(expected, actual):
    waitBin = []
    expBin = []
    valsToSum = []
    start = 0
    end = 0
    binCount = 0
    while binCount < 5:
        while len(expBin) < 5:
            end = end + 1
            # Get everything you can from the bin
            for val in actual:
                if start < val < end:
                    waitBin.append(val)
                elif val > end:
                    break
            for val in expected:
                if start < val < end:
                    expBin.append(val)
                elif val > end:
                    break
        print(str(start) + "-" + str(end) + "\t" + str(len(waitBin)) + "\t" + str(len(expBin)) + "\t" + str(
            (len(waitBin) - len(expBin)) ** 2 / len(expBin)))
        valsToSum.append((len(waitBin) - len(expBin)) ** 2 / len(expBin))
        start = end
        end = end + 1
        waitBin.clear()
        expBin.clear()
        binCount += 1
    return sum(valsToSum)


N = 1000
ia_times = []
service_times1 = []
for i in range(N):
    ia_times.append(random.expovariate(lambd=1))
    service_times1.append(random.expovariate(lambd=1 / 0.6))
delay_times1 = [0]
departure_times1 = [service_times1[0]]
arrival_times = [0]
total_times1 = [departure_times1[0]]
queue_size = [0]

for i in range(1, N):
    arrival_times.append(arrival_times[i - 1] + ia_times[i])
for i in range(1, N):
    queue_size.append(0)
    if arrival_times[i] < departure_times1[i - 1]:
        delay_times1.append(departure_times1[i - 1] - arrival_times[i])
    else:
        delay_times1.append(0)
    for j in range(len(departure_times1)):
        if arrival_times[i] < departure_times1[j]:
            queue_size[i] += 1
    departure_times1.append(arrival_times[i] + delay_times1[i] + service_times1[i])
    total_times1.append(departure_times1[i] - arrival_times[i])

# Generating the percentages of each queue size found
act = [0 for _ in range(max(queue_size) + 1)]
for i in queue_size:
    act[i] += 0.001

# Finding the p-value for the distribution given in the assignment
best = 0
p = 0
for i in np.arange(0.4, 0.7, 0.01):
    exp = []
    for j in range(max(queue_size) + 1):
        exp.append((pow(i, j) * (1 - i)))
    test = sp.chisquare(act, f_exp=exp, axis=None)
    if test[1] > best:
        best = test[1]
        p = i
print(p)
exp = np.random.exponential(scale=max(delay_times1), size=len(delay_times1))


pyplot.hist(queue_size, bins=range(max(queue_size)))
pyplot.title("Queue Size")
pyplot.show()

print(shit(exp, delay_times1))
pyplot.hist(delay_times1, 77)
pyplot.title("Wait Times")
pyplot.show()