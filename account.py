import math

# flux


class Income:

    def __init__(self, dest, amount):
        dest.give(amount)


class Expense:

    def __init__(self, source, amount):
        source.take(amount)


class Transfer:

    def __init__(self, source, dest, amount, name):
        self.amount = amount
        self.source = source
        self.dest = dest
        self.name = name

        print 'transferring $%0.2f from %s to %s: %s' % (amount, source.name, dest.name, name)
        source.take(amount)
        dest.give(amount)

# state


class Account:

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def take(self, amount):
        raise NotImplementedError("not implemented by base account.")

    def give(self, amount):
        raise NotImplementedError("not implemented by base account.")


class Asset(Account):

    def __init__(self, name, balance):
        Account.__init__(self, name, balance)

    def take(self, amount):
        self.balance -= amount

    def give(self, amount):
        self.balance += amount


class Liability(Account):

    def __init__(self, name, balance):
        Account.__init__(self, name, balance)

    def take(self, amount):
        self.balance += amount

    def give(self, amount):
        self.balance -= amount


class Loan(Liability):

    def effectiveMonthly(self):
        if not hasattr(self, 'ieff'):
            self.ieff = math.pow(1.0 + self.interest / 12.0, 1.0) - 1
        return self.ieff

    def chargeInterest(self):
        interest = self.effectiveMonthly() * 0.01 * self.balance
        Expense(self, interest)

    def payMinimum(self, source):
        payment = min(self.minimum_payment, self.balance)
        if payment > 0.0:
            Transfer(source, self, payment, "minimum loan payment")

    def __init__(self, name, interest, balance, minimum_payment):
        Liability.__init__(self, name, balance)
        self.interest = interest
        self.minimum_payment = minimum_payment

    @classmethod
    def compare_interest(cls, l1, l2):
        if l1.interest > l2.interest:
            return 1
        elif l1.interest == l2.interest:
            return 0
        else:
            return -1
