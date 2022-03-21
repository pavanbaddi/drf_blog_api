from django.db import models
import datetime

# Create your models here.
class PostModel(models.Model):
    post_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True)
    featured_image = models.CharField( max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)
    class Meta():
        db_table = "posts"

    def fill( self, **query ):
        for key, value in query.items():
            self.__setattr__( key, value )
            
        return self

    def slides(self):
        return FileModel.objects.filter(type="posts", type_id=self.pk)
class FileModel(models.Model):
    file_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    type_id = models.IntegerField()
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)
    class Meta():
        db_table = "files"

    def fill( self, **query ):
        for key, value in query.items():
            self.__setattr__( key, value )
            
        return self