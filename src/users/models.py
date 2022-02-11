from re import L
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("The email must not be empty.")
        if not username:
            raise ValueError("The username must not be empty.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_path(self):
    return f'profile_images/{self.pk}/{"profile_img.png"}'

def get_default_profile_img():
    return "project_files/default_profile.png"

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=40, unique=True)
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    profile_img = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_img)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # override defaults in AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    # define which field to be used as username and which fields are required
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_img).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

