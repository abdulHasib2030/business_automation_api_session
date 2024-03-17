from rest_framework import serializers
from django.contrib.auth.models import User

#### User Registration Serializers #####
class UserRegistrationSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = [ 'username', 'password']

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)
  
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
    