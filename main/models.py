from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator

# Create your models here.
class Category(models.Model): 
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title
    
class Drink(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="drink_images")
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.name
    
class People(models.Model):
    Name=models.CharField(max_length=200,validators=[MinLengthValidator(5)])
    Phone_Number=models.TextField()
    Email=models.EmailField()
    Message=models.TextField()

