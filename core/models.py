from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


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


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name='categories', through='CategoryUser')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category_id']
        verbose_name_plural = 'categories'


class CategoryUser(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'core_category_user'
        unique_together = [['category', 'user']]


class FavoriteThing(models.Model):
    favorite_thing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    ranking = models.PositiveIntegerField()
    metadata = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='favorite_things')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_things')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_favorite_thing'
        constraints = [
            models.UniqueConstraint(fields=['title', 'category', 'user'],
                                    name='unique_favorite_thing')
        ]

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    audit_log_id = models.AutoField(primary_key=True)
    log = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_log')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.log
