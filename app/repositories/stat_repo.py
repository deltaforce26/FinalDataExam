import math
from app.db.mongo_db import initialize_mongo
from app.settings.config import DB_URL

attacks_col = initialize_mongo(DB_URL, "terror_attacks_db", "attacks")
countries_col = initialize_mongo(DB_URL, "terror_attacks_db", "countries")


def find_most_fatal_attacks(limit=5):
    pipeline = [
        {
            '$group': {
                '_id': '$attack_type',
                'total_fatality_score': {'$sum': '$fatality_score'}
            }
        },
        {
            '$sort': {'total_fatality_score': -1}
        },
        {
            '$limit': limit
        }
    ]
    top_attack_types = attacks_col.aggregate(pipeline)
    return list(top_attack_types)


def calc_avg_casualties(limit=5):
    pipeline = [
        {
            '$group': {
                '_id': '$country',
                'avg_fatality_score': {'$avg': '$fatality_score'},
                'attack_locations': {
                    '$push': {
                        '$cond': [
                            {'$and': [{'$ne': ['$latitude', None]}, {'$ne': ['$longitude', None]}]},
                            {'latitude': '$latitude', 'longitude': '$longitude'},
                            None
                        ]
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 1,
                'avg_fatality_score': 1,
                'attack_locations': {
                    '$filter': {
                        'input': '$attack_locations',
                        'as': 'loc',
                        'cond': {'$ne': ['$$loc', None]}
                    }
                }
            }
        },
        {
            '$sort': {'avg_fatality_score': -1}
        },
        {
            '$limit': limit
        }
    ]
    country_avg_fatality = list(attacks_col.aggregate(pipeline))
    results = []
    for doc in country_avg_fatality:
        results.append({
            'country': doc['_id'],
            'avg_fatality_score': doc['avg_fatality_score'],
            'attack_locations': [
                (loc['longitude'], loc['latitude'])
                for loc in doc['attack_locations'] if not (math.isnan(loc['latitude']) or math.isnan(loc['longitude']))
            ]
        })
    return results


def find_most_violent_groups(limit=5):
    pipeline = [
        {
            '$group': {
                '_id': '$terror_group',
                'fatality_score': {'$sum': '$fatality_score'},
            }
        },
        {
            '$sort': {'fatality_score': -1}
        },
        {
            '$limit': limit
        }
    ]
    most_violent_groups = attacks_col.aggregate(pipeline)
    return list(most_violent_groups)


def find_top_groups_per_country(country=None, limit=5):
    pipeline = []
    if country:
        pipeline.append(
            {
                '$match': {
                    'country': country
                }
            }
        )
    pipeline.append(
        {
            '$group': {
                '_id': {'country': '$country', 'terror_group': '$terror_group'},
                'count': {'$sum': 1}
            }
        })
    pipeline.append(
        {
            '$group': {
                '_id': '$_id.country',
                'top_groups': {
                    '$push': {
                        'group': '$_id.terror_group',
                        'count': '$count'
                    }
                }
            }
        })
    pipeline.append(
        {
            '$addFields': {
                'top_groups': {
                    '$sortArray': {
                        'input': '$top_groups',
                        'sortBy': {'count': -1}
                    }
                }
            }
        }
    )
    pipeline.append(
        {
            '$project': {
                'top_groups': {'$slice': ['$top_groups', limit]}
            }
        })
    pipeline.append(
        {
            '$sort': {'_id': 1}
        })

    top_groups = list(attacks_col.aggregate(pipeline))
    for group in top_groups:
        res = countries_col.find_one(
                            {"Country": group['_id']},
                            {"location": 1, "_id": 0}
                        )
        group['location'] = res['location']
    return top_groups


def find_common_targets():
    pipeline = [
        {
            "$match": {
                "terror_group": {"$ne": None},
                "target1": {"$ne": None}
            }
        },
        {
            "$group": {
                "_id": {"group_name": "$terror_group", "target_type": "$target1"},
                "attack_count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "attack_count": {"$gte": 3}
            }
        },
        {
            "$sort": {"attack_count": -1}
        },
        {
            "$project": {
                "_id": 0,
                "group_name": "$_id.group_name",
                "target_type": "$_id.target_type",
                "attack_count": 1
            }
        }
    ]
    result = list(attacks_col.aggregate(pipeline))
    print(len(result))
    return result


if __name__ == '__main__':
    results = find_common_targets()

