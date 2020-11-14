from django.shortcuts import render
from django.http import JsonResponse
import random

counter = 0


def colors(request):
    global counter
    r = lambda: random.randint(0, 255)
    font_color = '#%02X%02X%02X' % (r(), r(), r())
    background_color = '#%02X%02X%02X' % (r(), r(), r())
    context = {'id': counter, 'font_color': font_color, 'background_color': background_color}
    counter += 1
    return JsonResponse(context)
