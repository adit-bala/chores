from ics import Calendar, Event, alarm, Attendee
from datetime import date, time, datetime, timedelta
from collections import deque
from dotenv import dotenv_values


chores_cal = Calendar(creator="adit-bala")
# UPDATE : start date and end date
start_date, end_date = date(2023, 8, 21), date(2023, 11, 6) 
weeks = (int((end_date - start_date).days) + 7) // 7

# UPDATE: roommates
mates = ["Adit", "Lambda", "Rouxles", "Zoro"]
emails = list(dotenv_values(".env").values())

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

# UPDATE: key : chores, value : frequency (every other _ week)
c_lst = {"Shower" : freq_stack(3), "Toilet" : freq_stack(1), "Bathroom Sink/Counter" : freq_stack(1), "Kitchen Stove" : freq_stack(3), "Kitchen Counters" : freq_stack(3)}

for curr_date in daterange(start_date, end_date):
    # UPDATE: start time : 10 AM PST
    time_start = 18
    for chore in c_lst.keys():
        due = c_lst[chore].pop()
        if due:
            begin = datetime.combine(curr_date, time(hour=time_start))
            emailAlarm = alarm.EmailAlarm(trigger=begin-timedelta(hours=2), subject=f"PLEASE COMPLETE {chore}", recipients=[Attendee(emails[due-1])])
            event = Event(name=f"Clean {chore} ({mates[due-1]})", begin=begin, duration=timedelta(hours=1), alarms=[emailAlarm])
            time_start += 1
            chores_cal.events.add(event)

with open("chore_calendar.ics", "w") as f:
    f.write(chores_cal.serialize())
