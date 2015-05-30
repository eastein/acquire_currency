import datetime
import plot


class Model:

    def __init__(self):
        self.assets = {}
        self.liabilities = {}
        self.schedules = []

    def addAsset(self, account):
        self.assets[account.name] = account

    def addLiability(self, account):
        self.liabilities[account.name] = account

    def addSchedule(self, schedule):
        if schedule not in self.schedules:
            self.schedules.append(schedule)

    # calculate state
    def netAssets(self):
        netassets = 0.0
        for asset in self.assets.values():
            netassets += asset.balance
        return netassets

    def netLiabilities(self):
        netliabilities = 0.0
        for liability in self.liabilities.values():
            netliabilities += liability.balance
        return netliabilities

    def netWorth(self):
        return self.netAssets() - self.netLiabilities()

    def evaluateMetricsOverPeriod(self, metricList, startdate, days):
        graphableLines = {}
        for metric in metricList:
            graphableLines[metric.name] = []

        dates = []

        for i in range(days):
            today = startdate + datetime.timedelta(i)
            dates.append(today.date())

            # evaluate metrics
            todaysdata = {}
            for metric in metricList:
                data = metric.evaluate(self)
                todaysdata[metric.name] = data
                graphableLines[metric.name].append(data)

            # determine today's date to iterate
            for schedule in self.schedules:
                schedule.run(today)

        return dates, graphableLines

    def plotMetricsOnceOverPeriod(self, metrics, days, startdate=datetime.datetime.today()):
        dates, lines = self.evaluateMetricsOverPeriod(metrics, startdate, days)
        linelist = [
            (lines['Net Worth'], 'g-'),
            (lines['Net Assets'], 'b-'),
            (lines['Net Liabilities'], 'r-'),
        ]

        plot.plot(dates, linelist)

        return lines['Net Worth'].pop()

    @classmethod
    def plotAggregateMetricsOverPeriod(cls, model_module, metrics, samples, days, startdate=datetime.datetime.today()):
        sampleset = []
        for i in range(samples):
            model_instance = Model.createModel(model_module)
            dates, lines = model_instance.evaluateMetricsOverPeriod(metrics, startdate, days)
            sampleset.append(lines)

        PERCENTILES = [10, 25, 50, 75, 90]
        PERCENTILE_DASH = [2]

        percentile_indexes = []
        for p in PERCENTILES:
            percentile_indexes.append(int(samples * float(p) / 100.0))

        METRICS_TO_COLOR = {
            'Net Worth': 'g',
            'Net Assets': 'b',
            'Net Liabilities': 'r'
        }

        graph_lines = []
        for metric_name in METRICS_TO_COLOR:
            percentile_datalines = [[]] * len(PERCENTILES)
            for d_idx in range(days):
                values_for_metric = []
                for run_idx in range(samples):
                    values_for_metric.append(sampleset[run_idx][metric_name][d_idx])

                percs = []
                values_for_metric.sort()
                for percentile_idx_idx in range(len(percentile_indexes)):
                    percentile_idx = percentile_indexes[percentile_idx_idx]
                    percentile_value = values_for_metric[percentile_idx]
                    percentile_datalines[percentile_idx_idx].append(percentile_value)

                    percs.append(percentile_value)

                print 'percentiles for metric: %s' % str(percs)

            for percentile_idx_idx in range(len(PERCENTILES)):
                format = ''
                if percentile_idx_idx in PERCENTILE_DASH:
                    format = '-'
                graph_lines.append((percentile_datalines[percentile_idx_idx], METRICS_TO_COLOR[metric_name] + format))
        print len(graph_lines)
        plot.plot(dates, graph_lines)

    @classmethod
    def createModel(cls, model_module, **kwargs):
        return model_module.createModel(**kwargs)


class Metric:
    pass


class NetWorth(Metric):

    def __init__(self):
        self.name = 'Net Worth'

    def evaluate(self, m):
        return m.netWorth()


class NetAssets(Metric):

    def __init__(self):
        self.name = 'Net Assets'

    def evaluate(self, m):
        return m.netAssets()


class NetLiabilities(Metric):

    def __init__(self):
        self.name = 'Net Liabilities'

    def evaluate(self, m):
        return m.netLiabilities()


class InDebt(Metric):

    def __init__(self):
        self.name = 'In Debt'

    def evaluate(self, m):
        return m.netLiabilities() > 0.0

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: model.py modelmodule'
        sys.exit(1)

    model_module = __import__(sys.argv[1])

    metrics = [NetAssets(), NetLiabilities(), NetWorth()]

    if len(sys.argv) == 2:
        mymodel = Model.createModel(model_module)
        print mymodel.plotMetricsOnceOverPeriod(metrics, days=365 * 2)
    elif len(sys.argv) == 4 and sys.argv[2] == '-samples':
        samples = int(sys.argv[3])
        Model.plotAggregateMetricsOverPeriod(model_module, metrics, samples, days=365 * 2)
