# 14-Dic-2021
# Install script
# Set the FLASK_ENV in the properly mode (development if you need to debug)

python -m pip install flask
cp dwdata.py app.py
export FLASK_APP=app.py
export FLASK_ENV=development
flask run