from posts.models import PostModel
from rest_framework import serializers

class PostSerializer( serializers.Serializer ):
    post_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)
    content = serializers.CharField( required=False )
    created_at = serializers.DateTimeField( required=False )
    updated_at = serializers.DateTimeField( required=False )

    instance = None

    @property
    def data(self):
        data = super(PostSerializer, self).data
        
        if self.instance:
            data.update({
                "post_id" : self.instance.pk,
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

        if validated_data.get('post_id') is None:
            self.instance = PostModel.objects.create( **query )
        else:
            self.instance = PostModel.objects.get(pk=validated_data.get('post_id'))
            self.instance.name = query["name"]
            self.instance.content = query["content"]
            self.instance.save()
            
        return self.instance