from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class UserManger(BaseUserManager):
    """Creates and save a new user"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Customer must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """"Creates and saves a new superuser"""
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'email'


class Category(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='categories', through='CategoryUser')

    class Meta:
        ordering = ['category_id']
        verbose_name_plural = 'categories'


class CategoryUser(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'core_category_user'
        unique_together=[['category', 'user']]
