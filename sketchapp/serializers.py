from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from sketchapp.models import *


class BlogSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Blog
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Messages
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = '__all__'