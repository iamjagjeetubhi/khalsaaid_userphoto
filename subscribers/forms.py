from django import forms
from .models import Subscribers, Posts, photoUpload

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ('username',)

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post_id','created_date','created_time', 'message',)
class photoUploadForm(forms.ModelForm):
	class Meta:
		model = photoUpload
		fields = ('username',)