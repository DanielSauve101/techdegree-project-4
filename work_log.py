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
        print("\nEnter 'q' to quit.")
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in main_menu:
            clear()
            main_menu[choice]()
        elif choice == 'q':
            pass
        else:
            print('\nMust select (Abc or q)')


def search_menu_loop():
    """Search entries"""
    choice = None

    while choice != 'q':
        print("\nEnter 'q' to return to previous menu.")
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in search_menu:
            clear()
            search_menu[choice]()
        elif choice == 'q':
            pass
        else:
            print('\nMust select (Abcde or q)')


def add_entry():
    """Add an entry"""
    title = input('Please enter the title of the task: ')
    name = input('Enter your name: ')

    while True:
        try:
            time = int(input('Enter the time spent on task in minutes: '))
        except ValueError:
            print('\nValue must be a number. Please try again.')
        else:
            break

    notes = input('Enter any notes (Optional): ')

    if title and name and time:
        while True:
            save = input('Save entry [Yn] ').lower()
            if save == 'y':
                Entry.create(task_title=title,
                             employee_name=name,
                             time_spent=time,
                             optional_notes=notes
                             )
                print('\nEntry saved successfully!')
                break
            elif save == 'n':
                break
            elif save != 'y' or save != 'n':
                print('\nYou must enter [Yn]')


def view_entries(search_query=None):
    """View entries"""
    if search_query:
        entries = search_query
    else:
        entries = Entry.select().order_by(Entry.id.desc())

    length_of_entries = len(entries)
    index = 0
    timestamp = entries[index].timestamp.strftime('%B %d %Y')

    while True:
        clear()
        print('Date entered: {}'.format(timestamp))
        print('='*len(timestamp))
        print('Task title: {}'.format(entries[index].task_title))
        print('Employee Name: {}'.format(entries[index].employee_name))
        print('Time spent on task in minutes: {}'.format(
            entries[index].time_spent))
        print('Optional notes: {}'.format(entries[index].optional_notes))
        print('\n'+'='*len(timestamp))
        print('n) next entry')
        print('p) previous entry')
        print('u) update entry')
        print('d) delete entry')
        print('q) return to previous menu')

        next_action = input('Choice: [Npudq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'n':
            if index == (length_of_entries-1):
                index = 0
            else:
                index += 1
        elif next_action == 'p':
            if index == 0:
                index = (length_of_entries-1)
            else:
                index -= 1
        elif next_action == 'u':
            update_entry(entries[index])
            break
        elif next_action == 'd':
            delete_entry(entries[index])
            break


def update_entry(entry):
    """Update entry"""
    print('\nEnter your changes as needed')
    title = input('Please enter the title of the task: ')

    while True:
        try:
            time = int(input('Enter the time spent on task in minutes: '))
        except ValueError:
            print('\nValue must be a number. Please try again.')
        else:
            break

    notes = input('Enter any notes (Optional): ')

    while True:
        try:
            date = datetime.datetime.strptime(
                input('Date (YYYY-MM-DD): '), '%Y-%m-%d')
        except ValueError:
            print('You must use the following format (YYYY-MM-DD)')
        else:
            break

    if title and time and date:
        entry.task_title = title
        entry.time_spent = time
        entry.optional_notes = notes
        entry.timestamp = date
        entry.save()
        print('\nEntry successfully updated!')


def delete_entry(entry):
    """Delete an entry"""
    while True:
        option = input('Are you sure? [yN] ').lower()
        if option == 'y':
            entry.delete_instance()
            print('\nEntry successfully deleted!')
            break
        elif option == 'n':
            break
        elif option != 'y' or option != 'n':
            print('\nYou must enter [Yn]')


def search_by_employee():
    """Search by employee name"""
    employee = input('Enter employee name: ')

    search_query = Entry.select().where(
        Entry.employee_name.contains(employee)).order_by(Entry.timestamp.desc())

    if search_query:
        view_entries(search_query)
    else:
        print('\nNo employee matches found for {}'.format(employee))


def search_by_date():
    """Search by specific date"""
    while True:
        try:
            date = datetime.datetime.strptime(
                input('Date (YYYY-MM-DD): '), '%Y-%m-%d')
        except ValueError:
            print('\nYou must use the following format (YYYY-MM-DD)')
        else:
            break

    search_query = Entry.select().where(
        Entry.timestamp == date).order_by(Entry.id.desc())

    if search_query:
        view_entries(search_query)
    else:
        print('\nSorry but there are no entries found for that specific date')


def search_by_range_of_dates():
    """Search by range of dates"""
    while True:
        try:
            start_date = datetime.datetime.strptime(
                input('Start date (YYYY-MM-DD): '), '%Y-%m-%d')
        except ValueError:
            print('\nYou must use the following format (YYYY-MM-DD)')
        else:
            break

    while True:
        try:
            end_date = datetime.datetime.strptime(
                input('End date (YYYY-MM-DD): '), '%Y-%m-%d')
        except ValueError:
            print('\nYou must use the following format (YYYY-MM-DD)')
        else:
            break

    search_query = Entry.select().where(Entry.timestamp.between(
        start_date, end_date)).order_by(Entry.timestamp.desc())

    if search_query:
        view_entries(search_query)
    else:
        print('\nSorry but there are no entries found for that range of dates')


def search_by_time_spent():
    """Search by time spent"""
    while True:
        try:
            time = int(input('Enter time spent: '))
        except ValueError:
            print('\nValue must be a number. Please try again.')
        else:
            break

    search_query = Entry.select().where(
        Entry.time_spent == time).order_by(Entry.timestamp.desc())

    if search_query:
        view_entries(search_query)
    else:
        print('\nNo entries found with {} minutes.'.format(time))


def search_by_word():
    """Search by word"""
    word = input('Enter search word: ')

    search_query = Entry.select().where(
        (Entry.task_title.contains(word)) |
        (Entry.optional_notes.contains(word))).order_by(Entry.timestamp.desc())

    if search_query:
        view_entries(search_query)
    else:
        print('\nNo entry found with word {} in title or notes .'.format(word))


main_menu = OrderedDict([
    ('a', add_entry),
    ('b', search_menu_loop),
    ('c', view_entries),
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
