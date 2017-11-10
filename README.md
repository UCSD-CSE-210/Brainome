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


### Setting Up the Code

Server file structure being emulated
```
root/
    scmdb_py_newdata/
        data/
             Convert_tables.m  
             mm_hs_homologous_cluster.txt
             mmu/  # This is an ensemble folder
                 gene_id_to_names.csv
                 mch/
                      ... <LOTS and LOTS of files>
                 tsne_points_ordered.csv
                 gene_names.sqlite3
                 top_corr_genes.sqlite3
                 tsne_points_ordered.csv.bkup
             tSNE_merger.py
             orthologs.sqlite3
             <any other ensemble folders>
    /scmdb_py
        /data
             Convert_tables.m  
             mm_hs_homologous_cluster.txt  
             mmu/  # This is an ensemble folder
                  cluster_order.txt
                  mch/
                       ... <LOTS and LOTS of files>
                  tsne_points_ordered.csv
                  gene_id_to_names.csv  
                  top_corr_genes.sqlite3
                  gene_names.sqlite3
                  tsne_points.csv
             orthologs.sqlite3
             <any other ensemble folders>
```
#### Do one of the following
1. Download all of the data. First go to the directory that you would like the data to be in. 
```
mkdir scmdb_py_newdata
rsync -r <username>@brainome.ucsd.edu/srv/scmdb_py_newdata/data/* scmdb_py_newdata
mkdir scmdb_py
rsync -r <username>@brainome.ucsd.edu/srv/scmdb_py/data scmdb_py
```
2. Download subset of data. First go to the directory that you would like the data to be in.
```
mkdir scmdb_py_newdata
rsync <username>@brainome.ucsd.edu/srv/scmdb_py_newdata/data/* scmdb_py_newdata
cd scmdb_py_newdata
rsync -r <username>@brainome.ucsd.edu/srv/scmdb_py_newdata/data/human_MB_EB scmdb_py_newdata

# Go back out to the root directory
cd ../../..
mkdir scmdb_py
rsync <username>@brainome.ucsd.edu/srv/scmdb_py/data
rsync -r <username>@brainome.ucsd.edu/srv/scmdb_py_newdata/data/mmu scmdb_py
```

Using rsync command: rsync -r <username>@brainome.ucsd.edu/srv/scmdb_py_newdata/
Download code: In the directory you want code to be in, run the following commands:
 

### Setting Up the Code 

1. Clone the Repository in your local. 
```
git clone -v https://github.com/UCSD-CSE-210/Brainome.git
```
2. Setup the Virtual Environment by following the below steps.
```
pip install virtualenv
cd Brainome/prod
virtualenv venv
source venv/bin/activate
cd scmdb_py
pip install -r requirements.txt
deactivate

cd ../../dev
virtualenv venv
source venv/bin/activate
cd scmdb_py_dev
pip install -r requirements.txt
deactivate

cd ../../team
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
3. Linking code to downloaded data.  You will need to modify 2 files: "prod/scmdb_py/default_config.py", and "dev/scmdb_py_dev/default_config.py"  For now, this will just point to the published data (the 
```
DATA_DIR = 'Users/karanuppal/PycharmProjects/scmdb_py'
# DATA_DIR = 'path/to/scmdb_py'
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

