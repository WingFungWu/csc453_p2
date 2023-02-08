import sys

jobs = []
alg = 'FIFO'
quantum = 1

class Job():
    id = 0
    burst_time = 0
    arrival_time = 0
    remaining_time = 0
    wait_time = 0
    turnaround_time = 0

    def __init__(self, id, burst_time, arrival_time) -> None:
        self.id = id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time

def FIFO():
    global jobs
    time = 0
    for job in jobs:
        job.wait_time = time
        time += job.burst_time
        job.turnaround_time = job.burst_time
        print('Job '+'{:3d} -- '.format(job.id)
            +'Turnaround {:3.2f} '.format(job.turnaround_time)
            +'Wait {:3.2f}'.format(job.wait_time))
    avg_turnaround_time = sum([job.turnaround_time for job in jobs])/len(jobs)
    avg_wait_time = sum([job.wait_time for job in jobs])/len(jobs)
    print('Average -- '+'Turnaround {:3.2f} '.format(avg_turnaround_time)
        +'Wait {:3.2f}'.format(avg_wait_time))

def SRTN():
    pass

def RR():
    pass

def main():
    global jobs
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()
        lines = [(line.split()[1], line.split()[0]) for line in lines]
        for line in lines:
            jobs.append(Job(0, int(line[1]), int(line[0])))
        jobs = sorted(jobs, key=lambda x:x.arrival_time)
        job_id = 0
        for job in jobs:
            job.id = job_id
            job_id += 1
    
    if 'SRTN' in sys.argv:
        SRTN()
    elif 'RR' in sys.argv:
        RR()
    else:
        FIFO()

if __name__ == '__main__':
    main()
    