'''
SOAP Server
Made by Let's Shop! 2023
'''
from flask import Flask
import ecs, ias, cas, cdn

app = Flask(__name__)
app.register_blueprint(ecs.ecs)
app.register_blueprint(ias.ias)
app.register_blueprint(cas.cas)
app.register_blueprint(cdn.ccs)