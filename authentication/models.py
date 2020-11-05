import jwt
from django.utils.timezone import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
# from app.apis.models import BaseModel
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teammanager = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']
    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()
    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email
    @property
    def token(self):
        """
        This method generates and returns a string of the token generated.
        """
        date = datetime.now() + timedelta(hours=24)
        payload = {
            'email': self.email,
            'exp': int(date.strftime('%s')),
            'id': self.id,
            'is_teammanager': self.is_teamlead,
            'is_manager': self.is_manager,
            'is_employee': self.is_employee,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()
