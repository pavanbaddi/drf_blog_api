from json import JSONEncoder
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class BaseModel( models.Model ):

    class Meta:
        abstract = True

    def fill( self, **query ):
        for key, value in query.items():
            self.__setattr__( key, value )
            
        return self
        
# Create your models here.
class PostQuerySet( models.QuerySet ):

    def search_name(self, value):
        return self.filter(name__icontains=value)

    def is_active(self, value=1):
        return self.filter(is_active=value)
        
    def is_active(self, value=1):
        return self.filter(is_active=value)

# class PostManager(models.Manager):
#     def get_queryset(self):
#         return PostQuerySet(self.model, using=self._db)

#     def search_name(self, value):
#         return self.get_queryset().search_name(value)

#     def is_active(self, value=1):
#         return self.get_queryset().is_active(value)

class BaseModelJSONEncoder(JSONEncoder):

    def default(self, o):
        
        try:
            if isinstance(o, models.Model):
                return model_to_dict(o)
            elif isinstance(o, models.query.QuerySet):
                return [ model_to_dict(obj) for obj in o ]
            else:
                iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, o)


class PostModel( models.Model ):
    post_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True)
    is_active = models.IntegerField(default=1)
    featured_image = models.CharField( max_length=255, null=True)
    meta_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)

    # objects = PostQuerySet.as_manager()
    
    class Meta():
        db_table = "posts"

    def slides(self):
        return FileModel.objects.filter(type="posts", type_id=self.pk)

    def get_meta_data(self):
        user_id  = self.meta_data.get("user_id") if self.meta_data else None
        if user_id:
            user = User.objects.filter(id=user_id).first()
            self.meta_data["user"] = UserSerializer(user).data if user else None

        return self.meta_data

    # def __str__(self):
    #     print("__str__ called")

    # def __repr__(self):
    #     print("__repr__ called")

    # def default(self, obj):
    #     print("inside default")
class FileModel(BaseModel):
    file_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    type_id = models.IntegerField()
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)
    class Meta():
        db_table = "files"

from comments.serializers import UserSerializer