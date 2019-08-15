import warnings

class BuildTable:
    def __init__(self, dbConn, filestream):
        self.sql_cursor = dbConn.cursor
        self.sql_database = dbConn.database
        self.filestream = filestream


    def insert_dates(self, dates):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nInserting dates...')

        for date in dates:
            self.sql_cursor.callproc('insert_date_search_results', [date])

    ###
    ### TODO OR NOT: something in here is broken but it only needs to delete the dummy...
    ###
    def insert_searches(self, searches, keywords, dates):
        with open(self.filestream, 'a+') as debug:
            debug.write('\nInserting search data...')

        for word in keywords:

            arg = [str(word)]
            try:
                self.sql_cursor.callproc('add_search_column', arg)
            except:
                with open(self.filestream, 'a+') as debug:
                    debug.write('\n   (\'{}\') search column already exists'.format(word))

            if (word != 'dummy'):
                for index in range(dates.size):
                    try:
                        args = [str(word), float(searches[word][index]), dates[index]]
                        try:
                            self.sql_cursor.callproc('add_data_point_search', args)
                        except:
                            warnings.warn("WARNING: data point rejected :::: ARGS: " + str(args))
                    except:
                        pass

        self.sql_cursor.execute('ALTER TABLE search_results DROP COLUMN dummy')
