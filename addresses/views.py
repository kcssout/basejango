from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser

json_dumps_params = {'ensure_ascii': False}


@csrf_exempt
def address_list(request):
    if request.method == 'GET':  # select
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False)

    elif request.method == 'POST':  # create
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def address(request, pk):
    obj = Addresses.objects.get(pk=pk)  # filter > sql where

    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        print(serializer.data)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, status=201)
        return JsonResponse(serializer.erros, status=400)

    elif request.method == 'DELETE':  # 숫자뒤에 슬래쉬를 붙여줘야한다
        obj.delete()
        return HttpResponse(status=204)


def addressName(request, name):
    obj = Addresses.objects.get(name=name)

    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False}, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        print('askdfjsadf')
        # name = request.POST.get('name', '')
        # ph = request.POST.get('phone_number', '')
        data = JSONParser().parse(request)

        name = data['name']
        ph = data['phone_number']
        print(name + ' ' + ph)
        obj = Addresses.objects.get(name=name)

        if ph == obj.phone_number:  # pw
            print("success > " + obj.phone_number)
            return JsonResponse({'code': '0000', 'msg': '로그인 성공 입니다.'}, status=200)
        else:
            return JsonResponse({'code': 'error', 'msg': '로그인 실패 입니다.'}, status=400)
