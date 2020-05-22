from bson.son import SON
# Get the username for the recipes from the users collection, and order the recipes alphabetically

user_lookup = [
    {
        u"$match": {}
    }, 
    {
        u"$lookup": {
            u"from": u"users",
            u"let": {
                u"id": u"$user_id"
            },
            u"pipeline": [
                {
                    u"$match": {
                        u"$expr": {
                            u"$eq": [
                                u"$_id",
                                u"$$id"
                            ]
                        }
                    }
                }
            ],
            u"as": u"user"
        }
    }, 
    {
        u"$unwind": {
            u"path": u"$user",
            u"preserveNullAndEmptyArrays": False
        }
    }, 
    {
        u"$addFields": {
            u"username": u"$user.username"
        }
    }, 
    {
        u"$project": {
            u"user": 0.0
        }
    }, 
    {
        u"$sort": SON([ (u"title", 1) ])
    }, 
    {
        u"$limit": 10.0
    }
]