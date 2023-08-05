import os
import sys
import yaml
from lib.Invoice import Invoice
from jinja2 import Template, Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = ROOT + '/template'
HTML_PATH = ROOT + '/html'
PARAMETER_PATH = sys.argv[1]

if not os.path.isfile(PARAMETER_PATH):
    print("Invalid argument.")
    exit(255)

if not os.path.isdir(HTML_PATH):
    os.mkdir(HTML_PATH)

with open(PARAMETER_PATH, 'r') as f:
    parameter = yaml.safe_load(f)

invoice=Invoice(
    parameter['tax_rate'], parameter['withhold_rate'],
    parameter['render_from'], parameter['include_withhold']
)

invoice.setTo(
    parameter['to']['name'],
    parameter['to']['address'],
    parameter['to']['tel'],
    parameter['to']['fax'],
    parameter['to']['email']
)

invoice.setFrom(
    parameter['from']['name'],
    parameter['from']['address'],
    parameter['from']['tel'],
    parameter['from']['fax'],
    parameter['from']['email']
)

invoice.setBank(
    parameter['bank']['name'],
    parameter['bank']['type'],
    parameter['bank']['number'],
    parameter['bank']['holder']
)

for detail in parameter['details']:
    invoice.addDetail(
        detail['descr'],
        detail['unit_price'],
        detail['amount'],
        detail['isFixTaxIncluded']
    )

env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
template = env.get_template("invoice.html.j2")
html = template.render(invoice.getInvoiceParameter())
with open(HTML_PATH + "/invoice.html", 'w') as f:
    f.write(html)