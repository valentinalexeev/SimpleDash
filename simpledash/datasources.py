class Datasource(object):
    name = None
    database = None

    def __init__(self, name, config):
        self.name = name
        database = config['database']
        pass

class XLSDatasource(Datasource):
    def __init__(self, name, config):
        super(Datasource, self).__init__(name, config)
        pass

class CSVDatasource(Datasource):
    def __init__(self, name, config):
        super(Datasource, self).__init__(name, config)
        pass

class SQLiteDatasource(Datasource):
    def __init__(self, name, config):
        super(Datasource, self).__init__(name, config)
        import sqlite3
        pass

    @classmethod    
    def get_data(klass, config, series):
        ds = config[series['source']]
        import sqlite3
        conn = sqlite3.connect(ds['database'])
        cur = conn.cursor()
        res = cur.execute(series['request']);
        
        # fetch results "series name", "data point", "stack id"         
        dbresult = {}
        for row in res:
            if not row[0] in dbresult:
                dbresult[row[0]] = {"data": [], "name": row[0], "stack": row[2]}
            dbresult[row[0]]['data'].append(row[1])
            
        # cleanup
        if cur:
            cur.close()
        
        result = []
        # import results
        for name in dbresult.keys():
            result.append(dbresult[name])

        cur.close()
        return result

class MySQLDatasource(Datasource):
    def __init__(self, name, config):
        super(Datasource, self).__init__(name, config)
        pass

class StaticDatasource(Datasource):
    def __init__(self, name, config):
        super(Datasource, self).__init__(name, config)
        pass

    @classmethod    
    def get_data(klass, config, series):
        result = [ series ]
        return result

class DatasourceFactory:
    datasourceConfig = None

    datasourceTypes = {
        "csv": CSVDatasource,
        "xls": XLSDatasource,
        "mysql": MySQLDatasource,
        "sqlite": SQLiteDatasource,
        "static": StaticDatasource
    }

    @classmethod
    def set_config(klass, config):
        klass.datasourceConfig = config
    
    @classmethod
    def get_data(klass, dataConfig):
        result = []
        for series in dataConfig:
            for type in series:
                for row in klass.datasourceTypes[type].get_data(klass.datasourceConfig, series[type]):
                    result.append(row)
        return result