#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *

import folium
import numpy as np
import json
import tempfile
import requests

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
#@app.teardown_request
#def shutdown_session(exception=None):
#    db_session.remove()

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

def postcode_search(postcode):
    key = app.config['THEYWORKFORYOUAPI']
    con_url='http://www.theyworkforyou.com/api/getConstituency?postcode={}&key={}'.format(postcode,key)
    mp_url='http://www.theyworkforyou.com/api/getMP?postcode={}&key={}'.format(postcode,key)
    r_con = requests.get(con_url)
    r_mp = requests.get(mp_url)
    con = r_con.json()['name']
    mp = r_mp.json()['full_name']
    return con, mp


def build_map(con):
    json_data=open('./boundaries/{}.json'.format(con))
    data = json.load(json_data)
    lat = np.zeros(1)
    lon = np.zeros(1)
    if len(data['geometry']['coordinates']) > 1:
        loop_data = data['geometry']['coordinates'][0][0]
    else:
        loop_data = data['geometry']['coordinates'][0]
    for i in loop_data:
        lon = lon+i[0]
        lat = lat+i[1]
    lat /= len(loop_data)
    lon /= len(loop_data)
    lat = lat[0]
    lon = lon[0]

    map = folium.Map(location=[lat,lon],zoom_start=10, width='100%')
    map.geo_json(geo_path='/boundaries/{}.json'.format(con))
    # map.create_map(path="tmp/test_ori.html")
    # map.env = app.jinja_env
    # map.create_map(path="tmp/test_flask.html")
    return map


@app.route('/', methods=['POST', 'GET'])
def home():
    form = PostCodeForm()
    if request.method == 'POST':
        if form.postcode.data:
            con, mp = postcode_search(form.postcode.data)
            con_dict = {'con':con,
                        'mp':mp}
            map = build_map(con)
            return render_template('pages/geojson_map.html', form=form, con=con_dict, **map.template_vars)
    return render_template('pages/home.html', form=form)


@app.route('/<path:path>')
def boundary_json(path):
    return send_from_directory('/boundaries/', path)


@app.route('/about')
def about():
    return render_template('pages/about.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
