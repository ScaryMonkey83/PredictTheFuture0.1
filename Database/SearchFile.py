import numpy as np
import datetime
from dateutil import parser

from matplotlib import pyplot as plot


class SearchFile:
    def __init__(self, goog_login, filestream):
        self.login = goog_login
        self.filestream = filestream
        self.trends_raw = []
        self.keywords = []
        self.trends = {}
        self.dates = []

        self.__efficiency__ = 0

    # Reads file and searches for each term in the file
    def read_database(self, dic):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nSearching terms...')

        for line in dic:
            with open(self.filestream, 'a+') as debug:
                debug.write('\n    {}'.format(line))
            # Create payload and capture API tokens. Only needed for interest_over_time(),
            # interest_by_region() & related_queries()
            self.login.build_payload(kw_list=[line[0]])

            interest_over_time_df = self.login.interest_over_time()
            self.trends_raw = np.append(self.trends_raw, interest_over_time_df.to_dict())
            self.keywords = np.append(self.keywords, line)
        self.keywords = np.append(self.keywords, 'dummy')

    # isolates the numbers without the dates in new dictionary
    def refine_dict(self):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nRefining data...')

        new = []

        for ii in np.arange(0, self.trends_raw.size):
            for key in self.trends_raw[ii][self.keywords[ii]]:
                new = np.append(new, self.trends_raw[ii][self.keywords[ii]][key])

            self.trends[self.keywords[ii]] = new
            new = []

    # gets all the dates which hold data in the trends_raw array
    def get_dates(self):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nRetrieving dates...')

        self.__efficiency__ = 0

        for ii in np.arange(0, self.trends_raw.size):
            for search in self.trends_raw[ii][self.keywords[ii]]:
                if search not in self.dates:
                    self.__efficiency__ += 1
                    self.dates = np.append(self.dates, parser.parse(str(search)))


    def graph_trend(self, keyword):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nGraphing trend...')

        x = np.arange(0, self.trends[keyword].size)
        y = self.trends[keyword]

        plot.plot(x, y)
        plot.title(keyword)
        plot.show()
