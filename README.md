SimpleDash
==========

All dashboards apps ... are bad. This one maybe not as much.

Rationale
=========

You have a database, spreadsheet, XML, you-name-it and you need some graphs out of it.
Something that you can look at and understand what's happening. Either with your business
or with the equipment or with ... 

There is a whole set of tools related to the topic. Some are relatively simple like
Microsoft Excel Pivot tables, some much more complex from the field of Business Intelligence.

What I wanted for my own use was to analyse a single simple XLS file that changes
weekly. Plot few graphs, make a decision and be done with it until next week.

Now when you look at the existing BI tools to do that it is far from being a simple task.
Setting up some Web stack like LAMP, going through tens of pages of configs or web admin
tools to hook that single XLS file in. And maybe you'll be able to see your tiny chart
by the month end. And some of them want you to describe a full OLAP cube. For a single XLS.

What it is
==========
- A standalone application that you can run on any PC, Mac or, say, Raspberry Pi
- Requires minimum software: Python and few simple packages
- Creating a dashboard is as simple as editing 1 text file

What it is not and will never be
================================
- Nothing out of OLAP, ETL etc
- No multi-user
- No web administration
- No WYSIWYG dashboard generators.

Make it work
============
- Installation

```sh
easy_install jinja2
easy_install webapp2
easy_install WebOb
easy_install pyyaml
```
- Create a dashboard

```sh
vi dashboards/mydashboard.yaml
```
- Start 

```sh
python main.py
```
- See

```sh
Go to http://localhost:8080/renderYaml?dashboard=mydashboard
```
- Done

Acknowledgements
================
SimpleDash uses
- Highcharts for the graphs
- Jinja2 to build the dashboards
- Webapp2 to tie it up
- Paste to serve it