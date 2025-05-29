from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_data(request):
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return Response(data)