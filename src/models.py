
import datetime
from flask.ext.mongoengine import MongoEngine


db = MongoEngine()


class Location(db.Document):

    address = db.StringField()
    point = db.PointField()

    timestamp = db.DateTimeField(default=datetime.datetime.now())


# http://gis.stackexchange.com/a/101898
