import os

# USAGE: gunicorn Task_Management_App.wsgi --config gunicorn_config.py

workers = 1

threads = 1

timeout = 90

bind = '0.0.0.0:8000'

logconfig = "log.conf"

access_log_format = '%(r)s %(s)s %(M)s'

forwarded_allow_ips = '*'



