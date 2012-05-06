#!/usr/bin/env python
try:
  import whatsupcoming.env_settings
except:
  pass

import os
import sys
import whatsupcoming

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsupcoming.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
