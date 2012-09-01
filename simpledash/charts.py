import json
from simpledash.datasources import DatasourceFactory

class Chart(object):
    def __init__(self, type, dashboard_name, name, config):
        self.type = type
        self.dashboard_name = dashboard_name
        self.name = name
        self.config = config
        self.title = config['title']
        if 'data' in config:
            self.data = config['data']
        if not 'datasource' in config:
            self.datasource = "/data/%s/%s" % (dashboard_name, name)
        else:
            self.datasource = config['datasource']
        pass
    
    def generate_import(self):
        return "{%% import '%s.html' as %s %%}\n" % (self.type, self.type)
    
    def generate_block(self):
        return "{%% block %s %%}{{ %s.%s('%s', '%s') }}{%% endblock %%}\n" % (self.name, self.type, self.type, self.name, self.datasource)
    
    def generate_config(self):
        cfg = {
            "config": {
                "title": {
                    "text": self.title
                }
            }
        }
        self.add_type_config(cfg['config'])
        return json.dumps(cfg, sort_keys=True, indent=4)
    
    def get_data(self):
        data = {
            "data": DatasourceFactory.get_data(self.data)
        }
        print data
        return json.dumps(data, sort_keys=True, indent=4)

class LineChart(Chart):
    def __init__(self, dashboard_name, name, config):
        Chart.__init__(self, "line", dashboard_name, name, config)
        self.xAxis = config['xAxis']
        self.yAxis = config['yAxis']
    
    def add_type_config(self, cfg):
        cfg['xAxis'] = self.xAxis
        cfg['yAxis'] = self.yAxis

class BarChart(Chart):
    def __init__(self, dashboard_name, name, config):
        Chart.__init__(self, "bar", dashboard_name, name, config)
        self.xAxis = config['xAxis']
        self.yAxis = config['yAxis']

    def add_type_config(self, cfg):
        cfg['xAxis'] = self.xAxis
        cfg['yAxis'] = self.yAxis

class PieChart(Chart):
    def __init__(self, dashboard_name, name, config):
        Chart.__init__(self, "pie", dashboard_name, name, config)

class ColumnChart(Chart):
    def __init__(self, dashboard_name, name, config):
        Chart.__init__(self, "column", dashboard_name, name, config)
        self.xAxis = config['xAxis']
        self.yAxis = config['yAxis']

    def add_type_config(self, cfg):
        cfg['xAxis'] = self.xAxis
        cfg['yAxis'] = self.yAxis

class ChartFactory:
    charts = {
        "line": LineChart,
        "bar": BarChart,
        "pie": PieChart,
        "column": ColumnChart,
    }
    
    @classmethod
    def from_config(klass, dashboard_name, name, config):
        return klass.charts[config['type']](dashboard_name, name, config)
    
    @classmethod
    def generate_imports(klass, widgets):
        # get list of chart types
        import_generators = {}
        for widget in widgets.values():
            import_generators[widget.type] = widget
        
        result = ""
        for w in import_generators.values():
            result = result + w.generate_import()
        return result

    @classmethod
    def generate_blocks(klass, widgets):
        result = ""
        for w in widgets.values():
            result = result + w.generate_block()
        return result