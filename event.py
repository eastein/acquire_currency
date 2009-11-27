import account

class Event :
	def trigger(self) :
		raise NotImplementedError("cannot trigger the base event.")

class Expense(Event) :
	def __init__(self, account, amount) :
		self.account = account
		self.amount = amount

	def trigger(self) :
		account.Expense(self.account, self.amount)

class Income(Event) :
	def __init__(self, account, amount) :
		self.account = account
		self.amount = amount

	def trigger(self) :
		account.Income(self.account, self.amount)

class Payment(Event) :
	def __init__(self, source, dest, amount) :
		self.source = source
		self.dest = dest
		self.amount = amount

	def trigger(self) :
		account.Transfer(self.source, self.dest, self.amount)

class MinimumPayment(Event) :
	def __init__(self, source, loan) :
		self.source = source
		self.loan = loan

	def trigger(self) :
		self.loan.payMinimum(self.source)

class ChargeInterest(Event) :
	def __init__(self, loan) :
		self.loan = loan

	def trigger(self) :
		self.loan.chargeInterest()

def compare_interest(l1, l2) :
	if l1.interest > l2.interest :
		return 1
	elif l1.interest == l2.interest :
		return 0
	else :
		return -1

class BringCashToMinimum(Event) :
	def __init__(self, model, cash, boundary) :
		self.model = model
		self.cash = cash
		self.boundary = boundary

	def trigger(self) :
		spareCash = self.model.netAssets() - self.boundary

		while spareCash > 0.0 :
			# select the highest interest rate liability with any remaining balance.
			due = filter(lambda l: l.balance > 0.0, self.model.liabilities.values())
			if due :
				due.sort(cmp=compare_interest)
				highest = due.pop()
			
				transfer = min(spareCash, highest.balance)
				account.Transfer(self.cash, highest, transfer, 'paying extra to pay down debt')
				spareCash = self.model.netAssets() - self.boundary
			else :
				break

class Schedule :
	def __init__(self) :
		self.events = []

	def schedule(self, event) :
		if event not in self.events :
			self.events.append(event)

	def unschedule(self, event) :
		if event in self.events :
			self.events.remove(event)

	def condition(self, dt) :
		raise NotImplementedError("cannot tell what the condition is.")

	def run(self, dt) :
		if self.condition(dt) :
			for event in self.events :
				event.trigger()

class Periodic(Schedule) :
	def __init__(self, firstdate, period) :
		Schedule.__init__(self)
		self.firstdate = firstdate
		self.period = period

	def condition(self, dt) :
		return (dt - self.firstdate).days % self.period == 0

class Daily(Schedule) :
	def condition(self, dt) :
		return True

class Monthly(Schedule) :
	def condition(self, dt) :
		return dt.day == 1