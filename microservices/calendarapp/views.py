from django.shortcuts import render
from datetime import datetime, date
from django.http import JsonResponse


counter = 0


def time_view(request):
    global counter
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    context = {'id': counter, 'time': current_time}
    counter += 1
    return JsonResponse(context)


def date_view(request):
    global counter
    today = date.today()
    context = {'id': counter, 'date': today}
    counter += 1
    return JsonResponse(context)
