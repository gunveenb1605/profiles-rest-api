from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #Imports standard HTTP status codes
from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

#Allows us to define endpoint that we're going to assign to this view
#We define a URL which is our endpoint and then you assign it to this view and the django rest framwork
#handles it by calling the appropriate function in the view for the HTTP request that you make.
class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    #requests parameter is passed by the django framework and contains details of
    #request being made to the API
    #format parameter allows us to add format suffix to the end of the endpoint URL
    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application project',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello!', 'an_apiview':an_apiview})


    def post(self, request):
        "Create a hello message with our name"
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        #only updates fields provided in the request
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
        'Uses actions (list, create, retrieve, update, partial_update)',
        'Automatically maps to URLs usinf Routers',
        'Provides more functionality with less code',
        ]

        return Response({'message' : 'Hello!', 'a_viewset' : a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message' : message})
        else:
            return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    #will retrieve object with primary key that matches
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method' : 'GET'})

    #corresponds to HTTP put method
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk=None):
        """handle updating part of an object"""
        return Response({'http_method' : 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method' : 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating prfiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    #configure to use the permissions class and authentication
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (permissions.UpdateOwnProfile,)

    #allows us to search  by name or email of profile
    filter_backends = (filters.SearchFilter,)
    searchfields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    #By default, Django does not show the login page on the web browser, thus we need to override that behaviour by rendering that page using this command
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
