from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, request
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.models import User
import requests
import json
from rest_framework import authentication
from rest_framework.views import APIView
from django.views.generic import ListView

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView  
from rest_framework import viewsets, status
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

#authentication helpers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate,logout, login
from django.contrib import messages

#from web.serializers import *
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser

from sketchapp.forms import *
from sketchapp.models import *
from sketchapp.serializers import *


class CompanyPagination(pagination.PageNumberPagination):
    page_size = 9

##### Auth View #####
#####################
class signin(APIView):
    def get(self, request):
        form=LoginForm()
        return render(request, 'user/login.ejs',{'form':form})

class signinpg(APIView):
    def post(self,request):
        form = LoginForm()
        user = authenticate(
            username=request.POST['name'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(reverse('dashboard'))
            else:
                return redirect(reverse('signin'))
        context = {
            'error':"Invalid Credential",
            'form': form
        }
        return render(request, 'web/login.ejs', context=context)

class logoutpg(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request):
        logout(request)
        print("done")
        return redirect('/signin')

#user main view
class index(APIView):
    def get(self, request):
        return render(request, 'user/home.ejs')

class about(APIView):
    def get(self, request):
        return render(request, 'user/about.ejs')

class blogs(APIView):
    def get(self, request):
        return render(request, 'user/blog.ejs')

class blogDetail(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            'blog' : self.kwargs['id']
        }
        return render(request, 'user/blogDetail.ejs',context=context) 

class contact(APIView):
    def get(self, request):
        return render(request, 'user/contact.ejs')

class Profile(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(reverse('signin'))
        profile=UserProfile.objects.get(user=self.request.user)
        if not profile.is_admin:
            return redirect(reverse('home'))
        context = {
            'profile' : self.kwargs['id'],
        }
        return render(request, 'user/myProfile.ejs',context=context)

class ProfilePage(APIView):
    def get(self, request):
        context = {
            'user' : UserProfile.objects.get(user=self.request.user)
        }
        return render(request, 'user/profilePage.ejs',context=context)


#admin main view
class dashboard(APIView):
    def get(self, request):
        return render(request, 'admin/index.ejs')

class AddBlog(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            'blog' : self.kwargs['id']
        }
        return render(request, 'admin/addBlog.ejs',context=context) 

class BlogList(APIView):
    def get(self, request):
        context = {
            "blogs": Blog.objects.all().order_by('-id')
        }
        return render(request, 'admin/blogList.ejs',context=context) 

class UserList(APIView):
    def get(self, request):
        context = {
            "users": UserProfile.objects.all().order_by('-id')
        }
        return render(request, 'admin/userList.ejs',context=context) 

class ViewContacts(APIView):
    def get(self, request):
        return render(request, 'admin/viewContacts.ejs')


#post views
class PostBlog(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def post(self, request, *args, **kwargs):
        if self.kwargs['id'] == 0:
            blog = BlogSerializer(data=request.data)
        else:
            obj = Blog.objects.get(pk=self.kwargs['id'])
            blog = BlogSerializer(obj,data=request.data)
        if blog.is_valid():
            blog.save()
            return Response(blog.data, status=status.HTTP_201_CREATED)
        return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)

class PostMessage(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def post(self, request):
        serializer = MessageSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostProfile(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def post(self, request, *args, **kwargs):
        if self.kwargs['id'] == 0:
            profile= UserProfileSerializer(data=request.data)
        else:
            obj = UserProfile.objects.get(pk=self.kwargs['id'])
            profile = UserProfileSerializer(obj,data=request.data)
        if profile.is_valid():
            profile.save()
            return Response(profile.data, status=status.HTTP_201_CREATED)
        return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)


#api list views
class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    pagination_class = CompanyPagination
    def get_queryset(self):
        data=Blog.objects.all().order_by('-id')
        return data 

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = CompanyPagination
    def get_queryset(self):
        data=Messages.objects.all().order_by('-id')
        return data



#filter 
class BlogDetailAPIView(APIView):
    def get(self,request,*args,**kwargs):
        blog = Blog.objects.get(pk=self.kwargs['id'])
        ser = BlogSerializer(blog)
        response = {
            'data' : ser.data
        }
        return Response(response)

class userDetailAPIView(APIView):
    def get(self,request,*args,**kwargs):
        userdata = UserProfile.objects.get(pk=self.kwargs['id'])
        ser = UserProfileSerializer(userdata)
        response = {
            'data' : ser.data
        }
        return Response(response)

class MessageAPIView(APIView):
    def get(self,request,*args,**kwargs):
        message = Messages.objects.get(pk=self.kwargs['id'])
        ser = MessageSerializer(message)
        response = {
            'data' : ser.data
        }
        return Response(response)


#delete
class DeleteBlog(APIView):
    def get(self,request,*args,**kwargs):
        try:
            data=Blog.objects.get(pk=self.kwargs['id'])
            data.delete()
            return redirect('/BlogList')
        except:
            return Response({'result' : False})

class DeleteProfile(APIView):
    def get(self,request,*args,**kwargs):
        try:
            data=UserProfile.objects.get(pk=self.kwargs['id'])
            data.delete()
            return redirect('/UserList')
        except:
            return Response({'result' : False})

class DeleteMessage(APIView):
    def get(self,request,*args,**kwargs):
        try:
            data=Messages.objects.get(pk=self.kwargs['id'])
            data.delete()
            return redirect('/ViewContacts')
        except:
            return Response({'result' : False})

# Create your views here.
