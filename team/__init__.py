from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_nav import Nav
from flask_compress import Compress
from flask.ext.htmlmin import HTMLMIN
from flask.json import JSONEncoder

cache = Cache()
nav = Nav()
compress = Compress()
htmlmin = HTMLMIN()

class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    # EAM : Set limit on the number of items in cache (RAM)
    cache.init_app(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 1000})

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

