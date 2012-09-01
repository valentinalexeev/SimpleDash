import yaml
from simpledash.datasources import DatasourceFactory
from simpledash.charts import ChartFactory

class Dashboard:
    title = None

    widgets = {}
    
    layout = None

    @classmethod
    def from_yaml(klass, filename):
        config = yaml.load(file("dashboards/%s.yaml" % filename, "r"))
        
        dashboard = Dashboard()
        dashboard.title = config['title']
        dashboard.layout = config['layout']
    
        print config    
        if 'datasource' in config:
            DatasourceFactory.set_config(config['datasource'])
        
        for widget in config['widgets'].keys():
            wg = ChartFactory.from_config(filename.split('.')[0], widget, config['widgets'][widget])
            dashboard.widgets[widget] = wg
        
        return dashboard

    def generate_template(self):
        t = """{%% extends '%s' %%}
{%% block title %%}%s{%% endblock %%}
""" % (self.layout, self.title)
        t = t + ChartFactory.generate_imports(self.widgets)
        t = t + ChartFactory.generate_blocks(self.widgets)
        return t
    
    def get_widget(self, widget_name):
        return self.widgets[widget_name]