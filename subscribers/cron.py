from django.shortcuts import render
from .forms import SubscriberForm, PostsForm, photoUploadForm
from .models import Subscribers, Posts, photoUpload
from datetime import datetime
from pytz import timezone
from django.core.mail import EmailMessage
from decouple import config
from django.conf import settings
import subprocess
import os
import sys
import time
import random
from tqdm import tqdm
import argparse
import subprocess
from instabot import Bot, API
api=API()
bot = Bot()

def uploadPhoto(username):
    try:
        if bot.login(username=config('IG_USER2'),password=config('IG_PASS2')) is True:
            try:
                caption = "In the support of KHALSAAID Instagram/#"+username+" just posted a photo!"
                hashtags = "#khalsaaid #supportkhalsaaid #khalsaaidigapp #khalsaaidsupporters"
                caption = caption +' '+ hashtags 
                if bot.uploadPhoto(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.jpg',caption=caption) is True:
                    print("photo uploaded successfully")
                    bot.logout()
                else:
                    print("photo failed to upload")
                    bot.logout()
            except:
                print("photo upload failed exception")
        else:
            print("unable to login")
    except:
        print("process failed")



def my_scheduled_job():
    last_uploaded_username = photoUpload.objects.last()
    last_uploaded_username = last_uploaded_username.username
    print("photo uploaded for last user is"+last_uploaded_username)


    users = Subscribers.objects.all().order_by('-id')
    for user in users:
        username = user.username
        print("usernames are "+username)
        if not photoUpload.objects.filter(username=username).exists():
            print("not a photouser")
            photoUpload.objects.create(username=username)
            uploadPhoto(username)