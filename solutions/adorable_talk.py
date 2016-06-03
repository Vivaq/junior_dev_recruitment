# -*- coding: utf-8 -*-
# Hello! Good luck!

##############
#   TASK 1   #
##############

import json
import types
from datetime import date


class DateForJson(date):  # json can't print 'date' object, so I have to convert it to string
    def __repr__(self):
        return str({'year': self.year, 'month': self.month, 'day': self.day})


class Ticket(object):
    def __init__(
            self,
            ticket_id,  # the unique identifier of the ticket;
            event_date,  # the date of the event;
            event_time,  # the time when event occurs;
            event_name,  # the event name -> obvious one :);
            client,  # the INSTANCE of the client;
            room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.client.add_ticket_id(self.ticket_id)
        self.room_number = room_number

    def __repr__(self):
            return str({x: y for (x, y) in self.__dict__.iteritems() if x[0] != '_' and not hasattr(x, '__call__')})
            # iterates over 'public' attributes, it has to return string

    def get_ticket_data(self):
        return json.dumps(eval(self.__repr__()), indent=3)

    def change_ticket_id(self, new_id):  # simple observer
        c.update_ids(self.ticket_id, new_id)
        self.ticket_id = new_id


class Client:
    def __init__(
            self,
            first_name,
            last_name,
            birth_date,
            sex,
    ):
        self.ids = []
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def __repr__(self):
        return str({x: y for (x, y) in self.__dict__.items() if x[0] is not '_' and not hasattr(x, '__call__')})

    def can_watch_pegi(self, min_age):
        if min_age not in [3, 7, 12, 16, 18]:
            raise ValueError('incorrect min_age')
        return date.today().year - self.birth_date.year + (1 if date.today().month > self.birth_date.month else 0) >= min_age

    def add_ticket_id(self, ticket_id):
        self.ids.append(ticket_id)

    def get_ticket_ids(self):
        return self.ids

    def update_ids(self, old_id, new_id):
        self.ids[self.ids.index(old_id)] = new_id

##############
#   TASK 2   #
##############


def iterate_over_list(some_list):
    try:
        return [int(element) + i for (i, element) in enumerate(some_list)]
    except ValueError:
        return [element * i for (i, element) in enumerate(some_list)]

###########
#  Tests  #
###########

if __name__ == '__main__':
    c = Client('Jan', 'Kowalski', DateForJson(2000, 1, 1), 'Male')
    t1 = Ticket(235, DateForJson(2016, 5, 7), 18, 'Cinema', c, 134)
    t2 = Ticket(857, DateForJson(2017, 8, 3), 12, 'Party', c, 12)
    print t1.get_ticket_data()
    print c.get_ticket_ids()
    t1.change_ticket_id(5)
    print c.get_ticket_ids()
    print c.can_watch_pegi(18)
    #print c.can_watch_pegi(9) #error
    print c.can_watch_pegi(7)
    print iterate_over_list([1, 3, 5])
    print iterate_over_list(['a', 'b', 'c'])

##############
#   TASK 3   #
##############

# sql = 'SELECT location_city, COUNT(*) FROM poi GROUP BY location_city'

# I wrote complete program to be make it works :)
"""
import sqlite3
import os
from random import randint

db = sqlite3.connect(os.getcwd() + '\database.sqlite3')
c = db.cursor()
c.execute('''CREATE TABLE poi (
	 id SERIAL PRIMARY KEY,
	 name TEXT,
	 location_city TEXT,
	 location_country TEXT,
	 latitude NUMERIC,
	 longitude NUMERIC
	 )''')
for i in xrange(1000):
    c.execute('INSERT INTO poi (location_city) VALUES (' + ['"Warsaw"', '"London"', '"Moscow"'][randint(0, 2)] + ')') # inserting into db
c.execute('SELECT location_city, COUNT(*) FROM poi GROUP BY location_city')  # <= query for checking poi in city
print '\n'.join([str(x).replace(',', '|') for x in c.fetchall()]) # pretty print
db.commit()
"""

# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?

# -We can use 'INDEX', it decreases number of comparisons (binary search-complexity O(log n))
# -We can pull only data, which we need
# -We should avoid queries in loops
