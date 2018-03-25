#!/usr/bin/env python3
"""
Based on the "cashman" application found at https://auth0.com/blog/developing-restful-apis-with-python-and-flask/
This version is for Meredith Courtney's experiments with a REST API

Top level of Flask application implementing a REST API for managing income and expenses

"""

import os
import datetime as dt
import logging
import time
from subprocess import TimeoutExpired
from flask import Flask, jsonify, request
# import pysipp looks like pysipp will not run on Linux only, not Mac - AttributeError: module 'select' has no attribute 'epoll'

from src.model.transaction import Transaction, TransactionSchema
from src.model.expense import Expense, ExpenseSchema
from src.model.income import Income, IncomeSchema
from src.model.balance import Balance, BalanceSchema
from src.model.transaction_type import TransactionType
from src.sipp_procs import SippServer



app = Flask(__name__)

uas = SippServer(script="uas_ivr_balance.xml")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

serverProc = SippServer.launch(uas)

time.sleep(5)

logging.basicConfig(filename='transaction.log', filemode = 'w', level = logging.INFO)
logging.info("starting REST test application")

balance = 0.0

transactions = []

first_income = Income('Salary',5000)
second_income = Income('Dividends', 200)
first_expense = Expense('pizza', 50)
second_expense = Expense('Rock Concert', 100)

balance += first_income.amount
transactions.append(first_income)

balance += second_income.amount
transactions.append(second_income)

balance += first_expense.amount
transactions.append(first_expense)

balance += second_expense.amount
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
    global balance
    income = IncomeSchema().load(request.get_json())
    transactions.append(income.data)
    balance += income.data.amount
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
    global balance
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense.data)
    balance += expense.data.amount
    if balance < 0.0:
        logging.info("expense " + str(expense.data.id) + " has caused negative balance, raise alarm")
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

@app.route('/get_balance', methods=['POST'])
def get_balance():
    global balance
    r = request.get_json()
    balance_inquiry = BalanceSchema().load(request.get_json())
    transactions.append(balance_inquiry.data)
    logging.info("Balance inquiry at  " + str(dt.datetime.now()) + "balance is currently " + str(balance))
    return jsonify({"balance": balance})

@app.route('/shutdown')
def shutdown():
    global serverProc
    try:
        outs, errs = serverProc.communicate(input = "q", timeout = 15)
    except TimeoutExpired:
        serverProc.kill()
        outs, errs = serverProc.communicate()

    print (errs)

    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run()

