from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from posts.models import BaseModelJSONEncoder, PostModel
from rest_framework.response import Response
from django.forms.models import model_to_dict
from posts.serializers import FileSerializer, PostSerializer
from rest_framework.views import APIView
import json
from itertools import chain

from django.core import serializers

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
        serializer = PostSerializer( data=post, request=request )
        
        if serializer.is_valid(  ):
            info["obj"] = serializer.save()
            slides = serializer.save_slides()
            info["obj"] = serializer.data
            file_Serializer = FileSerializer(slides, many=True)
            info["slides"] = file_Serializer.data

            # slides = post.getlist('slides')

            # if len(slides):
            #     for slide in slides:
            #         query = {
            #             "type" : "posts",
            #             "type_id" : info["obj"]["post_id"],
            #             "path" : slide,
            #         }
            #         file_serializer = FileSerializer(data=query)

            #         if file_serializer.is_valid():
            #             file_serializer.save()
            #             info["slides"].append( file_serializer.data )
        else:           
            info["error"] = serializer.errors
        
        return info

class EditApi( APIView ):

    def get(self, request, pk):

        info = {
            "obj" : None
        }

        query = PostModel.objects.get(pk=pk)
        # return HttpResponse(json.dumps(PostModel.objects.all(), cls=BaseModelJSONEncoder))

        print(model_to_dict(query))
        # breakpoint()
        # p = json.dumps(query, cls=BaseModelJSONEncoder)


        serializer = PostSerializer(query)

        info["obj"] = serializer.data

        info["obj"]["slides"] = FileSerializer(query.slides(), many=True).data

        d = serializers.serialize("jsonl", PostModel.objects.all())
        # return HttpResponse(d)
        # return Response(model_to_dict(query))

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