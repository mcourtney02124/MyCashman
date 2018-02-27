import datetime as dt
import logging

from marshmallow import Schema, fields

#logging.basicConfig(filename='transaction.log', level = logging.INFO)

class Transaction(object):
  def __init__(self, description, amount, type):
    self.description = description
    self.amount = amount
    self.created_at = dt.datetime.now()
    self.type = type
    logging.info(str(self.created_at) + " " + self.type.value + " " + self.description + " " + str(self.amount) + "\n")

  def __repr__(self):
    return '<Transaction(name={self.description!r})>'.format(self=self)


class TransactionSchema(Schema):
  description = fields.Str()
  amount = fields.Number()
  created_at = fields.Date()
  type = fields.Str()

