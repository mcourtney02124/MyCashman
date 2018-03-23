#!/usr/bin/env python3
from marshmallow import post_load
from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Balance(Transaction):
  def __init__(self, description, amount):
    super(Balance, self).__init__(description, amount, TransactionType.BALANCE)

  def __repr__(self):
    return '<Balance(name={self.description!r})>'.format(self=self)


class BalanceSchema(TransactionSchema):
  @post_load
  def make_balance(self, data):
    return Balance(**data)

