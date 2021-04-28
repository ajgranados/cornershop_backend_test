from .models import Menu, User, MenuOption, EmployeeMenu
from .serializers import UserRegistrationSerializer, MenuSerializer, UserLoginSerializer, MenuOptionSerializer, EmployeeMenuSerializer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime

"""
This class has the functionality for the endpoints /user
GET /user bring all the users in the data base
POST /user create a new user

This endpoints doesn't need a token
"""
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().filter(is_active = True)
    serializer_class = UserRegistrationSerializer

"""
This class has the functionality for the endpoints /user/id
GET /user/id bring the user with the given id
PUT /user/id update the data of the user with the given id
DELETE /user/id deletes the user with the given id

This endpoints need a token
"""
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().filter(is_active = True)
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

"""
This class has the functionality for the endpoints /menu
GET /menu bring all the menu in the data base
POST /menu create a new menu

This endpoints doesn't need a token
"""
class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formar = None):
        user = request.user
        if(user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to see this"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menus = Menu.objects.all()
            menuSerializer = self.serializer_class(menus, many = True)

            return Response(menuSerializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to create a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuSerializer = MenuSerializer(data = request.data)
            if menuSerializer.is_valid():
                menuSerializer.save()

                return Response(menuSerializer.data, status = status.HTTP_201_CREATED)

            return Response(menuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
This class has the functionality for the endpoints /menu/uuid
GET /menu/uuid bring the user with the given id
PUT /menu/uuid update the data of the user with the given id
DELETE /menu/uuid deletes the user with the given id

This endpoints need a token, except the GET method
"""
class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all().filter()
    serializer_class = MenuSerializer

    def get_object(self, uuid):
        try:
            return Menu.objects.get(uuid = uuid)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        menu = self.get_object(uuid)
        menuSerializer = MenuSerializer(menu)

        options = MenuOption.objects.all().filter(menu = menu)
        optionsSerializer = MenuOptionSerializer(options, many = True)
        response = {
            'menu': menuSerializer.data,
            'options': optionsSerializer.data
        }

        return Response(response)

    def put(self, request, uuid, format=None):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to change a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menu = self.get_object(uuid)
            menuSerializer = MenuSerializer(menu, data=request.data)

            if menuSerializer.is_valid():
                menuSerializer.save()
                return Response(menuSerializer.data)

            return Response(menuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to delete a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menu = self.get_object(uuid)
            menu.delete()

            return Response(status=status.HTTP_200_OK)

"""
This class has the functionality for the endpoints /menuoptions
GET /menuoptions bring all the options of the menus in the data base
POST /menuoptions create a new option for a menu

This endpoints doesn't need a token
"""
class MenuOptionList(generics.ListCreateAPIView):
    serializer_class = MenuOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format = None):
        user = request.user
        if(user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to see this"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuOptions = MenuOption.objects.all()
            menuOptionSerializer = self.serializer_class(menuOptions, many = True)

            return Response(menuOptionSerializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to create an option for a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuOptionSerializer = MenuOptionSerializer(data = request.data)
            if menuOptionSerializer.is_valid():
                menuOptionSerializer.save()

                return Response(menuOptionSerializer.data, status = status.HTTP_201_CREATED)

            return Response(menuOptionSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
This class has the functionality for the endpoints /menuoptions/id
GET /menuoptions/id bring the option with the given id
PUT /menuoptions/id update the data of the option with the given id
DELETE /menuoptions/id deletes the option with the given id

This endpoints need a token
"""
class MenuOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuOptionSerializer

    def get_object(self, id):
        try:
            return MenuOption.objects.get(id = id)
        except MenuOption.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to view a Menu option"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuOption = self.get_object(id)
            menuOptionSerializer = MenuOptionSerializer(menuOption)

            return Response(menuOptionSerializer.data, status = status.HTTP_200_OK)

    def put(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to change a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuOption = self.get_object(id)
            menuOptionSerializer = MenuOptionSerializer(menuOption, data=request.data)

            if menuOptionSerializer.is_valid():
                menuOptionSerializer.save()
                return Response(menuOptionSerializer.data)

            return Response(menuOptionSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        if (user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to delete a Menu"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            menuOption = self.get_object(id)
            menuOption.delete()

            return Response(status=status.HTTP_200_OK)

"""
This class has the functionality for the endpoint /authenticate
POST /menuoptions generates a new token if the user is valid

This endpoint doesn't need a token
"""
class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

"""
This class has the functionality for the endpoints /employeemenu
GET /employeemenu bring all the orders from the users in the data base
POST /employeemenu create a new order for a user for a menu

This endpoints doesn't need a token
"""
class EmployeeMenuList(generics.ListCreateAPIView):
    serializer_class = EmployeeMenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format = None):
        user = request.user
        if(user.role != 1):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "Only the chef is authorized to see this"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            employeeMenu = EmployeeMenu.objects.all()
            employeeMenuSerializer = self.serializer_class(employeeMenu, many = True)

            return Response(employeeMenuSerializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        user = request.user
        if (datetime.now().hour > 10 and datetime.now().minute > 0):
            response = {
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': "The time to order a menu has expired"
            }

            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            employeeMenuSerializer = EmployeeMenuSerializer(data = request.data)
            if employeeMenuSerializer.is_valid():
                employeeMenuSerializer.save()

                return Response(employeeMenuSerializer.data, status = status.HTTP_201_CREATED)

            return Response(employeeMenuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
This class has the functionality for the endpoints /employeemenu/id
GET /employeemenu/id bring the order with the given id
PUT /employeemenu/id update the order with the given id
DELETE /employeemenu/id deletes the order with the given id

This endpoints need a token
"""
class EmployeeMenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeMenu.objects.all().filter()
    serializer_class = EmployeeMenuSerializer

    def get_object(self, id):
        try:
            return EmployeeMenu.objects.get(id = id)
        except EmployeeMenu.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]

        employeeMenu = self.get_object(id)
        employeeMenuSerializer = EmployeeMenuSerializer(employeeMenu)

        return Response(employeeMenuSerializer.data, status = status.HTTP_200_OK)

    def put(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]

        employeeMenu = self.get_object(id)
        employeeMenuSerializer = EmployeeMenuSerializer(employeeMenu, data=request.data)

        if employeeMenuSerializer.is_valid():
            employeeMenuSerializer.save()
            return Response(employeeMenuSerializer.data)

        return Response(employeeMenuSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        permission_classes = [permissions.IsAuthenticated]

        employeeMenu = self.get_object(id)
        employeeMenu.delete()

        return Response(status=status.HTTP_200_OK)