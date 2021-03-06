# -*- coding: utf-8 -*-

import unittest
from datetime import date, datetime
from dateutil import relativedelta
dates_difference = relativedelta.relativedelta
import json

##############
#   TASK 1   #
##############


class Ticket(object):
    def __init__(
        self,
        ticket_id,    # the unique identifier of the ticket;
        event_date,   # the date of the event;
        event_time,   # the time when event occurs;
        event_name,   # the event name -> obvious one :);
        client,       # the INSTANCE of the client;
        room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number

        self.client.add_ticket(self.ticket_id)

    def get_ticket_data(self, *, json_format=True):
        data = {
            "event_time":  self.event_time,
            "event_name":  self.event_name,
            "room_number": self.room_number,
            "ticket_id":   self.ticket_id,
            "event_date":  self.event_date,
            "client":      self.client.get_client_data(json_format=False)
        }
        return json.dumps(data) if json_format else data


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

        self.bought_tickets = set()

    def get_client_data(self, *, json_format=True):
        data = {
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'birth_date': self.birth_date,
            'sex':        self.sex
        }
        return json.dumps(data) if json_format else data

    def add_ticket(self, ticket_id):
        self.bought_tickets.add(ticket_id)

    def get_ticket_ids(self):
        return self.bought_tickets

    def get_age(self):
        birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
        return dates_difference(date.today(), birth_date)

    def can_watch_pegi(self, mark):
        assert mark in [3, 7, 12, 16, 18]  # assert the argument is a PEGI mark
        return self.get_age().years >= mark


# SUBTASK 2
# define a method on Ticket: get_ticket_data, which returns dumped JSON object
# with all data on ticket, and all data on client;


# SUBTASK 3
# Write a method (name: can_watch_pegi ;)) on client which check if he is able
# to watch the movie - according to PEGI
# assume following age marks: 3, 7, 12, 16, 18;
# Method should return True or False -> True means that client is older than
# restriction and can watch the movie;


# SUBTASK 4
# Propose a structure where client instance will have some interface to get the
# all ticket ids - whenever added, which returns all ticket ids;


class Task1Tests(unittest.TestCase):
    def test_ticket_data_storing(self):
        client = Client('fname', 'lname', '1994-03-11', 'male')
        ticket1 = Ticket('12345678', '2016-06-05', '19:00',
                         'example event', client, '6')
        ticket2 = Ticket('8765431', '2016-06-05', '19:00',
                         'example event', client, '6')
        ticket3 = Ticket('12343141', '2016-06-05', '19:00',
                         'example event', client, '6')

        self.assertEqual({'12345678', '8765431', '12343141'},
                         client.get_ticket_ids())

    def test_pegi_marks(self):
        client = Client('fname', 'lname', '2003-03-01', 'female')
        self.assertTrue(client.can_watch_pegi(3))
        self.assertTrue(client.can_watch_pegi(12))
        self.assertFalse(client.can_watch_pegi(16))
        self.assertFalse(client.can_watch_pegi(18))

    def test_json_serializing(self):
        client = Client('fname', 'lname', '1985-11-05', 'male')
        ticket = Ticket('7821471', '2016-08-31', "12:00",
                        'example event', client, '3')

        serialized_data = ticket.get_ticket_data()
        valid_data = [
            '"event_name": "{}"'.format(ticket.event_name),
            '"last_name": "{}"'.format(client.last_name)
        ]
        invalid_data = [
            '"tic_id": "{}"'.format(ticket.ticket_id),
            '"sex": "{}"'.format(client.first_name)
        ]

        for item in valid_data:
            self.assertTrue(item in serialized_data)

        for item in invalid_data:
            self.assertTrue(item not in serialized_data)


##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;

def iterate_over_list(some_list):
    if any(type(s) == str for s in some_list):
        return [x * index for x, index in enumerate(some_list)]
    else:
        return [x + index for x, index in enumerate(some_list)]

# SUBTASK 2
# and how handle this?
# in such case - method should repeat string index times;
# input -> ['a', 'b', 'c']; output: ['', 'b', 'cc'];


class Task2Tests(unittest.TestCase):
    def test_integers(self):
        self.assertEqual(iterate_over_list([5, 8, 4]), [5, 9, 6])

    def test_strings(self):
        self.assertEqual(iterate_over_list(['a', 'b', 'c']), ['', 'b', 'cc'])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            iterate_over_list([ [], (), {} ])


##############
#   TASK 3   #
##############

r"SELECT location_city, COUNT(1) FROM poi GROUP BY location_city"

# SUBTASK 1

# According to W3S we can create index on column location_city
# W3S: "Indexes allow the database application to find data fast;
#       without reading the whole table."


#######################

if __name__ == '__main__':
    unittest.main()
