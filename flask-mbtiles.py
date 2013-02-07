import sqlite3
from flask import Flask, g, send_file, abort, Blueprint, current_app
from flask.ext.cache import Cache

try:
    raise ImportError
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO  # NOQA


frontend = Blueprint('frontend', __name__)
cache = Cache()


@frontend.before_request
def before_request():
    """Ensure database is connected for each request """
    g.db = sqlite3.connect(current_app.config['MBTILES_PATH'])


@frontend.teardown_request
def teardown_request(exception):
    """Cleanup database afterwards """
    if hasattr(g, 'db'):
        g.db.close()


@frontend.route("/<int:zoom>/<int:column>/<int:row>.png")
@cache.cached(timeout=300)
def query_tile(zoom, column, row):
    """Get a tile from the MBTiles database """
    query = 'SELECT tile_data FROM tiles '\
            'WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?;'
    cur = g.db.execute(query, (zoom, column, row))
    results = cur.fetchall()
    if not results:
        abort(404)
    the_image = results[0][0]
    print 'doot', current_app.config['TESTING']
    return send_file(StringIO(the_image), mimetype='image/png')


def create_app(mbtiles=None, cache_config=None):
    """Initialize the application with a given configuration.

    mbtiles must be a path to the MBTiles sqlite file.

    """
    app = Flask(__name__)
    app.config.update({
        'MBTILES_PATH': mbtiles
    })
    app.register_blueprint(frontend)
    print cache_config
    cache.init_app(app, config=cache_config)
    return app


if __name__ == "__main__":
    app = create_app(
        mbtiles='/Users/friis/Documents/Traffik.mbtiles',
        cache_config={
            'CACHE_TYPE': 'simple',
        }
    )
    app.run(debug=True, port=41815)
