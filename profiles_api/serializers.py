from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta: #class container with some options (metadata) attached to the model. Defines things such as permissions, whether model is abstract or not, etc.
        model = models.UserProfile

        #list of all fields that we want to manage through our serializer
        fields = ('id', 'email', 'name', 'password')

        #to only make the password readonly and not writeable and password shows only the * characters and not the actual plaintext
        extra_kwargs = {
        'password':{
            'write_only' : True,
            'style' : {'input_type' : 'password'}
            }
        }

    #creates a new object | profile by using only the validated data that was serialized
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
        email = validated_data['email'],
        name = validated_data['name'],
        password = validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handles updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on') #id field is created automatically by django thus it is set to read-only by default
        #created_on field is also created automatically thus the only 2 fields that need to be serialized are user_profile and status_text
        #We don't want the user to be able to create profile feed items for other user profiles, thus we need to set user_profile to read-only

        extra_kwargs = {'user_profile' : {'read_only' : True}}
