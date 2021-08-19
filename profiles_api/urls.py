#Stores URLs for our API
from django.urls import path, include
from rest_framework.routers import DefaultRouter #For ViewSet
from profiles_api import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset') #to register our viewset with the router, the first arguement is the name of url that we wish to create
#second argument is the viewset that we wish to register #third argument is the base_name which is used if we need to use the default returning function provided by django
#need to assign base_name coz queryset is not defined for this viewset

router.register('profile', views.UserProfileViewSet)
#don't need to assign a base_name coz we have specified a queryset for this view

router.register('feed', views.UserProfileFeedViewSet)
#don't need to assign a base_name coz we have specified a queryset for this view

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()), #as_view function helps render the HelloApiView
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)) #we use an empty string in the beginning because we don't want to put any prefix to this url, we just want to include all of urls in the base of this urls file

]
