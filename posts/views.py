from django.http import JsonResponse
from django.shortcuts import render
from posts.models import PostModel
from posts.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ListApi( APIView ):

    def get(self, request):
        info = {
            "list" : []
        }

        query = PostModel.objects.order_by("-post_id").all()

        serializer = PostSerializer(query, many=True)

        info["list"] = serializer.data

        return Response(info)

class CreateApi( APIView ):

    def post(self, request):
        info = self.process(request)
        return Response(info)

    def process( self, request ):
        info = {
            "obj" : None
        }

        post = request.data
        
        serializer = PostSerializer( data=post )
        # print(serializer.is_valid(  ))
        # print(serializer.errors)
        if serializer.is_valid(  ):
            info["obj"] = serializer.save()
            info["obj"] = serializer.data
        else:
            info["error"] = serializer.errors()
        
        return info

class EditApi( APIView ):

    def get(self, request, pk):
        info = {
            "obj" : None
        }

        query = PostModel.objects.get(pk=pk)

        serializer = PostSerializer(query)

        info["obj"] = serializer.data

        return Response(info)

class DeleteApi( APIView ):

    def post(self, request, pk):
        info = {
            "success" : False,
            "msg" : "Something went wrong",
        }

        obj = PostModel.objects.filter(pk=pk).first()

        if obj:
            obj.delete()
            
            info.update({
                "success" : True,
                "msg" : "Successful",
            })

        return Response(info)