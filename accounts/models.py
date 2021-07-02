from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # import AbstractBaseUser & BaserUserManger

# Create your models here.

#Custom Manger and Function for Creating User and Super User in Custom User Model
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None): #creating normal user function code
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #creating super user function code
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user( #using create_user function here for creating superuser 
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    # must required when you making custom usr model 
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = MyAccountManager() # Inheriting MyAccountManager HERE
    
    def __str__(self):
        return self.email
    
    # need to define also these below mandatory methods
    def has_perm(self, perm, obj=None):
        return self.is_admin # Mening of this function is if the user is admin he has all permission
    
    def has_module_perms(self, add_label):
        return True
    
    
    
    
    
    
    