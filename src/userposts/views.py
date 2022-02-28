import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from userposts.forms import UserPostForm
from userposts.models import UserPost
from friends.models import FriendList

def home_page(request, *args, **kwargs):
    context = {}
    curr_user = request.user
    if request.method == "POST" and curr_user.is_authenticated:
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            content_val=form.cleaned_data.get("content")
            try: 
                request_file = request.FILES['post_image_file_selector'] 
                url = os.path.join(settings.MEDIA_ROOT + "/", str(curr_user.pk))
                fss = FileSystemStorage(location=url)
                file = fss.save(f"{curr_user.pk}.png", request_file)
                new_post = UserPost.objects.create(content=content_val, img=file, poster=request.user)
            except:
                new_post = UserPost.objects.create(content=content_val, poster=request.user)
    if curr_user.is_authenticated:
        # request.method GET
        friend_list = []
        try:
            curr_user_friend_list = FriendList.objects.get(user=curr_user)
            for friend in curr_user_friend_list.friends.all():
                friend_list.append(friend)
        except FriendList.DoesNotExist:
            pass

        if friend_list != []:
            # include curr user to list before filtering
            friend_list.append(curr_user)
            # display own post + friends' posts
            # filter UserPost based on poster = current user
            posts = reversed(UserPost.objects.filter(poster__in=friend_list).order_by('timestamp'))
            context['posts'] = posts
        else:
            # display own posts only
            # use orderby and reversed to display newer posts at the top while the older posts at the bottom
            posts = reversed(UserPost.objects.filter(poster=curr_user).order_by('timestamp'))
            context['posts'] = posts
        form = UserPostForm()
        context['form'] = form    
    return render(request, "userposts/homepage.html", context)