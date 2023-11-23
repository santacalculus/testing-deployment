from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_action, name='global'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('socialnetwork/get-global', views.get_list_json_dumps_serializer, name='get-global'),
    path('socialnetwork/get-follower', views.get_followerlist_json_dumps_serializer, name='get-follower'),
    path('socialnetwork/add-comment', views.add_comment, name='add-comment'),
    path('follower-add-comment', views.follower_add_comment, name='follower-add-comment'),
    path('global/<int:id>', views.global_action, name='global'),
    path('follower', views.follower_action, name='follower'),
    path('myprofile', views.myprofile_action, name='myprofile'),
    path('otherprofile/<int:id>', views.otherprofile_action, name='otherprofile'),
    path('unfollow/<int:id>', views.otherprofile_action, name='unfollow'),
    path('follow/<int:id>', views.otherprofile_action, name='follow'),
    path('photo/<int:id>', views.getphoto_action, name='photo'),
]