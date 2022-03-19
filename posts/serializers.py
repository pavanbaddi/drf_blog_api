from posts.models import PostModel
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