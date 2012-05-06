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

When working on the project, it is advisable to always switch to the virtual
environment with

```
source venv/bin/activate
```
