# 14-Dic-2021
# Install script
# Set the FLASK_ENV in the properly mode (development if you need to debug)

# 0. install python!!
# 1. download flask using pip
# python -m pip install flask
# cd WORKING_DIR
cp dwdata.py app.py
export FLASK_APP=app.py
export FLASK_ENV=development
flask run