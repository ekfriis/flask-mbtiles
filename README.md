flask-mbtiles
=============

Ultra simple MBTiles server using Flask

Requirements
------------

This package depends on Flask and the Flask-Cache packages.

Quickstart
----------

You can use the built-in Flask http server to test things locally.  Set the
```MBTILES_PATH``` environment variable to your local .mbtiles file, and run

```shell
python flask-mbtiles.py
```

You can then browse tiles on
```http://localhost:41815/{zoom}/{column}/{row}.png```.


In Production
-------------

To run in production, create a wrapper script to configure the application.

```python
from mbtileserver.py import create_app

my_app = create_app(mbtiles='/path/to/my.mbtiles', 
                    cache_config={'CACHE_TYPE': 'simple'})

# whatever else your WSGI wrapper requires
```

The ```cache_config``` variable is a dictionary which is used to configure
Flask-Cache.
