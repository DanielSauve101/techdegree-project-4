"""Work Log

Created: 2019-05-01
Updated: 2019-05-01
Author: Daniel Sauve
"""

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *


db = SqliteDatabase('work_log.db')


class Entry(Model):
    task_title = CharField(max_length=100)
    employee_name = CharField(max_length=100)
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
    entries = Entry.select().where(Entry.employee_name.contains(employee))
    view_entries(entries)


def search_by_date():
    """Search by specific date"""
    date = input('Enter a specific date (YYYY-MM-DD): ')
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    entries = Entry.select().where(fn.date_trunc('day', Entry.timestamp) == date_object)
    # Possible second solution
    # entries = Entry.select().where(Entry.timestamp.day == date_object.day)
    view_entries(entries)


def search_by_range_of_dates():
    """Search by range of dates"""
    pass


def search_by_time_spent():
    """Search by time spent"""
    pass


def search_by_word():
    """Search by word"""
    pass


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


if __name__ == '__main__':
    initialize()
    main_menu_loop()
