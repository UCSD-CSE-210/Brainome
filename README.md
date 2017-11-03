# Brainome

Prerequisites
---------------
1. Make sure you have python3 installed in your local.
2. You can make sure that python3 is running in your bash terminal by running the below command. I have Python 3.6.3.
```
python --version
```

Installation on MAC
--------------------
1. Clone the Repository in your local. 
```
git clone -v https://github.com/UCSD-CSE-210/Brainome.git
```

2. Setup the Virtual Environment by following the below steps.
```
pip install virtualenv
cd Brainome/
virtualenv venv
source venv/bin/activate
cd team
pip install -r requirements.txt
deactivate
```
3. Copy the data from the Brainome server to your local directory. (You need to copy scmdb_py and scmdb_py_newdata directories)
4. Make note of the Path of data directory in your local directory and update the default_config.py file pointing 
it to the location of the data directory. (For example)
```
DATA_DIR = '/Users/karanuppal/PycharmProjects/scmdb_py'
```
5. Activate the Virtual environment.
```
source venv/bin/activate
```
6. Make sure you have all the dependencies specified in requirements.txt in your virtual environment by running the below command.
```
pip freeze
```
7. Start the Application on port 5000.
```
flask --app=team serve --port 5000
```

