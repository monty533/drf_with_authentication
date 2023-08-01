from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, BlogSerializer, ArticleSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User, Blog, Article
# from django.contrib.auth import authenticate
from django.contrib.auth.hashers import	check_password
from rest_framework_simplejwt.tokens import AccessToken
import jwt

# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        # print ("********* In function ****************")
        data = request.data
        ser = UserSerializer(data=data)
        if ser.is_valid():
	        ser.save()
	        current_user = User.objects.get(username=data.get('username'))
	        refresh = RefreshToken.for_user(current_user)
	        response_data = {
		    	'refresh_token': str(refresh),
		    	'access_token': str(refresh.access_token),
		    	'userid':str(current_user.id)
	    	}
	        return Response(response_data, status=status.HTTP_201_CREATED)
        else:
	        return Response({'title':'Error', 'message':f'User Registratin failed because of the error => {ser.errors}'})

class UserLogin(APIView):
      def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        current_user = User.objects.get(username=username)
        if not current_user:
              return Response({'title':'Error', 'message':'No user found with the given Username'}, status=401)
        correct_pass = check_password(password, current_user.password)
        if not correct_pass:
              return Response({'title':'Error', 'message':'Incorrect Password'}, status=401)
        if (current_user):
                refresh_token = RefreshToken.for_user(current_user)
                access_token = refresh_token.access_token
                response_data = {
                                           'refresh_token':str(refresh_token),
                                           'access_token':str(access_token),
                                           'userid':str(current_user.id),
                                           'title':'Success',
                                           'message':'User loggedin Successfully',
				}
                return Response(response_data, status=status.HTTP_200_OK)
        else:
                return Response({'title':'Error', 'message':'Invalid Username or Password'}, status=400)
        

class GetUser(APIView):
      def post(self, request):
            jwt_token = request.headers.get('X-Authorization')
            try:
                access_token = AccessToken(jwt_token)
                user_id = access_token.payload['user_id']
                user = User.objects.get(id=user_id)
                user_data = UserSerializer(user)
                return Response({'title':'Success', 'data':user_data.data}, status=200)
            except Exception as e:
                  return Response({'title':'Error', 'message':f'Token is either invalid or expired => {e}'}, status=401)
            

