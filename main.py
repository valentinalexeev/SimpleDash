import webapp2
from jinja2 import Environment, FileSystemLoader
import cgi
import os
import yaml
import json

env = Environment(loader = FileSystemLoader(["templates/", "layouts/", "widgets/", "dashboards/"]))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        result_html = []
        result_yaml = []
        for dirname, dirnames, filenames in os.walk("dashboards/"):
            for filename in filenames:
            	if filename.count(".html") > 0:
            		result_html.append(filename.split('.')[0])
            	elif filename.count(".yaml"):
            		result_yaml.append(filename.split('.')[0])
        template = env.get_template("template_index.html")
        self.response.write(template.render(dashboards_html=result_html, dashboards_yaml=result_yaml))

class RenderHandler(webapp2.RequestHandler):
    def get(self):
        dashboard_name = cgi.escape(self.request.params['dashboard'])
        # TODO: pass remaining parameters to templates
        template = env.get_template(dashboard_name + ".html")
        self.response.write(template.render())

class RenderYamlHandler(webapp2.RequestHandler):
	def get(self):
		dashboard_name = cgi.escape(self.request.params['dashboard'])
		# load YAML file, UNSAFE
		dashboard = yaml.load(file("dashboards/%s.yaml" % dashboard_name, "r"))
		t = """{%% extends '%s' %%}
{%% block title %%}%s{%% endblock %%}
""" % (dashboard['layout'], dashboard['title'])
		
		for dirname, dirnames, filenames in os.walk("widgets/"):
			for filename in filenames:
				if filename.count(".html") == 0:
					continue
				name = filename.split('.', 2)[0]
				t = t + "{%% import '%s' as %s %%}\n" % (filename, name)
		
		for widget in dashboard['widgets'].keys():
			data = dashboard['widgets'][widget]
			data['id'] = widget
			if 'datasource' not in data:
				data['datasource'] = '/data/%s/%s' % (dashboard_name, widget)
			t = t + "{%% block %(id)s %%}{{ %(type)s.%(type)s('%(id)s', '%(datasource)s') }}{%% endblock %%}\n" % data
		print t
		template = env.from_string(t)
		self.response.write(template.render())

class DataHandler(webapp2.RequestHandler):
	def get(self, dashboard_name, widget_name, action):
		dashboard = yaml.load(file("dashboards/%s.yaml" % dashboard_name, "r"))
		widget = dashboard['widgets'][widget_name]
		result = ""
		if action == "config":
			result = self.getConfig(dashboard, widget, dashboard_name, widget_name)
		elif action == "data":
			result = self.getData(dashboard, widget, dashboard_name, widget_name)
		self.response.headers['Content-type'] = "application/json"
		self.response.write(result)
	
	def getConfig(self, dashboard, widget, dashboard_name, widget_name):
		config = widget['config']
		return '{ "config": %s }' % json.dumps(config, sort_keys=True, indent=4)
	def getData(self, dashboard, widget, dashboard_name, widget_name):
		result = []
		for series in widget['data']:
			if 'static' in series:
				result.append(series['static'])
			elif 'db' in series:
				self.fetchDbData(dashboard, series, result)
		return '{ "data": %s }' % json.dumps(result, sort_keys=True, indent=4)

	def fetchDbData(self, dashboard, series, result):
		conn = None
		cur = None
		res = None
		
		# connect to db
		datasource = dashboard['datasource'][series['db']['source']]
		if datasource['type'] == 'sqlite':
			import sqlite3
			conn = sqlite3.connect(datasource['database'])
			cur = conn.cursor()
			res = cur.execute(series['db']['request']);
		elif datasource['type'] == 'mysql':
			pass
		elif datasource['type'] == 'csv':
			import csv
			res = conn = csv.reader(open(datasource['database'], 'rb'), dialect = datasource['dialect'])
						
		if not conn:
			return

		# fetch results "series name", "data point", "stack id"			
		dbresult = {}
		for row in res:
			print row
			if not row[0] in dbresult:
				dbresult[row[0]] = {"data": [], "name": row[0], "stack": row[2]}
			dbresult[row[0]]['data'].append(row[1])

		# cleanup
		if cur:
			cur.close()
		
		# import results
		for name in dbresult.keys():
			result.append(dbresult[name])
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/render', RenderHandler),
    ('/renderYaml', RenderYamlHandler),
    ('/data/(\w+)/(\w+)/(\w+)', DataHandler)
], debug=True)

def main():
    from paste import httpserver
    from paste.urlmap import URLMap
    from paste.urlparser import make_static
    map_app = URLMap()
    map_app['/'] = app
    map_app['/static'] = make_static({}, "static/")
    httpserver.serve(map_app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
