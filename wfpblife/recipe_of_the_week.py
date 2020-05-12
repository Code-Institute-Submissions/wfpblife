# Requires pymongo 3.6.0+
from bson.son import SON
from bson.tz_util import FixedOffset
from datetime import datetime

rotw = [
    {
        u"$match": {
            u"date_added": {
                u"$gt": datetime.strptime("2019-01-01 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo = FixedOffset(0, "+0000"))
            }
        }
    }, 
    {
        u"$addFields": {
            u"ratings_total": {
                u"$sum": u"$ratings.value"
            }
        }
    }, 
    {
        u"$sort": SON([ (u"ratings_total", -1) ])
    }, 
    {
        u"$limit": 1.0
    }
]