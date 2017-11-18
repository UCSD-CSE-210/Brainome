# App-specific configuration

# Serve the Bootstrap template locally
# Set to False due to SCCF's subfolder reverse proxy shenanigans, 
# which will cause HTML paths to fail
BOOTSTRAP_SERVE_LOCAL = False

# Disable pretty-printing to conserve network transfer
JSONIFY_PRETTYPRINT_REGULAR = False

# Minify HTML to conserve network transfer
MINIFY_PAGE = True  

# TODO: Consider changing to point to new_data
DATA_DIR = '/srv/scmdb_py/data'
PUBLISHED_DATA_DIR = '/srv/scmdb_py/data'
ALL_DATA_DIR = '/srv/scmdb_py_newdata/data'

PUBLISHED_DIRECTORIES = ["mouse_published", "human_hv1_published"]
