from posts.models import FileModel, PostModel
from posts.serializer_fields import PostMetaSerializerField
from rest_framework import serializers
from drf_blog_api.utils import upload
from comments.serializers import UserSerializer
from django.contrib.auth.models import User

class PostSerializer( serializers.Serializer ):
    post_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)
    content = serializers.CharField( required=False )
    # meta_data = serializers.JSONField( source="get_meta_data" )
    meta_data = PostMetaSerializerField(  )
    featured_image = serializers.FileField(required=False, max_length=None, allow_empty_file=True )
    created_at = serializers.DateTimeField( required=False )
    updated_at = serializers.DateTimeField( required=False )
    # meta_data_formatted = serializers.SerializerMethodField(write_only=False, read_only=False)

    instance = None
    slide_instances = None
    request = None

    # def get_meta_data(self, obj):
    #     print("meta_data")

    def to_representation(self, instance):
        ret = super(PostSerializer, self).to_representation(instance)
        
        # user_id  = ret.get("meta_data").get("user_id") if ret.get("meta_data") else None
        # if user_id:
        #     user = User.objects.filter(id=user_id).first()
        #     ret["meta_data"]["user"] = UserSerializer(user).data if user else None

        return ret

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') if kwargs.get('request') else None
        super(PostSerializer, self).__init__(*args, **kwargs)

    @property
    def data(self):
        # print("data called")
        data = super(PostSerializer, self).data
        
        if self.instance:
            data.update({
                "post_id" : self.instance.pk,
                "featured_image" : self.instance.featured_image,
                "created_at" : self.instance.created_at,
                "updated_at" : self.instance.updated_at,
            }) 

        # user = User.objects.filter(id=data.get("meta_data").get("user_id")).first()
        
        # if user:
        #     data["meta_data"].update({
        #         "user" : UserSerializer(user).data
        #     }) 

        return data

    def save( self ):
        validated_data = self.validated_data
        # print(validated_data["meta_data"], type(validated_data["meta_data"]))
        # breakpoint()
        query = {
            "name" : validated_data["name"],
            "content" : validated_data.get("content", "no content present"),
            "meta_data" : validated_data.get("meta_data"),
        }

        if validated_data.get('featured_image'):
            result = upload( file=validated_data.get('featured_image') )

            if result["success"]:
                query["featured_image"] = result["path"]
                
        if validated_data.get('post_id') is None:
            self.instance = PostModel.objects.create( **query )
        else:
            self.instance = PostModel.objects.get(pk=validated_data.get('post_id'))
            self.instance.fill(**query)
            self.instance.save()

        return self.instance

    def save_slides( self ):
        slides = self.request.data.getlist('slides') if self.request else []

        if len(slides):
            self.slide_instances = []
            for slide in slides:
                query = {
                    "type" : "posts",
                    "type_id" : self.instance.post_id,
                    "path" : slide,
                }
                file_serializer = FileSerializer(data=query)

                if file_serializer.is_valid():
                    slide_object = file_serializer.save()
                    self.slide_instances.append( slide_object )

        return self.slide_instances

    # def get_meta_data_formatted(self, obj):
    #     user = User.objects.filter(id=obj.meta_data.get("user_id") if obj.meta_data else None).first()
    #     return UserSerializer(user).data if user else None
class FileSerializer( serializers.Serializer ):
    file_id = serializers.IntegerField(required=False)
    type = serializers.CharField(max_length=255)
    type_id = serializers.IntegerField()
    path = serializers.FileField( max_length=None, allow_empty_file=True )
    created_at = serializers.DateTimeField( required=False )
    updated_at = serializers.DateTimeField( required=False )

    instance = None

    @property
    def data(self):
        data = super(FileSerializer, self).data
        
        if self.instance:
            data.update({
                "file_id" : self.instance.pk,
                "type" : self.instance.type,
                "type_id" : self.instance.type_id,
                "path" : self.instance.path,
                "created_at" : self.instance.created_at,
                "updated_at" : self.instance.updated_at,
            }) 

        return data

    def save( self ):
        validated_data = self.validated_data

        query = {
            "type" : validated_data["type"],
            "type_id" : validated_data["type_id"],
        }
        
        if validated_data.get('path'):
            result = upload( file=validated_data.get('path') )
            if result["success"]:
                query["path"] = result["path"]
                
        if validated_data.get('file_id') is None:
            self.instance = FileModel.objects.create( **query )
        else:
            self.instance = FileModel.objects.get(pk=validated_data.get('file_id'))
            self.instance.fill(**query)
            self.instance.save()

        return self.instance

    