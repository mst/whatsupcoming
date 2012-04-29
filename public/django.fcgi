#!/usr/bin/python
import os, sys

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

_PROJECT_NAME = _PROJECT_DIR.split('/')[-1]
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % _PROJECT_NAME
whatsupcoming = __import__(os.environ['DJANGO_SETTINGS_MODULE'])

try:
  import whatsupcoming.env_settings
except:
  pass

# scm dependency management
import deps
deps.add_all_to_path(whatsupcoming.settings, False)

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
