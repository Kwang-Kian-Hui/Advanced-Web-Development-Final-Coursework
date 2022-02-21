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

    # def save(self, commit=True):
    #     userpost = super(UserPostForm, self).save(commit=False)
    #     # userpost.content = self.cleaned_data['content']
    #     # userpost.img = self.cleaned_data['img']
    #     # userpost.poster = user.pk
    #     # if commit:
    #     userpost.save()
    #     return userpost