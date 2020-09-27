from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from api.models import Label, Todo

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=6, max_length=100,
            write_only=True)

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('name',)

class TodoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'title', 'updated_at')


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True, many = False)
    assigned_users = UserSerializer(read_only = True, many = True)
    label_todo = serializers.SerializerMethodField()

    def get_label_todo(self, post):
        return post.label_todo.values_list('name', flat=True)

    class Meta:
        model = Todo
        fields = '__all__'
