from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return JsonResponse({"status": "OK"}, status=200)
