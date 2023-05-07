from ics import Calendar, Event
import ics
from datetime import date, time, datetime, timedelta
from collections import deque
import pytz
import tkinter as tk
from tkinter import ttk

chores_cal = Calendar(creator="NAME")

#KESHAV: UPDATE: time-zone variable
timezone = 'US/Pacific'

# UPDATE : start date and end date
start_date, end_date = date(2023, 1, 21), date(2023, 5, 6) 
weeks = (int((end_date - start_date).days) + 7) // 7

# UPDATE: roommates
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

# UPDATE: key : chores, value : frequency (every other _ week)
c_lst = {"Shower" : freq_stack(3), "Toilet" : freq_stack(1), "Bathroom Sink/Counter" : freq_stack(2), "Kitchen Stove" : freq_stack(3), "Kitchen Counters" : freq_stack(3)}

for curr_date in daterange(start_date, end_date):
    # UPDATE: start time : 10 AM PST
    time_start = 18 
    for chore in c_lst.keys():
        # KESHAV: I think we have to pop the first rather than the last, doesnt really matter because its sorted later.
        due = c_lst[chore].pop(0)
        if due:
            begin = datetime.combine(curr_date, time(hour=time_start))
            event = Event(name=f"Clean {chore} ({mates[due-1]})", begin=begin, duration=timedelta(hours=1))
            time_start += 1
            chores_cal.events.add(event)

with open("chore_calendar.ics", "w") as f:
    f.write(chores_cal.serialize())


# KESHAV: UPDATE: show events method that lets you see the calendar prior to uploading it
def show_events():
    with open('chore_calendar.ics', 'r') as f:
        cal = ics.Calendar(f.read())
    events = sorted(cal.events, key=lambda e: e.begin)

    popup = tk.Tk()
    popup.title("Chore Calendar")

    tree = ttk.Treeview(popup)
    tree["columns"] = ("one", "two")
    tree.column("#0", width=250)
    tree.column("one", width=350)
    tree.column("two", width=150)
    tree.heading("#0", text="Chore")
    tree.heading("one", text="Date and Time")
    tree.heading("two", text="Assigned to")

    for event in events:
        start = event.begin.astimezone(pytz.timezone(timezone))
        end = event.end.astimezone(pytz.timezone(timezone))
        start_str = start.strftime('%a, %b %d, %Y at %I:%M %p')
        end_str = end.strftime('%a, %b %d, %Y at %I:%M %p')
        mate = event.name.split()[-1][1:-1]
        tree.insert("", "end", text=event.name, values=(start_str + ' - ' + end_str, mate))
    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    button = ttk.Button(popup, text="Close", command=popup.destroy)
    button.pack(side=tk.BOTTOM)
    popup.geometry("750x500")
    popup.mainloop()

show_events()
