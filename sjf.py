import csv

process = []

# Read CSV file
with open("Process_scheduling.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        pro_id = row["Process"]
        at = int(row["Arrival Time"])
        bt = int(row["Burst Time"])
        process.append([pro_id, at, bt])

completed = []
time = 0
total_tat = 0
total_wt = 0
total_rt = 0
gantt = []

print("Process | Arrival | Burst | Completion | Turnaround | Waiting | Response")
print("-"*75)

while process:
    # Get processes that have arrived
    ready = [p for p in process if p[1] <= time]

    # If no process is ready → move time
    if not ready:
        time += 1
        continue

    # Pick process with smallest burst time
    ready.sort(key=lambda x: x[2])
    pro_id, at, bt = ready[0]

    process.remove(ready[0])

    start_time = time
    rt = start_time - at

    time += bt
    ct = time
    tat = ct - at
    wt = tat - bt

    total_tat += tat
    total_wt += wt
    total_rt += rt

    gantt.append((pro_id, ct))

    print(f"{pro_id:^7} | {at:^7} | {bt:^5} | {ct:^10} | {tat:^10} | {wt:^7} | {rt:^8}")

# Gantt Chart
print("\nGANTT CHART")
print("|", end="")
for p, _ in gantt:
    print(f" {p} |", end="")

print("\n0", end="")
for _, t in gantt:
    print(f"   {t}", end="")

# Averages
n = len(gantt)
print("\n\nAverage Turnaround Time =", round(total_tat/n, 2))
print("Average Waiting Time =", round(total_wt/n, 2))
print("Average Response Time =", round(total_rt/n, 2))                                                                                                 