from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_reqex = re.compile(r'^[a-zA-Z]+$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # validating fname and lname with less than 2 character
        if len(postData['fname']) < 2:
            errors['fname'] = "First name must be at least 2 characters long!"
        if not name_reqex.match(postData['fname']):
            errors['fname']="First name can not contain numbers!"
        if len(postData['lname']) < 2:
            errors['lname'] = "Last name must be at least 2 characters long!"
        if not name_reqex.match(postData['lname']):
            errors['lname']="Last name can not contain numbers!"
        # email required
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email id used!"
        if len(postData['email']) < 1:
            errors['email'] = "Email is required!"
        # password required 8 characters
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters!"
        if postData['pw']!=postData['checkpw']:
            errors['checkpw']="Password do not match!"
        return errors
    
    def login_validator(self, postData):
        errors={}
        checkemail=postData['email']
        user.User.objects.filter(email=checkemail)
        if len(user) < 1:
            errors['login']="Invalid email or password!"
        elif not bcrypt.checkpw(postData['pw'].encode(), user[0].pw.concode()):
            errors['login']="Invalid email or password!"
        return errors
            
        


class User(models.Model):
    fname = models.CharField(max_length=225)
    lname = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    pw = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
