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
    optional_notes = TextField()
    timestamp = TimestampField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


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


def search_entries():
    """Search entries"""
    pass


def view_entries():
    """View entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    for entry in Entry.select():
        timestamp = entry.timestamp.strftime('%B %d %Y, %I:%M%p')
        clear()
        print("Date entered: {}".format(timestamp))
        print('='*len(timestamp))
        print("Task title: {}".format(entry.task_title))
        print("Employee Name: {}".format(entry.employee_name))
        print("Time spent on task in minutes: {}".format(entry.time_spent))
        print("Optional notes: {}".format(entry.optional_notes))
        print('\n'+'='*len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def delete_entry(entry):
    """Delete an entry"""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()


menu = OrderedDict([
    ('a', add_entry),
    ('b', search_entries),
    ('v', view_entries),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
