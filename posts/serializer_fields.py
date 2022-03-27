from rest_framework import serializers
from django.core.exceptions import ValidationError 
import json
from django.contrib.auth.models import User
from comments.serializers import UserSerializer

class PostMetaSerializerField( serializers.Field ):

    # respresentation for json
    def to_representation(self, values):
        try:
            if values and values.get("user_id"):
                user_id = values.get("user_id")
                user = User.objects.filter(id=user_id).first()
            
                if user:
                    values.update({
                        "user" : UserSerializer(user).data
                    }) 
        except:
            values = None

        return values

    # respresentation for python object
    def to_internal_value(self, values):
        try:
            json_data = json.loads(values)
        except:
            raise ValidationError("Invalid JSON")
        return json_data