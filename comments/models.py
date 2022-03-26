from django.db import models
import datetime
from django.contrib.auth.models import User

from posts.models import BaseModel, PostModel

# Create your models here.

class CommentQuerySet(models.QuerySet):
    def posts( self, value ):
        return self.filter(post=value)


    def strainer( self, kwargs ):
        query = self

        if kwargs.get("post_id"):
            query = self.posts(kwargs["post_id"])

        if kwargs.get("user_id"):
            query = self.filter(user_id=kwargs["user_id"])

        if kwargs.get("comment_id"):
            query = self.filter(comment_id=kwargs["comment_id"])

        return query

    # def order_by( self, value ):
    #     return self.filter(post=value)

class CommentModel(BaseModel):
    comment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=PostModel, on_delete=models.CASCADE, related_name="comments" )
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)

    objects = CommentQuerySet.as_manager()
    
    class Meta():
        db_table = "comments"