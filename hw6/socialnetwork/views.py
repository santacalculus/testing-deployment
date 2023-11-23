from django.shortcuts import render, redirect, reverse, get_object_or_404

# Create your views here.
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm, EntryForm, PostForm, ProfileForm
from socialnetwork.models import Profile, Post, Comment
import json
from django.views.decorators.csrf import ensure_csrf_cookie


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect('global')

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    
    new_profile = Profile(user = new_user, user_bio="")
    

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    new_user.save()
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('global'))

"""@login_required
def global_action(request) :
    context = {}
    if request.method == 'GET' :
        return render(request, 'socialnetwork/global.html', context)"""

@login_required
def follower_action(request) :
    if request.method == "GET" :
        return render(request, 'socialnetwork/follower.html', {'posts': Post.objects.all().order_by('-date_time')})

"""@login_required
def myprofile_action(request) :
    context = {}
    if request.method == 'GET' :
        return render(request, 'socialnetwork/myprofile.html', context)

@login_required
def otherprofile_action(request) :
    context = {}
    if request.method == 'GET' :
        return render(request, 'socialnetwork/otherprofile.html', context)"""

@login_required   
def myprofile_action(request) :
    
    if request.method == 'GET' :
        context = {'profile': request.user.profile, 
                   'form': ProfileForm(initial={'user_bio': request.user.profile.user_bio})}
        return render(request, 'socialnetwork/myprofile.html', context)

    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid() :
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'socialnetwork/myprofile.html', context)
    
    profile = request.user.profile
    profile.picture = form.cleaned_data['picture']
    profile.content_type = form.cleaned_data['picture'].content_type
    profile.user_bio = form.cleaned_data['user_bio']
    profile.save()
    print(profile.picture)
    return redirect(reverse('myprofile'))




@login_required
def global_action(request) :
    context = {}
    user = request.user
    context['posts'] = Post.objects.all().order_by('-date_time')
    context['profile'] = user.profile
    if request.method == "GET" :
        return render(request, 'socialnetwork/global.html', context)
    
    if 'text' not in request.POST or not request.POST['text'] :
        context['error'] = 'You cannot post nothing.'
        return render(request, 'socialnetwork/global.html', context)
    new_post = Post(text=request.POST['text'], user=request.user, date_time=timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/global.html', context)


def get_list_json_dumps_serializer(request):
    if not request.user.id :
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    post_list = []
    for model_item in Post.objects.all():
        my_item = {
            'id': model_item.id,
            'text': model_item.text,
            'date_time': model_item.date_time.isoformat(),
            'user_id': model_item.user.id,
            
        }
        post_list.append(my_item)
    
    comment_list = []
    for model_item in Comment.objects.all():
        my_item = {
            'id': model_item.id,
            'text': model_item.text,
            'creator': model_item.creator.id,
            'creation_time': model_item.creation_time.isoformat(),
            'wait_time': model_item.post.id,
            
        }
        comment_list.append(my_item)

    response_data = {}
    response_data['posts'] = post_list
    response_data['comments'] = comment_list
    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')

@login_required
def get_followerlist_json_dumps_serializer(request):
    if not request.user.id :
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    post_list = []
    for model_item in Post.objects.all():
        if model_item.user in request.user.profile.follow.all() and model_item.user != request.user:
            my_item = {
                'id': model_item.id,
                'text': model_item.text,
                'date_time': model_item.date_time.isoformat(),
                'user_id': model_item.user.id,
                'user_first': model_item.user.first_name,
                'user_last': model_item.user.last_name
            }
            post_list.append(my_item)
    comment_list = []
    for model_item in Comment.objects.all():
        if model_item.post.user in request.user.profile.follow.all() and model_item.post.user != request.user : #checking whether the user who made the post is in the list of those you are following
            my_item = {
                'id': model_item.id,
                'text': model_item.text,
                'creator': model_item.creator.id,
                'creation_time': model_item.creation_time.isoformat(),
                'post_id': model_item.post.id,
                'creator_first': model_item.creator.first_name,
                'creator_last': model_item.creator.last_name
            }
            comment_list.append(my_item)
    response_data = {}
    response_data['posts'] = post_list
    response_data['comments'] = comment_list
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def otherprofile_action(request, id) :
    user = get_object_or_404(User, id=id)
    if user == request.user :
        return myprofile_action(request)
    if request.method == "POST" :
        if "unfollow" in request.POST :
            unfollow_action(request, user)
        if "follow" in request.POST :
            follow_action(request, user)
        return render(request, 'socialnetwork/otherprofile.html', {'profile': user.profile})
    if request.method == "GET" :
        return render(request, 'socialnetwork/otherprofile.html', {'profile': user.profile})

@login_required
def unfollow_action(request, user) :
    request.user.profile.follow.remove(user)
    request.user.profile.save()
    


@login_required
def follow_action(request, user) :
    request.user.profile.follow.add(user)
    request.user.profile.save()

@login_required
def getphoto_action(request, id):
    user = get_object_or_404(Profile, id=id)
    if not user:
        raise Http404
    print('Picture #{} fetched from db: {} (type={})'.format(id, user.picture, type(user.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.

    return HttpResponse(user.picture, content_type=user.content_type)



def add_comment(request) :
    if not request.user.id :
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text'] or not 'post_id' in request.POST or not request.POST['post_id'] or not request.POST['post_id'].isnumeric():
        return _my_json_error_response("You must enter a comment to add.", status=400)
    
    post_count = 0
    for posts in Post.objects.all():
        post_count += 1
    if int(request.POST['post_id']) <= 0 or int(request.POST['post_id']) > post_count :
        return _my_json_error_response("You must enter a comment to add.", status=400)

    new_comment = Comment(text=request.POST['comment_text'], creator=request.user, creation_time=timezone.now(), post=Post.objects.get(id=request.POST['post_id']))
    new_comment.save()

    return get_list_json_dumps_serializer(request)


def follower_add_comment(request) :
    if not request.user.id :
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text'] or not 'post_id' in request.POST or not request.POST['post_id'] or not request.POST['post_id'].isnumeric():
        return _my_json_error_response("You must enter a comment to add.", status=400)

    post_count = 0
    for posts in Post.objects.all():
        post_count += 1
    if int(request.POST['post_id']) <= 0 or int(request.POST['post_id']) > post_count :
        return _my_json_error_response("You must enter a comment to add.", status=400)
        
    new_comment = Comment(text=request.POST['comment_text'], creator=request.user, creation_time=timezone.now(), post=Post.objects.get(id=request.POST['post_id']))
    new_comment.save()

    return get_followerlist_json_dumps_serializer(request)

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)
