# Get the latest 5 recipes and username form user collection

latest_recipes = [
        {
            u"$project": {
                u"_id": 0.0,
                u"recipes": u"$$ROOT",
                u"date_added": {
                    u"$dateToString": {
                        u"format": u"%Y-%m-%d",
                        u"date": u"$date_added"
                    }
                }
            }
        },
        {
            u"$lookup": {
                u"from": u"users",
                u"localField": u"recipes.user_id",
                u"foreignField": u"_id",
                u"as": u"users"
            }
        }, 
        {
            u"$unwind": {
                u"path": u"$users",
                u"preserveNullAndEmptyArrays": False
            }
        }, 
        {
            u"$addFields": {
                u"recipes.username": u"$users.username"
            }
        }, 
        {
            u"$project": {
                u"users": 0
            }
        },
        {
            u"$sort": {
                u"recipes.date_added": -1
            }
        },
        {
            u"$limit": 5
        }
    ]