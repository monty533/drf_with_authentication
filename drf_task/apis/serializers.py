from rest_framework import serializers
from .models import User, Blog, Article
from django.contrib.auth.hashers import	make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
	    model = User
	    fields = ['id', 'name', 'email', 'password','username']

    def create(self, validated_data):
	    validated_data['password'] = make_password(validated_data.get('password'))
	    return User.objects.create(**validated_data)
	
    def update(self, validated_data, instance):
	    instance.name = validated_data.get('name', instance.name)
	    instance.email = validated_data.get('email', instance.email)
	    new_pass = make_password(validated_data.get('password'))
	    instance.password = new_pass if new_pass else instance.password
	    instance.save()
	    

class BlogSerializer(serializers.ModelSerializer):
	description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
	class Meta:
		model = Blog
		fields = ['id','title', 'description', 'author']



class ArticleSerializer(serializers.ModelSerializer):
	content = serializers.CharField(required=False, allow_null=True, allow_blank=True)
	class Meta:
		model = Article
		fields = ['id','title', 'content', 'blog', 'author']
