from posts.models import FileModel, PostModel
from rest_framework import serializers
from drf_blog_api.utils import upload

class PostSerializer( serializers.Serializer ):
    post_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)
    content = serializers.CharField( required=False )
    featured_image = serializers.FileField( max_length=None, allow_empty_file=True )
    created_at = serializers.DateTimeField( required=False )
    updated_at = serializers.DateTimeField( required=False )

    instance = None
    slide_instances = None
    request = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') if kwargs.get('request') else None
        super(PostSerializer, self).__init__(*args, **kwargs)

    @property
    def data(self):
        data = super(PostSerializer, self).data
        
        if self.instance:
            data.update({
                "post_id" : self.instance.pk,
                "featured_image" : self.instance.featured_image,
                "created_at" : self.instance.created_at,
                "updated_at" : self.instance.updated_at,
            }) 

        return data

    def save( self ):
        validated_data = self.validated_data

        query = {
            "name" : validated_data["name"],
            "content" : validated_data.get("content", "no content present"),
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

    