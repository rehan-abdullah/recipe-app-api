from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings


class UserManager(BaseUserManager):

    # **extra_fields allows any fields added to the model to be passed
    # down to the manager.
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """

        # Raise ValueError if no email provided
        # when trying to create a new user
        if not email:
            raise ValueError('Users must have an email address!')

        # self.model allows the manager to access the model that the
        # manager is targeting.
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using=self._db is required for supporting multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves a new superuser """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        # user has been modified so must save
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username. """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used for a recipe """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
