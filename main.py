import webapp2
from jinja2 import Environment, FileSystemLoader
import cgi
import os
import yaml
import json
from simpledash import Dashboard

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
		
		t = Dashboard.from_yaml(dashboard_name).generate_template()

		template = env.from_string(t)
		self.response.write(template.render())

class DataHandler(webapp2.RequestHandler):
	def get(self, dashboard_name, widget_name, action):
		d = Dashboard.from_yaml(dashboard_name)
		widget = d.get_widget(widget_name)
		result = ""
		if action == "config":
			result = widget.generate_config()
		elif action == "data":
			result = widget.get_data()
		self.response.headers['Content-type'] = "application/json"
		self.response.write(result)
	
		
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
