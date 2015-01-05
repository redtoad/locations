import functools
import json

from flask import Flask, render_template, Response, request, redirect, flash
from flask.ext.mongoengine import MongoEngine
from utils import address_lookup

app = Flask(__name__)   # create our flask app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {
    'HOST': '127.0.0.1',
    'DB': 'Locations'
}

#this prints shit to terminal
app.logger.debug("Connecting to mongodb")
db = MongoEngine(app)  # connect MongoEngine with Flask App

print db.connection

# import data models
import models

# FloatConverter does not handle negative numbers. This converter also treats
# integers as floats, which also would have failed.
# http://stackoverflow.com/a/20640550/294082
from werkzeug.routing import FloatConverter
class CoordinateConverter(FloatConverter):
    regex = r'-?\d+(\.\d+)?'

app.url_map.converters['coord'] = CoordinateConverter


def jsonify(fnc):
    @functools.wraps(fnc)
    def decorated_function(*args, **kwargs):
        resp = json.dumps(fnc(*args, **kwargs))
        return Response(resp, content_type='application/json')
    return decorated_function


def is_ajax():
    print request.headers
    return 'XMLHttpRequest' in request.headers.get('X_REQUESTED_WITH', '')


@app.route('/')
def index():
    return render_template('overview-map.html')


@app.route('/location', methods=['GET', 'POST'])
def add_location():

    if request.method == 'POST':

        address = request.form.get('address')
        coordinates = address_lookup(address)

        if address and coordinates:
            loc = models.Location()
            loc.address = address
            loc.point = coordinates
            loc.save()

        else:
            flash('Thanks for registering', 'error')
            return render_template('add_location.html')

        add_another = 'add_another' in request.form

        if add_another:
            return redirect('/location')
        if not is_ajax():
            return redirect('/')

    return render_template('add_location.html')


@app.route('/locations/<coord:lonSW>,<coord:latSW>,<coord:lonNE>,<coord:latNE>')
@jsonify
def get_locations(lonSW, latSW, lonNE, latNE):
    box = [(lonSW, latSW), (lonNE, latNE)]
    locations = models.Location.objects(point__geo_within_box=box)

    for loc in models.Location.objects():
        print loc

    def to_geojson(loc):
        properties = loc.properties
        properties.update({
            "name": loc.properties.get('name', loc.address),
            "address": loc.address,
            "date_creation": str(loc.timestamp)
        })
        return {
            "type": "Feature",
            "geometry": loc.point,
            "properties": properties
        }

    return map(to_geojson, locations)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')