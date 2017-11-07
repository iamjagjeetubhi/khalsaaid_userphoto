from django.shortcuts import render
from .forms import SubscriberForm, PostsForm, EmailSentForm
from .models import Subscribers, Posts, EmailSent
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

def subscriber(request):
    last_users = Subscribers.objects.all().order_by('-id')[:5]
    latest_user = last_users[0]
    return render(request, 'subscribers/profile.html', {
        'last_users': last_users,
        'latest_user':latest_user
        
    	})


def roundImage(url,username):
    import requests
    from io import BytesIO
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    im = im.resize((150, 150));
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    round_im = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    round_im.putalpha(mask)
    round_im.save(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.png', format='PNG', subsampling=0, quality=100)

def finalImage(username):
    font = ImageFont.truetype(settings.STATIC_ROOT+'assets/fonts/FreeSerif.ttf', 22)
    im = Image.open(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.png')
    background = Image.open(settings.STATIC_ROOT+'assets/img/background/background.jpg')
    background.paste(im, (44, 161), im) 
    background.save(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.png')
    img = Image.open(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.png')
    d = ImageDraw.Draw(img)
    w, h = d.textsize(username, font)
    d.text((134,67), username, font=font, fill=(244,121,32,255))
    img.save(settings.MEDIA_ROOT+'/uploaded_images/'+username+'.jpg', format='JPEG', subsampling=0, quality=100)

@csrf_exempt
def subscribed(request):
    try:
        if request.method == 'POST':
            data = request.POST
            import pdb
            username = data['username']
            username = username.lower()
            #password = data['password']
            print(settings.STATIC_ROOT)
            try:
                if bot.login(username=config('IG_USER'),password=config('IG_PASS')) is True:
                    try :
                        if bot.get_user_info(username) is not False:
                            info = bot.get_user_info(username)
                            url = info['profile_pic_url']
                            Subscribers.objects.get_or_create(username=username, dpUrl=url, photoUrl='media/uploaded_images/'+username+'.jpg')
                            print(settings.MEDIA_ROOT)
                            roundImage(url,username)
                            finalImage(username)
                            bot.logout()
                            return HttpResponse(json.dumps({'mesg': "photosuccess",}), content_type='application/json')                        
                        else:
                            bot.logout()
                            return HttpResponse(json.dumps({'mesg': "photofailed"}), content_type='application/json')
                    except:
                        print("photo upload failed exception")
                        return HttpResponse(json.dumps({'mesg': "photofailed"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'mesg': "failed"}), content_type='application/json')
            except:
                print("login exception failed")
                return HttpResponse(json.dumps({'mesg': "failed"}), content_type='application/json')
            
    except:
        print("end exception")
        return HttpResponse(json.dumps({'mesg': "failed"}), content_type='application/json')
              
