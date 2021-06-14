from django.db import models, IntegrityError
import re 
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def reg_validation(self, post_data):
        errors = {}
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Email is not valid'
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    objects = UserManager()



class Favorites(models.Model):
    title = models.CharField(max_length=255 )
    category = models.CharField(max_length=45)
    instructions = models.CharField(max_length=1024*2)
    ingredients = models.CharField(max_length=1024*2)
    poster= models.ForeignKey(User, related_name="user_favorites", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
