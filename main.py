import webapp2
from jinja2 import Environment, FileSystemLoader
import cgi
import os
import yaml

env = Environment(loader = FileSystemLoader(["templates/", "layouts/", "widgets/", "dashboards/"]))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        result = []
        for dirname, dirnames, filenames in os.walk("dashboards/"):
            for filename in filenames:
                result.append(dict(id=filename, title=filename))
        template = env.get_template("template_index.html")
        self.response.write(template.render(dashboards=result))

class RenderHandler(webapp2.RequestHandler):
    def get(self):
        dashboard_name = cgi.escape(self.request.params['dashboard'])
        # TODO: pass remaining parameters to templates
        template = env.get_template(dashboard_name)
        self.response.write(template.render())

class RenderYamlHandler(webapp2.RequestHandler):
	def get(self):
		dashboard_name = cgi.escape(self.request.params['dashboard'])
		# load YAML file, UNSAFE
		dashboard = yaml.load(file("dashboards/%s" % dashboard_name, "r"))
		t = """
		{%% extends '%s' %%}
		{%% import "bar.html" as bar %%}
		{%% import "line.html" as line %%}
		{%% block title %%}%s{%% endblock %%}
		""" % (dashboard['layout'], dashboard['title'])
		
		for widget in dashboard['widgets'].keys():
			data = dashboard['widgets'][widget]
			data['id'] = widget
			t = t + "{%% block %(id)s %%}{{ %(type)s.%(type)s('%(id)s', '%(datasource)s') }}{%% endblock %%}" % data
		print t
		template = env.from_string(t)
		self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/render', RenderHandler),
    ('/renderYaml', RenderYamlHandler)
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
