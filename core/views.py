from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.contrib.auth.models import User

from . models import *

#For decorators
from django.contrib.auth.decorators import login_required

from itertools import chain

import random

#The attribute is used to redirect when you are in the index page without login in
@login_required(login_url='signin')
def index(request):
    #We a re bascially getting an object of the log in user
    user_object =User.objects.get(username =request.user)

    #we get the profile of the log in user from the User model created
   
    user_profile =Profile.objects.get(user=user_object)
   # Method e
   #  user_profile =Profile.objects.get(user=request.user)

    post =Post.objects.all()

    user_following_list= []
    
    feed =[]

    user_following = followersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)


    for usernames in user_following_list:
        feed_lists =Post.objects.filter(user =usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))


    #user suggestion starts

    all_users =User.objects.all()
    user_following_all =[]

    for user in user_following:
        user_list =User.objects.get(username =user.user)

        user_following_all.append(user_list)


    new_suggestion_list =[x for x in list(all_users) if (x not in list(user_following_all))]
    currrent_user =User.objects.filter(username =request.user.username)

    final_suggestions_list =[x for x in list(new_suggestion_list) if (x not in list(currrent_user))]

    random.shuffle(final_suggestions_list)


    username_profile =[]
    username_profile_list =[]

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists =Profile.objects.filter(id_user =ids)

        username_profile_list.append(profile_lists)

    suggestions_username_profile_list =list(chain(*username_profile_list))
    
    return render(request,'index.html',{
        'user_profile':user_profile,
        'posts':feed_list,
        'suggestions_username_profile_list':suggestions_username_profile_list[:4],

    })


def signup(request):



    if request.method =='POST':

        username =request.POST.get('username')
        email =request.POST.get('email')       
        password1 =request.POST.get('password1')
        password2=request.POST.get('password2')

        if password1 == password2:

            if User.objects.filter(username =username).exists():
                messages.error(request,'Username Taken')
                
                return redirect('signup')
            
            elif  User.objects.filter(email =email).exists():
                messages.error(request,'Email Taken')
                return redirect('signup')
        
        
            else:
                #Creating  a User 
                user =User.objects.create_user(username =username ,
                                          
                                          email =email ,
                                          
                                          password =password1)
                user.save()

                login(request,user)
                
                #creating a profile object for a new user
                user_model =User.objects.get(username=username)

                new_profile =Profile.objects.create(user =user_model, 
                                                    
                                                    id_user =user_model.id)
                
                new_profile.save()

                return redirect ('settings')
        else:
            messages.error(request,'Password dont match')

            return redirect('signup')


    else:
        


        return render(request,'signup.html')


def signin(request):


    if request.method == "POST":
        
        username =request.POST.get('username')
        password =request.POST.get('password')



        user =authenticate(username =username, password =password)

        if user is not None:

            login(request,user)
            return redirect('/')
        
        else:
            messages.error(request,"Credentials Invalid")
            return redirect('signin')
        


    else:
        return render(request,'signin.html')



#Setting of the account
@login_required(login_url='signin')
def settings(request):

    user_profile =Profile.objects.get(user = request.user)

    if request.method == "POST":

        if request.FILES.get('image') == None:
            image =user_profile.profile_img

        else:
            
            image =request.FILES.get('image')
           
        bio =request.POST.get('bio')
        location =request.POST.get('location')

        user_profile.profile_img =image

        user_profile.bio =bio

        user_profile.location =location

        user_profile.save()


    
        return redirect('settings')





    return render(request,'setting.html',{
        'user_profile': user_profile,
    })




@login_required(login_url='signin')
def Logout(request):

    logout(request)

    return redirect('/signin')



@login_required(login_url='signin')
def upload(request):

    if request.method =="POST":

        user =request.user.username
        caption =request.POST.get('caption')
        image =request.FILES.get('upload')

        new_post =Post.objects.create(user=user , caption =caption , image =image)
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')



@login_required(login_url='signin')
def like_post(request):

    username =request.user.username
    #We use Get to get a varibale value from a link
    post_id=request.GET.get('post_id')

    post_object =Post.objects.get(id =post_id)

    #Checking the post weather it has been liked by the logged in  user

    like_filter =LikePost.objects.filter(post_id =post_id, user_name =username).first()

    if like_filter == None:
        new_like =LikePost.objects.create(post_id =post_id ,user_name =username)
        new_like.save()

        post_object.no_likes =post_object.no_likes +1

        post_object.save()

        return redirect('/') 
    else:
        like_filter.delete()
        post_object.no_likes =post_object.no_likes -1

        post_object.save()

        return redirect('/')

@login_required(login_url='signin')
def profile(request,pk):
    
    user_obj =User.objects.get(username =pk)
   
    user_profile =Profile.objects.get(user =user_obj)
   
    user_post =Post.objects.filter(user=pk)

    user_post_length =len(user_post)
    
    follower =request.user.username
    user =pk

    if followersCount.objects.filter(follower =follower , user = user).first():
        button_text ='Unfollow'
    else:
        button_text ='Follow'

    user_followers =len(followersCount.objects.filter(user=pk))
    user_following =len(followersCount.objects.filter(follower=pk))
    

    return render(request,'profile.html',{
        'user_object':user_obj,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following


    })




@login_required(login_url='signin')
def follow(request):




    
    if request.method =='POST':
    
        follower =request.POST.get('follower')
        user =request.POST.get('user')
        

        if followersCount.objects.filter(follower =follower , user =user).first():
            delete_follower =followersCount.objects.get(follower=follower , user =user)
            delete_follower.delete()
            return redirect('profile',user)
        
        else:
            new_follower =followersCount.objects.create(follower =follower ,user =user)
            new_follower.save()
            return redirect('profile',user)
        
    else:
        return redirect('/')

    

def search(request):
    user_object =User.objects.get(username =request.user.username)
    profile =Profile.objects.get(user =user_object)
    
    if request.method == 'POST':
        username =request.POST.get('username')
        username_object =User.objects.filter(username__icontains =username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        
        for ids in username_profile:
            profile_list =Profile.objects.filter(id_user =ids)
            username_profile_list .append(profile_list)


        username_profile_list  =list(chain(*username_profile_list))

        

    return render(request,'search.html',{
        'user_profile':profile,
        'username_profile_list':username_profile_list,  
    })

"""
lawal
123



taye

taye


fatai
fatai


kenny
kenny
"""