INSTALL
=======


In the projects root folder, execute:

``` bash
# create a virtual environment for the python dependencies:
virtualenv venv --distribute

# switch to the virtual environment
source venv/bin/activate

# let pip install the requirements
pip install -r requirements.txt

# collect statics
./manage.py collectstatics
```

Before working on the project, switch to the virtual environment with

``` bash
source venv/bin/activate
```

[More information on virtualenv](http://pypi.python.org/pypi/virtualenv)


IPython and MacOS
===
To get around the readline issues with IPython and MacOS, install readline in your virtual env with
``` bash
easy_install -a readline
```

