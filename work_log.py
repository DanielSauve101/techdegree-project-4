"""Work Log

Created: 2019-05-01
Updated: 2019-05-03
Author: Daniel Sauve
"""

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *


db = SqliteDatabase('work_log.db')

work_log = [
    {'task_title': 'Job1',
     'employee_name': 'Daniel',
     'time_spent': 12,
     'optional_notes': 'This is a memo',
     'timestamp': datetime.datetime(2019, 5, 1)},
    {'task_title': 'Job2',
     'employee_name': 'Daniel Sauve',
     'time_spent': 45,
     'optional_notes': '',
     'timestamp': datetime.datetime(2019, 5, 1)},
    {'task_title': 'Job3',
     'employee_name': 'Benoit',
     'time_spent': 45,
     'optional_notes': 'I like green eggs and ham',
     'timestamp': datetime.datetime(2019, 4, 20)},
    {'task_title': 'Job4',
     'employee_name': 'Samatha K',
     'time_spent': 63,
     'optional_notes': '12344',
     'timestamp': datetime.datetime(2019, 4, 1)},
    {'task_title': 'Job5',
     'employee_name': 'Flash',
     'time_spent': 76,
     'optional_notes': 'I like python',
     'timestamp': datetime.datetime(2019, 5, 2)},
    {'task_title': 'Job6',
     'employee_name': 'Mathieu Carman',
     'time_spent': 3,
     'optional_notes': 'Very short task',
     'timestamp': datetime.datetime(2019, 5, 3)},
    {'task_title': 'Job7',
     'employee_name': 'Daniel T',
     'time_spent': 65,
     'optional_notes': 'job1',
     'timestamp': datetime.datetime(2019, 5, 3)}
]


class Entry(Model):
    task_title = CharField(max_length=100)
    employee_name = CharField(max_length=100, unique=True)
    time_spent = IntegerField()
    optional_notes = TextField(null=False)
    timestamp = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu_loop():
    """Show the main menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in main_menu:
            clear()
            main_menu[choice]()


def search_menu_loop():
    """Search entries"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to return to previous menu.")
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in search_menu:
            clear()
            search_menu[choice]()


def add_entry():
    """Add an entry"""
    title = input("Please enter the title of the task: ")
    name = input("Please enter your name: ")
    time = input("Please enter the time spent on task in minutes: ")
    notes = input("Please enter any notes (Optional): ")

    # data = sys.stdin.read().strip()

    if title and name and time:
        if input('Save entry [Yn] ').lower() != 'n':
            Entry.create(task_title=title,
                         employee_name=name,
                         time_spent=time,
                         optional_notes=notes
                         )
            print("Saved successfully!")


def view_entries(search_query=None):
    """View entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = search_query

    for entry in entries:
        timestamp = entry.timestamp.strftime('%B %d %Y')
        clear()
        print("Date entered: {}".format(timestamp))
        print('='*len(timestamp))
        print("Task title: {}".format(entry.task_title))
        print("Employee Name: {}".format(entry.employee_name))
        print("Time spent on task in minutes: {}".format(entry.time_spent))
        print("Optional notes: {}".format(entry.optional_notes))
        print('\n'+'='*len(timestamp))
        print('n) next entry')
        print('u) update entry')
        print('d) delete entry')
        print('q) return to previous menu')

        next_action = input('Choice: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'u':
            update_entry(entry)
        elif next_action == 'd':
            delete_entry(entry)


def update_entry(entry):
    """Update entry"""
    print("\nEnter your changes as needed")
    entry.task_title = input("Task title: ")
    entry.time_spent = input('Time spent on task in minutes: ')
    entry.optional_notes = input('Optional Notes: ')
    entry.timestamp = datetime.datetime.strptime(input("Date (YYYY-MM-DD): "), '%Y-%m-%d')

    if input("Are you sure you accept changes? [yN] ").lower() == 'y':
        entry.save()
    clear()


def delete_entry(entry):
    """Delete an entry"""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()


def search_by_employee():
    """Search by employee name"""
    employee = input('Enter employee name: ')
    search_query = Entry.select().where(
        Entry.employee_name.contains(employee)).order_by(Entry.timestamp.desc())
    view_entries(search_query)


def search_by_date():
    """Search by specific date"""
    date = input('Enter a specific date (YYYY-MM-DD): ')
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    search_query = Entry.select().where(Entry.timestamp == date_object)
    view_entries(search_query)


def search_by_range_of_dates():
    """Search by range of dates"""
    start_date = input('Enter a start date (YYYY-MM-DD): ')
    start_date_object = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    end_date = input('Enter a end date (YYYY-MM-DD): ')
    end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    search_query = Entry.select().where(Entry.timestamp.between(
        start_date_object, end_date_object)).order_by(Entry.timestamp.desc())
    view_entries(search_query)


def search_by_time_spent():
    """Search by time spent"""
    time = int(input('Enter time spent: '))
    search_query = Entry.select().where(
        Entry.time_spent == time).order_by(Entry.timestamp.desc())
    view_entries(search_query)


def search_by_word():
    """Search by word"""
    word = input('Enter search word: ')
    search_query = Entry.select().where(
        (Entry.task_title.contains(word)) |
        (Entry.optional_notes.contains(word))).order_by(Entry.timestamp.desc())
    view_entries(search_query)


main_menu = OrderedDict([
    ('a', add_entry),
    ('b', search_menu_loop),
    ('v', view_entries),
])

search_menu = OrderedDict([
    ('a', search_by_employee),
    ('b', search_by_date),
    ('c', search_by_range_of_dates),
    ('d', search_by_time_spent),
    ('e', search_by_word),
])


def add_worklog():
    for log in work_log:
        try:
            Entry.create(task_title=log['task_title'],
                         employee_name=log['employee_name'],
                         time_spent=log['time_spent'],
                         optional_notes=log['optional_notes'])
        except IntegrityError:
            employee = Entry.get(employee_name=log['employee_name'])
            employee.task_title = log['task_title']
            employee.time_spent = log['time_spent']
            employee.optional_notes = log['optional_notes']
            employee.timestamp = log['timestamp']
            employee.save()


if __name__ == '__main__':
    initialize()
    add_worklog()
    main_menu_loop()
