from django.shortcuts import render
from comments.models import CommentModel
from comments.serializers import CommentSerializer
from posts.models import PostModel
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

# Create your views here.
class ListApi( APIView ):

    def get(self, request):
        info = {
            "list" : []
        }

        query = CommentModel.objects.strainer(request.GET).order_by("-comment_id")

        serializer = CommentSerializer(query, many=True)

        info["list"] = serializer.data

        # for item in info["list"]:
        #     user = User.objects.filter(id=item["user_id"]).first()
        #     print(user)
        #     if user:
        #         item.update({
        #             "user" : {
        #                 "first_name" : user.first_name,
        #                 "last_name" : user.last_name,
        #                 "email" : user.email,
        #             }
        #         })

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
        serializer = CommentSerializer( data=post, context={
            'request': request
        } )
        
        if serializer.is_valid(  ):
            info["obj"] = serializer.save()
            info["obj"] = serializer.data
        else:           
            info["error"] = serializer.errors
        
        return info

class EditApi( APIView ):

    def get(self, request, pk):
        info = {
            "obj" : None
        }

        query = PostModel.objects.get(pk=pk)

        serializer = CommentSerializer(query)

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