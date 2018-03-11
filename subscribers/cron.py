from django.shortcuts import render
from .forms import SubscriberForm, PostsForm, photoUploadForm
from .models import Subscribers, Posts, photoUpload
from datetime import datetime
from pytz import timezone
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
import json
from django.conf import settings
from decouple import config
import sys
import os
import time
import random
from tqdm import tqdm
import argparse
import subprocess
from django.core.mail import EmailMessage
from PIL import Image, ImageOps, ImageDraw, ImageFont
from django.views import generic
#sys.path.append(os.path.join(sys.path[0], '/home/jagjeet/Documents/khalsaaid/instagram_login/instabot/'))
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
                    #bot.logout()
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
