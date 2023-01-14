from ics import Calendar, Event
from datetime import date, time, datetime, timedelta
from collections import deque

chores_cal = Calendar(creator="adit-bala")
start_date, end_date = date(2023, 1, 21), date(2023, 5, 6) 
weeks = (int((end_date - start_date).days) + 7) // 7

# roommates
mates = ["adit", "Ollie", "Rouxles", "Zoro"]
# cyclic rotation to distribute chores
cycle_index = deque(list(range(1, len(mates) + 1)))

# return weekly range for chore days
def daterange(start_date, end_date):
    for n in range(0, int((end_date - start_date).days) + 7, 7):
        yield start_date + timedelta(n)

# create stack to monitor frequencies of each chore and assign to roommates
def freq_stack(freq):
    mate_cycle = iter(cycle_index * (weeks // len(mates)))
    cycle_index.rotate(-1)
    return [0 if day % freq else next(mate_cycle) for day in range(weeks)]

# key : chores, value : frequency (every other _ week)
c_lst = {"Shower" : freq_stack(3), "Toilet" : freq_stack(1), "Bathroom Sink/Counter" : freq_stack(2), "Kitchen Stove" : freq_stack(3), "Kitchen Counters" : freq_stack(3)}

for curr_date in daterange(start_date, end_date):
    # start time : 10 AM EST
    time_start = 18 
    for chore in c_lst.keys():
        due = c_lst[chore].pop()
        if due:
            begin = datetime.combine(curr_date, time(hour=time_start))
            event = Event(name=f"Clean {chore} ({mates[due-1]})", begin=begin, duration=timedelta(hours=1))
            time_start += 1
            chores_cal.events.add(event)

with open("chore_calendar.ics", "w") as f:
    f.write(chores_cal.serialize())
