from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .serializers import NewsSerializer
from blog.models import News
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class API_LIST_PAGE(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class API_DETAIL_PAGE(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = "slug" #pass the command to use slug, pk is default for RetrieveUpdateDestroyView

# Create your views here.
@api_view(["GET", "POST"]) #function based
def api_list_page(request):
    if request.method == "GET":
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

class Api_list_page(APIView): #class based
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True) #many=true is used when serializing more than one view ie. "news.objects.all"
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 

@api_view(["GET", "PUT", "DELETE"])
def api_detail_page(request, slug):
    try:
        news = News.objects.get(slug=slug)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NewsSerializer(news) #many=true isnt needed here bcs it is getting only one view
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        news.delete()
        return Response(status=status.HTTP_200_OK)


class Api_detail_page(APIView):
    def get(self, request, slug):
        news = News.objects.get(slug=slug)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

@api_view(["POST"]) #function based
def api_create_page(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class  Api_create_page(APIView):
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def api_update_page(request, slug):
    try:
        news = News.objects.get(slug=slug)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = NewsSerializer(data=request.data, partial=True) #setting partial to true is to allow only one or more changes, not necessarily have to update all fields
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

