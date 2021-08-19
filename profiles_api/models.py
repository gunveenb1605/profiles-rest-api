from django.db import models

#Import these modules to override the default django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

#This import is to get the default user manager. We customize it according to need using UserProfileManager class
#By default, the django authenticates using username and name but in our app, we customize it to authenticate using email and name
#Hence we need to do all this processing as below
from django.contrib.auth.models import BaseUserManager

from django.conf import settings #For the feed API
#Used to retrieve settings from our Django project settings.py file


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #Helps manipulate objects in the model
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email: #if empty string given
            raise ValueError('User must have an email address')

        #normalize email address (make the second half completely to lowercase)
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) #converts to encrypted form, not plaintext
        #This function is available by default with django

        #Django allows multiple databases to be used. here we are using only one
        #By using this command, we say to django that we might use other databases in the future
        user.save(using=self._db)

        #return newly created users
        return user

        #we don't want super user to have None as password
    def create_superuser(self, email, name, password):
        """Create superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


#Inherited from base classes AbstractBaseUser and PermissionsMixin
#This will allow us to get all features of these 2 classes but will also allow it to customize them according to need
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    #We want an email field in the model with a max length of 255 chars
    #Unique=True means every email in the database must be unique
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) #detects if user is a staff and thus whether user should have access to the django app or not

    #Needed so that Django knows how to work with this custom user model using the CLI tools
    objects = UserProfileManager()

    #Need to specify this coz we are replacing our default django login by our custom email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

        #if whenever we read this model in the django admin, we want to identify it using the email
    def __str__(self):
        """Return string representation of user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    #we create foreign keys to link two models together in django
    #In the foreign key function, we do not handcode it to use the UserPofile mmodel coz later if we want to change it, we will have to manually
    #This we fetch the model name from the settings.py file
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE #since there is a foreign key rship, this model needs to be told what to do in case the primary key is deleted
        #Here we are telling this model that if primary key is deleted, cascade all these changes down, which means apply all those changes wherever applicable
        #Option other than cascading is set to null whic means, it would set the user profile model value to null
    )

    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True) #automatically add the date time field whenever a new feed item is created

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
