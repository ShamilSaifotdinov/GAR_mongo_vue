from django.shortcuts import render

from django.http import HttpResponse

from utils import get_database
import json

db = get_database()
region = db["addr"]

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def query(request, objectId):
    elem = list(region.find({"adm_parentId": objectId}))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')

def query_level(request, objectId, hierarchy, levelId):
    if objectId == 0:
        elem = list(region.find({"versions.level": levelId}, {'_id': False }))
        print(elem)
    else:
        elem = list(region.find(
            {
                '$and': [
                    { hierarchy + "_parentId": objectId, },
                    {
                        '$or': [
                            { 'versions': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '1', 'level': levelId } } },
                            {
                                '$and': [
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '1' } } } },
                                    { 'versions': { '$elemMatch': { 'ISACTUAL': '0', 'ISACTIVE': '1', 'level': levelId } } }
                                ]
                            },
                            {
                                '$and': [
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '1' } } } },
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '0', 'ISACTIVE': '1' } } } },
                                    { 'versions': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '0', 'level': levelId } } }
                                ]
                            },
                            {
                                '$and': [
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '1' } } } },
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '0', 'ISACTIVE': '1' } } } },
                                    { 'versions': { '$not': { '$elemMatch': { 'ISACTUAL': '1', 'ISACTIVE': '0' } } } },
                                    { 'versions': { '$elemMatch': { 'ISACTUAL': '0', 'ISACTIVE': '0', 'level': levelId } } }
                                ]
                            }
                        ]
                    }
                ]
            }
            , {'_id': False }))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')


def levels(request, objectId, hierarchy):
    elem = list(region.aggregate([
        {
            '$match': {
                hierarchy + '_parentId': objectId
            },
        },
        {
            '$group': {
                '_id': {
                    '$getField': {
                        'input': {
                            '$first': {
                                '$filter' : {
                                    'input': "$versions",
                                    'as': "version",
                                    'cond': { '$and': [ { '$eq': ["$$version.ISACTUAL", "1"]}, { '$eq': ["$$version.ISACTIVE", "1"]} ] }
                                },
                            }
                        },
                        'field': "level"
                    }
                },
                'count': {
                    '$sum': 1
                }
            }
        },
        {
            '$lookup': {
                'from': 'levels',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'level'
            }
        },
        {
            '$set': {
                'levelName': {
                    '$arrayElemAt': [
                        '$level.name', 0
                    ]
                }
            }
        },
        {
            '$sort': {
                '_id': 1
            }
        }
    ]))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')
