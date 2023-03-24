from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rater.models import Instance, Professor, Module, Rating
import json
from django.core import serializers
import ast

# Create your views here.
def ConnectionTest (request):
    return HttpResponse (1)

@csrf_exempt
def HandleRegisterRequest (request):
    loginObj = json.loads(request.body)
    username = loginObj["username"]
    email = loginObj["email"]
    password = loginObj["password"]
    try:
        User.objects.create_user(username, email, password)
        return HttpResponse (1)
    except:
        return HttpResponse (0)

@csrf_exempt
def HandleLoginRequest (request):
    loginObj = json.loads(request.body)
    username = loginObj["username"]
    password = loginObj["password"]
    user = authenticate(request, username = username, password = password)
    if user is not None:
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def HandleListRequest (request):
    instances = Instance.objects.order_by("module", "year", "semester")
    instList = []
    for instance in instances:
        instList.append([instance.module.code, instance.module.name, instance.year, instance.semester, instance.professor.code, instance.professor.name])

    toPop = 0
    for i in range(0, len(instList) - 1):
        if instList[i][0] == instList[i+1][0] and instList[i][2] == instList[i+1][2] and instList[i][3] == instList[i+1][3] and instList[i][4] != instList[i+1][4]:
            instList[i][4] = [instList[i][4], instList[i+1][4]]
            instList[i][5] = [instList[i][5], instList[i+1][5]]
            for j in range(i + 1, len(instList) - 1):
                instList[j] = instList[j + 1]
            i -= 1
            toPop += 1

    for i in range (0, toPop):
        instList.pop()
    return HttpResponse(json.dumps(instList), content_type="application/json")


def HandleViewRequest (request):
    ratings = Rating.objects.order_by("instance")
    profSet = set()
    for rating in ratings:
        profSet.add(rating.instance.professor.code + "|" + rating.instance.professor.name)

    profList = []
    for professor in profSet:
        profList.append(professor.split("|"))
    for i in range(0, len(profList)):
        noOfRatings = 0.0
        total = 0.0
        for rating in ratings:
            if rating.instance.professor.code == profList[i][0]:
                total += float(rating.rating)
                noOfRatings += 1.0
        rating = int(total/noOfRatings + 0.5)
        profList[i].append(rating)
    return HttpResponse(json.dumps(profList), content_type="application/json")

def HandleAvgRequest (request):
    temp = json.loads(request.body)
    params = ast.literal_eval(temp)
    ratings = Rating.objects.filter(instance__professor__code = params["professor"], instance__module__code = params["module"])

    try:
        data = [ratings[0].instance.professor.code, ratings[0].instance.professor.name, ratings[0].instance.module.code, ratings[0].instance.module.name]
    except:
        return HttpResponse(0)
    noOfRatings = 0.0
    total = 0.0
    for rating in ratings:
        total += rating.rating
        noOfRatings += 1.0
    rating = int(total/noOfRatings + 0.5)
    data.append(rating)
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def HandleRateRequest (request):
    params = json.loads(request.body)

    if int(params["rating"]) < 1 or int(params["rating"]) > 5:
        return HttpResponse(-1)
    elif int(params["semester"]) != 1 and int(params["semester"]) != 2:
        return HttpResponse(-2)

    try:
        instance = Instance.objects.get(professor__code = params["professor"],
        module__code = params["module"],
        year = params["year"],
        semester = params["semester"]
        )
    except:
        return HttpResponse(-3)
    user = User.objects.get(username = params["user"])

    if Rating.objects.filter(user__username = params["user"],
        instance__professor__code = params["professor"],
        instance__module__code = params["module"],
        instance__year = params["year"], instance__semester = params["semester"]
    ).exists():
        return HttpResponse(-4)
    else:
        rating = Rating(rating = params["rating"], instance = instance, user = user)
        rating.save()
        return HttpResponse(1)
