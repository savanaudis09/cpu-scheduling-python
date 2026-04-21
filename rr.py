import csv
from collections import deque

processes = []

# Read CSV
with open("processes.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        processes.append({
            "pid": row["Process"],
            "arrival": int(row["Arrival"]),
            "burst": int(row["Burst"]),
            "remaining": int(row["Burst"]),
            "start": None,
            "completion": 0
        })

# Sort by arrival time
processes.sort(key=lambda x: x["arrival"])

time_quantum = int(input("Enter Time Quantum: "))

ready_queue = deque()
time = 0
index = 0
gantt = []
context_switches = 0

while ready_queue or index < len(processes):

    # Add arrived processes
    while index < len(processes) and processes[index]["arrival"] <= time:
        ready_queue.append(processes[index])
        index += 1

    if not ready_queue:
        time += 1
        continue

    current = ready_queue.popleft()

    # First time execution → response time
    if current["start"] is None:
        current["start"] = time

    exec_time = min(time_quantum, current["remaining"])

    gantt.append((current["pid"], time, time + exec_time))
    context_switches += 1

    time += exec_time
    current["remaining"] -= exec_time

    # Add new arrivals during execution
    while index < len(processes) and processes[index]["arrival"] <= time:
        ready_queue.append(processes[index])
        index += 1

    # If not finished → push back
    if current["remaining"] > 0:
        ready_queue.append(current)
    else:
        current["completion"] = time

# Calculate metrics
total_tat = total_wt = total_rt = 0

print("\nProcess Details Table:")
print("Process | Arrival | Burst | Completion | Turnaround | Waiting | Response")
print("-"*75)

for p in processes:
    tat = p["completion"] - p["arrival"]
    wt = tat - p["burst"]
    rt = p["start"] - p["arrival"]

    total_tat += tat
    total_wt += wt
    total_rt += rt

    print(f"{p['pid']:>7} | {p['arrival']:>7} | {p['burst']:>5} | {p['completion']:>10} |"
          f"{tat:>11} | {wt:>7} | {rt:>8}")

# Gantt Chart
print("\nGANTT CHART")
print("|", end="")
for i in gantt:
    print(f" {i[0]} |", end="")

print("\n0", end="")
for j in gantt:
    print(f"   {j[2]}", end="")

# Averages
n = len(processes)
print("\n\nAverage Turnaround Time:", round(total_tat / n, 2))
print("Average Waiting Time:", round(total_wt / n, 2))
print("Average Response Time:", round(total_rt / n, 2))
print("\nTotal Context Switches:", context_switches - 1)