from django.db import models
import datetime

class BaseModel( models.Model ):

    class Meta:
        abstract = True

    def fill( self, **query ):
        for key, value in query.items():
            self.__setattr__( key, value )
            
        return self
        
# Create your models here.
class PostQuerySet(models.QuerySet):
    def search_name( self, value ):
        return self.filter(name__icontains=value)

    def pk( self, value ):
        return self.filter(pk=value)
        
# class PostManager(models.Manager):
#     def get_queryset(self):
#         print("self._db", self._db)
#         return PostQuerySet(self.model, using=self._db)

#     def search_name( self, value ):
#         return self.get_queryset().search_name(value)

#     def pk( self, value ):
#         return self.get_queryset().pk(value)
        
# class PostManager(models.Manager):
#     def get_queryset(self):
#         return models.QuerySet(self.model, using=self._db)

#     def search_name( self, value ):
#         return self.filter(name__icontains=value)

#     def pk( self, value ):
#         return self.filter(pk=value)

class PostModel(BaseModel):
    post_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True)
    featured_image = models.CharField( max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)

    objects = PostQuerySet().as_manager()
    
    class Meta():
        db_table = "posts"

    def slides(self):
        return FileModel.objects.filter(type="posts", type_id=self.pk)
class FileModel(BaseModel):
    file_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    type_id = models.IntegerField()
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)
    class Meta():
        db_table = "files"