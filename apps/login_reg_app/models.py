from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def validate_registration(self, post_data):
        # create an errors dictionary (some way of keeping track of which validations failed)
        errors = {}
        # validations are: 
        # presence of all fields,
        if len(post_data['name']) == 0:
            errors['name'] = "Name must be provided"
        if len(post_data['email']) == 0:
            errors['email'] = "Email must be provided"
        if len(post_data['password']) <8:
            errors['password'] = "Password must be provided and at least 8 characters in length"
        # making sure email is unique,
        emails_query = self.filter(email = post_data['email'])
        if len(emails_query) > 0:
            errors['email'] = "User with that email already exists"
        #  password == password_confirmation
        if post_data['password'] != post_data['password_confirmation']:
            errors['password'] = 'Password and password confirmation must match'
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField()

class Purchase(models.Model):
    product = models.ForeignKey(Product, related_name="purchased_product")
    buyer = models.ForeignKey(User, related_name="purchasing_buyer")
    quantity = models.IntegerField()
