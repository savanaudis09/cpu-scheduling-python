import csv

process = []

with open("Process_scheduling.csv", "r") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        pro_id = row["Process"]
        at = int(row["Arrival Time"])
        bt = int(row["Burst Time"])
        process.append([pro_id, at, bt])

process.sort(key=lambda x: x[1])

time = 0
total_tat = 0
total_wt = 0
total_rt = 0
gantt = []

print("Process | Arrival | Burst | Completion | Turnaround | Waiting | Response")
print("-"*75)

for pro_id, at, bt in process:
    
    if time < at:
        time = at
    
    rt = time - at   # response time
    time += bt
    ct = time        # completion time
    tat = ct - at    # turnaround time
    wt = tat - bt    # waiting time

    total_tat += tat
    total_wt += wt
    total_rt += rt

    gantt.append((pro_id, ct))

    print(f"{pro_id:^7} | {at:^7} | {bt:^5} | {ct:^10} | {tat:^10} | {wt:^7} | {rt:^8}")

print("\nGANTT CHART")
print("|", end="")
for p, _ in gantt:
    print(f" {p} |", end="")

print("\n0", end="")
for _, t in gantt:
    print(f"   {t}", end="")

n = len(process)
print("\n\nAverage Turnaround Time =", round(total_tat/n, 2))
print("Average Waiting Time =", round(total_wt/n, 2))
print("Average Response Time =", round(total_rt/n, 2))