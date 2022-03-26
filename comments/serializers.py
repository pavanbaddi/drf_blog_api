from comments.models import CommentModel
from posts.models import PostModel
from rest_framework import serializers
from django.contrib.auth.models import User

class CommentSerializer( serializers.Serializer ):
    comment_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255)
    content = serializers.CharField( required=False )
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
    created_at = serializers.DateTimeField( required=False )
    updated_at = serializers.DateTimeField( required=False )

    user = serializers.SerializerMethodField()

    instance = None
    class Meta:
        extra_kwargs = {
            "updated_at" : {
                "write_only" : True
            }
        }
    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)

    def validate_user_id( self, value ):
        count = User.objects.filter(id=value).count()

        if count == 0:
            raise serializers.ValidationError(f"User with id {value} does not exists.")
            
        return value

    def validate_post_id( self, value ):
        count = PostModel.objects.filter(post_id=value).count()

        if count == 0:
            raise serializers.ValidationError(f"Post does not exists.")

        return value

    @property
    def data(self):
        data = super(CommentSerializer, self).data
        if self.instance:
            data.update({
                "comment_id" : self.instance.pk,
                "created_at" : self.instance.created_at,
                "updated_at" : self.instance.updated_at,
            })

        return data

    def save( self ):
        validated_data = self.validated_data
        user = User.objects.get(id=validated_data["user_id"])
        post = PostModel.objects.get(post_id=validated_data["post_id"])
       
        query = {
            "name" : validated_data["name"],
            "content" : validated_data.get("content", "no content present"),
            "user" : user,
            "post" : post
        }
                
        self.instance, created = CommentModel.objects.update_or_create( 
            comment_id = validated_data.get('comment_id', None),
            defaults=query 
        )
        
        return self.instance

    def get_user(self, obj):
        return UserSerializer(obj.user).data if obj.user else {}

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = ["id", "first_name", "last_name", "email"]
        fields = "__all__"
        extra_kwargs = {
            "password" : {
                "write_only" : True
            },
            "groups" : {
                "write_only" : True
            },
            "user_permissions" : {
                "write_only" : True
            }
        }