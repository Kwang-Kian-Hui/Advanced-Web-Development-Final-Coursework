from django import forms
from userposts.models import UserPost

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('img', 'content')
    
    def clean_content_data(self):
        content = self.cleaned_data['content']
        if content == None:
            raise forms.ValidationError("Contents of the post must not be empty.")