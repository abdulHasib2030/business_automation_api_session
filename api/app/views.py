from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import views, response, status
from app.serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# Create your views here.
#### Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access' : str(refresh.access_token),
  }
  
########## User Account Register View ###############
class UserRegistrationView(views.APIView):
  def post(self, request):
    serializer = UserRegistrationSerializer(data= request.data)
    serializer.is_valid(raise_exception= True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return response.Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(views.APIView):
  def post(self, request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username = username, password = password)
    
    if user is not None:
      token = get_tokens_for_user(user)
      return response.Response({'token': token, 'msg':"Login Success"}, status=status.HTTP_200_OK)
    else:
      return response.Response({'errors':{'non_field_errors': ['Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class ProfileView(views.APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    serializer = UserProfileSerializer(request.user)
    return response.Response(serializer.data, status = status.HTTP_200_OK)
  

