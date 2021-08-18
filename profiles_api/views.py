from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #Imports standard HTTP status codes
from profiles_api import serializers

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
