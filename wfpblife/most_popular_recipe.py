from bson.son import SON


mpr = [
    {
        u"$match": {}
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