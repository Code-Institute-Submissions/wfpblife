recipe_comments = [
    {
        u"$unwind": {
            u"path": u"$comments",
            u"preserveNullAndEmptyArrays": False
        }
    }, 
    {
        u"$lookup": {
            u"from": u"users",
            u"localField": u"comments.user_id",
            u"foreignField": u"_id",
            u"as": u"comment_by"
        }
    }, 
    {
        u"$unwind": {
            u"path": u"$comment_by",
            u"preserveNullAndEmptyArrays": False
        }
    }, 
    {
        u"$addFields": {
            u"comments.comment_by": u"$comment_by.username"
        }
    }, 
    {
        u"$project": {
            u"comment_by": 0.0,
        }
    }, 
    {
        u"$project": {
            u"comments": 1.0
        }
    }
]