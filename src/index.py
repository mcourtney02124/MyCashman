#!/usr/bin/env python3
"""
Based on the "cashman" application found at https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
This version is for Meredith Courtney's experiments with a REST API

Top level of Flask application implementing a REST API for managing income and expenses

"""

import os
import logging
import time
from flask import Flask, jsonify, request

from src.model.transaction import Transaction, TransactionSchema
from src.model.expense import Expense, ExpenseSchema
from src.model.income import Income, IncomeSchema
from src.model.transaction_type import TransactionType

app = Flask(__name__)


time.sleep(5)

logging.basicConfig(filename='transaction.log', filemode = 'w', level = logging.INFO)
logging.info("starting REST test application")

first_income = Income('Salary',5000)
second_income = Income('Dividends', 200)
first_expense = Expense('pizza', 50)
second_expense = Expense('Rock Concert', 100)

transactions = []

transactions.append(first_income)
transactions.append(second_income)
transactions.append(first_expense)
transactions.append(second_expense)


@app.route('/incomes')
def get_incomes():
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes.data)

@app.route('/incomes', methods=['POST'])
def add_income():
  income = IncomeSchema().load(request.get_json())
  transactions.append(income.data)
  return jsonify({"unique": income.data.id})

@app.route('/expenses')
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses.data)


@app.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense.data)
  return jsonify({"unique": expense.data.id})

@app.route('/get_item', methods=['POST'])
def get_item():
  r = request.get_json()
  number = r["number"]
  schema = TransactionSchema(many=True)
  item = schema.dump(
    filter(lambda t: t.id == number, transactions)
  )
  return jsonify(item.data[0])


if __name__ == "__main__":
    app.run()

