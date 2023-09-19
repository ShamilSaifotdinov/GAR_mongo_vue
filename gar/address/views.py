from django.shortcuts import render

from django.http import HttpResponse

from utils import get_database
import json

db = get_database()
region = db["87"]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def query(request, objectId):
    elem = list(region.find({"adm_parentId": objectId}))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')

def query_level(request, objectId, hierarchy, levelId):
    elem = list(region.find({hierarchy + "_parentId": objectId, "level": levelId}))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')


def levels(request, objectId, hierarchy):
    elem = list(region.aggregate([
        {
            '$match': {
                hierarchy + '_parentId': objectId
            }
        }, {
            '$group': {
                '_id': '$level',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$lookup': {
                'from': 'levels',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'level'
            }
        }, {
            '$set': {
                'levelName': {
                    '$arrayElemAt': [
                        '$level.name', 0
                    ]
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]))
    # print(elem)
    # print(json.dumps(elem))
    return HttpResponse(json.dumps(elem), content_type='application/json')
# Create your views here.
