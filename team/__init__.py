import os
from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_nav import Nav
from flask_assets import Environment
from flask_compress import Compress
from flask.ext.htmlmin import HTMLMIN
from flask.json import JSONEncoder
from .assets import app_css, app_js, vendor_css, vendor_js

cache = Cache()
nav = Nav()
compress = Compress()
htmlmin = HTMLMIN()
basedir = os.path.abspath(os.path.dirname(__file__))

class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'

def create_app(configfile=None):
    app = Flask(__name__)
    app.secret_key = 's3cr3t'
    AppConfig(app)
    Bootstrap(app)
    # EAM : Set limit on the number of items in cache (RAM)
    cache.init_app(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 1000})

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    with app.app_context():
        from .frontend import frontend
        app.register_blueprint(frontend)

    app.json_encoder = MiniJSONEncoder

    nav.init_app(app)

    compress.init_app(app)
    htmlmin.init_app(app)

    return app

if __name__ == '__main__':
  #app.run(debug=True)
  create_app().start(debug=True)

