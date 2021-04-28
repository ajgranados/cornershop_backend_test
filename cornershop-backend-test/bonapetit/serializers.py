from .models import Person, Menu, MenuOption, EmployeeMenu, User
from rest_framework import serializers
#from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import uuid

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'second_name', 'last_name', 'email']

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role']

    def create(self, validated_data):
        personData = validated_data.pop('person')
        email = validated_data.pop('email')
        print(email)
        password = validated_data.pop('password')

        print(password)
        person = Person.objects.create(**personData)

        return User.objects.create_user(email = email, password = password, person = person, **validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data.pop('email')
        password = data.pop('password')
        print(email)
        print(password)
        user = authenticate(email = email, password = password)#serializers.authenticate(email=username, password=password)
        print(user)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        #try:
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        #update_last_login(None, user)

        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'email': user.email,
            'role': user.role,
        }

        return validation
        #except AuthUser.DoesNotExist:
         #   raise serializers.ValidationError("Invalid login credentials")


"""class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

    def create(self, validated_data):
        return Role.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance"""

class MenuOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuOption
        fields = ['id', 'name', 'ingredients', 'menu']

    def create(self, validated_data):
        return MenuOption.objects.create(**validated_data)

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'available_date']

    def create(self, validated_data):
        menu = Menu.objects.create(uuid=uuid.uuid4(), **validated_data)
        return menu

class EmployeeMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMenu
        fields = ['id', 'user_id', 'option_id', 'without', 'extra']

    def create(self, validated_data):
        return EmployeeMenu.objects.create(**validated_data)
