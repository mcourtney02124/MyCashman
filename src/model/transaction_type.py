#!/usr/bin/env python3
from enum import Enum


class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    BALANCE = "BALANCE"
