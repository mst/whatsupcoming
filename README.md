INSTALL
=======


In the projects root folder, execute:

``` bash
# create a virtual environment for the python dependencies:
virtualenv venv --distribute

# let pip install the requirements
pip install -r requirements.txt

# collect statics
./manage.py collectstatics
```
