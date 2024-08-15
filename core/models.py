from django.db import models

#Getting user model
from django.contrib.auth import get_user_model

import uuid

from datetime import datetime

User =get_user_model()

class Profile(models.Model):

    #Linking the fk to the use models that is imported
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    
    id_user =models.IntegerField()
   
    bio = models.TextField(blank=True)
    #To add a default profile 
    #We use default attribute
    profile_img  =models.ImageField(upload_to='profile',default ='blank.png')
    
    location =models.CharField(max_length=100,blank=True)



    def __str__(self):

        return self.user.username
    



class Post(models.Model):

    #Uisng the uuid filed will give u a id but by defaul we wanna
    #create our own uuid id that the uuid4
    id = models.UUIDField(primary_key=True , default=uuid.uuid4)
    user =models.CharField(max_length=200)
    image =models.ImageField(upload_to='post_images')
    caption =models.TextField()
    created_at =models.DateTimeField(default=datetime.now)
    no_likes =models.IntegerField(default=0)




    def __str__(self):

        return self.user
    



class LikePost(models.Model):

    post_id =models.CharField(max_length=500)

    user_name =models.CharField(max_length=100)



    def __str__(self):

        return self.user_name
    


class followersCount(models.Model):
    follower =models.CharField(max_length=100)
    user =models.CharField(max_length=200)



    def __str__(self):
        return self.user    