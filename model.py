import datetime
import plot

class Model :
	def __init__(self) :
		self.assets = {}
		self.liabilities = {}
		self.schedules = []

	def addAsset(self, account) :
		self.assets[account.name] = account

	def addLiability(self, account) :
		self.liabilities[account.name] = account

	def addSchedule(self, schedule) :
		if schedule not in self.schedules :
			self.schedules.append(schedule)

	# calculate state
	def netAssets(self) :
		netassets = 0.0
		for asset in self.assets.values() :
			netassets += asset.balance
		return netassets

	def netLiabilities(self) :
		netliabilities = 0.0
		for liability in self.liabilities.values() :
			netliabilities += liability.balance
		return netliabilities

	def netWorth(self) :
		return self.netAssets() - self.netLiabilities()

	def evaluateMetricsOverPeriod(self, metricList, startdate, days) :
		graphableLines = {}
		for metric in metricList :
			graphableLines[metric.name] = []

		dates = []

		for i in range(days) :
			today = startdate + datetime.timedelta(i)
			dates.append(today.date())

			# evaluate metrics
			todaysdata = {}
			for metric in metricList :
				data = metric.evaluate(self)
				todaysdata[metric.name] = data
				graphableLines[metric.name].append(data)

			# determine today's date to iterate
			for schedule in self.schedules :
				schedule.run(today)
		
		return dates, graphableLines

	def plotMetricsOnceOverPeriod(self, metrics, days, startdate=datetime.datetime.today()) :
		dates, lines = self.evaluateMetricsOverPeriod(metrics, startdate, days)
		linelist = [
			(lines['Net Worth'], 'g-'),
			(lines['Net Assets'], 'b-'),
			(lines['Net Liabilities'], 'r-'),
		]

		plot.plot(dates, linelist)

		return lines['Net Worth'].pop()


	@classmethod
	def plotMetricsOverPeriod(cls, model_module, metrics, days, startdate=datetime.datetime.today()) :
		PERCENTILES = [2, 10, 25, 50, 25, 90, 98]

	@classmethod
	def createModel(cls, model_module, **kwargs) :
		return model_module.createModel(**kwargs)

class Metric :
	pass

class NetWorth(Metric) :
	def __init__(self) :
		self.name = 'Net Worth'

	def evaluate(self, m) :
		return m.netWorth()

class NetAssets(Metric) :
	def __init__(self) :
		self.name = 'Net Assets'

	def evaluate(self, m) :
		return m.netAssets()

class NetLiabilities(Metric) :
	def __init__(self) :
		self.name = 'Net Liabilities'

	def evaluate(self, m) :
		return m.netLiabilities()

class InDebt(Metric) :
	def __init__(self) :
		self.name = 'In Debt'

	def evaluate(self, m) :
		return m.netLiabilities() > 0.0

if __name__ == '__main__' :
	import sys
	if len(sys.argv) < 2 :
		print 'usage: model.py modelmodule'
		sys.exit(1)

	model_module = __import__(sys.argv[1])

	metrics = [NetAssets(), NetLiabilities(), NetWorth()]

	if len(sys.argv) == 2 :
		mymodel = Model.createModel(model_module)
		print mymodel.plotMetricsOnceOverPeriod(metrics, days=365*2)
	elif len(sys.argv) == 4 and sys.argv[2] == '-samples' :
		times = int(sys.argv[3])
		Model.plotMetricsOverPeriod(model_module, metrics, days=365*2)

