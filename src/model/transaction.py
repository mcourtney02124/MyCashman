#!/usr/bin/env python3
import datetime as dt
import logging

from marshmallow import Schema, fields

unique = 0

#logging.basicConfig(filename='transaction.log', level = logging.INFO)

class Transaction(object):
    def __init__(self, description, amount, type):
        global unique
        unique += 1
        self.description = description
        self.amount = amount
        self.created_at = dt.datetime.now()
        self.type = type
        self.id = unique
        logging.info("record " + str(self.id) + " " + str(self.created_at) + " " + self.type.value + " " + self.description + " " + str(self.amount) + "\n")
        if self.description.find("covert") >= 0:
            logging.info("record " + str(self.id) + " is covert, raise alarm")

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)


class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    created_at = fields.Date()
    type = fields.Str()
    id = fields.Integer()

