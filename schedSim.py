import sys

alg = 'FIFO'
quantum = 1
processes = []

def print_job(jobs):
    for job in jobs:
        print(job[0]+' -- '+'Turnaround {:3.2f} '.format(job[1])+'Wait {:3.2f}'.format(job[2]))

def print_average(jobs):
    avg_turnaround_time = sum([job[1] for job in jobs])/len(jobs)
    avg_wait_time = sum([job[2] for job in jobs])/len(jobs)
    print('Average -- '+'Turnaround {:3.2f} '.format(avg_turnaround_time)+'Wait {:3.2f}'.format(avg_wait_time))

def FIFO():
    global processes
    processes = sorted(processes, key=lambda x:(x[2], x[0]))
    time = min([p[2] for p in processes])
    analyzed_jobs = []
    for i in range(len(processes)):
        time += processes[i][1]
        turnaround_time = time-processes[i][2]
        waiting_time = turnaround_time-processes[i][1]
        analyzed_job = (processes[i][0], turnaround_time, waiting_time)
        analyzed_jobs.append(analyzed_job)
    print_job(analyzed_jobs)
    print_average(analyzed_jobs)

def SRTN():
    global processes
    completion_time = [0] * len(processes)
    remaining_time = [p[1] for p in processes]
    arrival_time = [p[2] for p in processes]
    time = min(arrival_time)
    completed = 0
    while completed < len(processes):
        shortest = float('inf')
        shortest_index = -1
        for i in range(len(processes)):
            if arrival_time[i] <= time and remaining_time[i] < shortest and remaining_time[i] > 0:
                shortest = remaining_time[i]
                shortest_index = i
        remaining_time[shortest_index] -= 1
        time += 1
        if remaining_time[shortest_index] == 0:
            completion_time[shortest_index] = time
            completed += 1
    analyzed_jobs = []
    for j in range(len(processes)):
        turnaround_time = completion_time[j]-arrival_time[j]
        waiting_time = turnaround_time - processes[j][1]
        analyzed_job = (processes[j][0], turnaround_time, waiting_time)
        analyzed_jobs.append(analyzed_job)
    print_job(analyzed_jobs)
    print_average(analyzed_jobs)
    
def RR():
    global processes, quantum
    time = processes[0][2]
    processes = [(p[0], p[1], p[2], p[1]) for p in processes]
    completed_processes = []
    while processes:
        process = processes.pop(0)
        if process[1] > quantum:
            time += quantum
            processes.append((process[0], process[1]-quantum, process[2], process[3]))
        else:
            time += process[1]
            turnaround_time = time-process[2]
            waiting_time = turnaround_time-process[3]
            completed_processes.append((process[0], turnaround_time, waiting_time))
    print_job(completed_processes)
    print_average(completed_processes)

def main():
    global processes
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        id = 0
        for line in lines:
            line = line.split()
            process = ('Job {:3d}'.format(id), int(line[0]), int(line[1])) # Store process id, burst time, arrival time
            processes.append(process)
            id += 1
        processes = sorted(processes, key=lambda x:(x[2], x[0]))
        
    if 'SRTN' in sys.argv:
        SRTN()
    elif 'RR' in sys.argv:
        try:
            global quantum
            quantum = int(sys.argv[-1])
            if quantum < 1:
                quantum = 1
                raise ValueError
        except ValueError:
            print("No quantum given or invalid quantum given\nThe program will continue with quantum=1\n")
        RR()
    else:
        FIFO()

if __name__ == '__main__':
    main()
    