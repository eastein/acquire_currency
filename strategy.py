import account
import event


class Strategy(event.Event):
    pass


class BringCashToMinimum(Strategy):

    def __init__(self, model, cash, boundary):
        self.model = model
        self.cash = cash
        self.boundary = boundary

    def trigger(self):
        spareCash = self.model.netAssets() - self.boundary

        while spareCash > 0.0:
            # select the highest interest rate liability with any remaining balance.
            due = filter(lambda l: l.balance > 0.0, self.model.liabilities.values())
            if due:
                due.sort(cmp=account.Loan.compare_interest)
                highest = due.pop()

                transfer = min(spareCash, highest.balance)
                account.Transfer(self.cash, highest, transfer, 'paying extra to pay down debt')
                spareCash = self.model.netAssets() - self.boundary
            else:
                break
