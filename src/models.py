
import datetime
from flask.ext.mongoengine import MongoEngine


db = MongoEngine()


class Location(db.Document):

    address = db.StringField()
    point = db.PointField()

    properties = db.DictField()

    timestamp = db.DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return '<Location address=%r, point=%r>' % (
            self.address, self.point)

    def __unicode__(self):
        return repr(self)


# http://gis.stackexchange.com/a/101898