class BlogApis(APIView):
      def post(self, request):
            '''
            This function creates a new blog. The user is authenticated using jwt.
            '''
            jwt_token = request.headers.get('X-Authorization')
            try:
                  access_token = AccessToken(jwt_token)
                  user_id = access_token.payload['user_id']
                  try:
                        user = User.objects.get(id=user_id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No User Found for given Credintials'}, status=401)
                  data = request.data
                  data['author'] = user_id
                  ser = BlogSerializer(data=data)
                  if ser.is_valid():
                        ser.save()
                        return Response({'title':'Success', 'message':'Blog Created Successfully', 'data':ser.data}, status=201)
                  return Response({'title':'Error', 'message':f'Error in creating Blog => {ser.errors}'}, status = 500)
            except Exception as e: 
                  return Response({'title':'Error', 'message':f'Token is invalid or expired => {e}'}, status=401)
            
      def put(self, request):
            '''
            This function modifies the blog after authenticating the user through jwt and authorizes only if the user is the author. Blog is modified if the valid blog id is provided.
            '''
            user_id = verify_token(request)
            if user_id:
                  try:
                        user = User.objects.get(id = user_id)
                  except Exception as e:
                        return Response ({'title':'Error', 'message':'Not a valid user'}, status = 401)
                  id = request.data.get('blog_id')
                  if not id :
                        return Response({'title':'Error', 'message':'Please Provide Blog id'}, status = 400)
                  try:
                        blog = Blog.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No Blog found for given id'}, status = 400)
                  if (user_id != blog.author.id):
                        return Response({'title':'Error', 'message':'Only Authors can modify the Blogs'})
                  ser = BlogSerializer(blog, data=request.data, partial=True)
                  if ser.is_valid():
                        ser.save()
                        return Response({'title':'Success', 'message':'Blog Updated Successfuly'}, status=200)
            else:
                  return Response({'title':'Error', 'message':'Token is either invalid or expired'}, status = 401)
            
      def get(self, request):
            '''
            This function returns single blog or a list of blogs depending upon the parameters passed
            '''
            id = request.data.get('blog_id')
            if id:
                  try:
                        blog = Blog.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No blog found for the given id'}, status = 400)
                  ser = BlogSerializer(blog)
                  return Response({'title':'Success', 'message':'Blog fetched Successfully', 'data':ser.data}, status=200)
            blogs = Blog.objects.all()
            ser = BlogSerializer(blogs, many=True)
            return Response({'title':'Success', 'message':'List of Articles fetched Successfully', 'data':ser.data}, status=200)
      
      def delete(self, request):
            '''
            This function deletes the blog of the given id, if the blog id is invalid returns a error message.
            '''
            user_id = verify_token(request)
            if user_id:
                  try:
                        user = User.objects.get(id = user_id)
                  except Exception as e:
                        return Response ({'title':'Error', 'message':'Not a valid user'}, status = 401)
                  id = request.data.get('blog_id')
                  if not id :
                        return Response({'title':'Error', 'message':'Please Provide blog id'}, status = 400)
                  try:
                        blog = Blog.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No Blog found for given id'}, status = 400)
                  if (user_id != blog.author.id):
                        return Response({'title':'Error', 'message':'Only Authors can modify the blogs'})
                  blog.delete()
                  return Response({'title':'Success', 'message':'Blog with the given id deleted successfully'}, status=204)

            else:
                  return Response({'title':'Error', 'message':'Token is either invalid or expired'}, status = 401)

            

class ArticleApis(APIView):

      def post(self, request):
            '''
            This function created new articles for the given blog if the user is authenticated through jwt
            '''
            jwt_token = request.headers.get('X-Authorization')
            try:
                  access_token = AccessToken(jwt_token)
                  user_id = access_token.payload['user_id']
                  try:
                        user = User.objects.get(id=user_id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No User Found for given Credintials'}, status=401)
                  data = request.data
                  data['author'] = user_id
                  ser = ArticleSerializer(data=data)
                  if ser.is_valid():
                        ser.save()
                        return Response({'title':'Success', 'message':f'Article Created Successfuly =>{ser.data}'}, status=201)
                  return Response({'title':'Error', 'message':f'There is some error in creating Article =>{ser.errors} '})
            except Exception as e:
                  return Response({'title':'Error', 'message':f'Token is invalid or expired => {e}'}, status=401)
            
      def put(self, request):
            '''
            This function updates the given article if the article id is valid and the user is the author of the article, user is authenticated using jwt
            '''
            user_id = verify_token(request)
            if user_id:
                  try:
                        user = User.objects.get(id = user_id)
                  except Exception as e:
                        return Response ({'title':'Error', 'message':'Not a valid user'}, status = 401)
                  id = request.data.get('article_id')
                  if not id :
                        return Response({'title':'Error', 'message':'Please Provide Article id'}, status = 400)
                  try:
                        article = Article.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No Article found for given id'}, status = 400)
                  if (user_id != article.author.id):
                        return Response({'title':'Error', 'message':'Only Authors can modify the articles'})
                  ser = ArticleSerializer(article, data=request.data, partial=True)
                  if ser.is_valid():
                        ser.save()
                        return Response({'title':'Success', 'message':'Article Updated Successfuly'}, status=200)
            else:
                  return Response({'title':'Error', 'message':'Token is either invalid or expired'}, status = 401)
            
      def get(self, request):
            '''
            This function returns single article or a list of articles depending upon the parameters passed
            '''
            id = request.data.get('article_id')
            if id:
                  try:
                        article = Article.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No article found for the given id'}, status = 400)
                  ser = ArticleSerializer(article)
                  return Response({'title':'Success', 'message':'Article fetched Successfully', 'data':ser.data}, status=200)
            articles = Article.objects.all()
            ser = ArticleSerializer(articles, many=True)
            return Response({'title':'Success', 'message':'List of Articles fetched Successfully', 'data':ser.data}, status=200)

      def delete(self, request):
            '''
            This function deletes the article of the given id, if the article id is invalid returns a error message.
            '''
            user_id = verify_token(request)
            if user_id:
                  try:
                        user = User.objects.get(id = user_id)
                  except Exception as e:
                        return Response ({'title':'Error', 'message':'Not a valid user'}, status = 401)
                  id = request.data.get('article_id')
                  if not id :
                        return Response({'title':'Error', 'message':'Please Provide Article id'}, status = 400)
                  try:
                        article = Article.objects.get(id=id)
                  except Exception as e:
                        return Response({'title':'Error', 'message':'No Article found for given id'}, status = 400)
                  if (user_id != article.author.id):
                        return Response({'title':'Error', 'message':'Only Authors can modify the articles'})
                  article.delete()
                  return Response({'title':'Success', 'message':'Article with the given id deleted successfully'}, status=204)

            else:
                  return Response({'title':'Error', 'message':'Token is either invalid or expired'}, status = 401)

                  
def verify_token(request):
      jwt_token = request.headers.get('X-Authorization')
      try:
            access_token = AccessToken(jwt_token)
            user_id = access_token.payload['user_id']
            return user_id
      except Exception as e:
            return 0
            