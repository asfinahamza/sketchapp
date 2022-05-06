from django.urls import path, include, re_path
from sketchapp import views
urlpatterns = [

    #Auth Urls
    path('signin/', views.signin.as_view(),name="signin"),
    path('signinpg', views.signinpg.as_view(),name="signinpg"),
    path('logout/', views.logoutpg.as_view(),name="logout"),
    

    #main urls#####

    #user
    path('', views.index.as_view(),name="home"),
    path('about/', views.about.as_view(),name="about"),
    path('contact/', views.contact.as_view()),
    path('<int:id>/Profile/', views.Profile.as_view()),
    path('ProfilePage/', views.ProfilePage.as_view()),
    path('blogs/', views.blogs.as_view()),
    path('<int:id>/blogDetail/', views.blogDetail.as_view()),

    #admin
    path('dashboard/', views.dashboard.as_view(),name="dashboard"),
    path('UserList/', views.UserList.as_view()),
    path('<int:id>/AddBlog/', views.AddBlog.as_view()),
    path('BlogList/', views.BlogList.as_view()),
    path('ViewContacts/', views.ViewContacts.as_view()),
    

    #post urls
    path('<int:id>/PostBlog', views.PostBlog.as_view()),
    path('PostMessage', views.PostMessage.as_view()),
    path('<int:id>/PostProfile', views.PostProfile.as_view()),

    #list view urls
    path('BlogListView', views.BlogListView.as_view()),
    path('MessageListView', views.MessageListView.as_view()),

    #filter api urls
    path('<int:id>/BlogDetailAPIView/', views.BlogDetailAPIView.as_view()),
    path('<int:id>/userDetailAPIView/', views.userDetailAPIView.as_view()),
    path('<int:id>/MessageAPIView/', views.MessageAPIView.as_view()),


    #delete
    path('<int:id>/DeleteBlog', views.DeleteBlog.as_view()),
    path('<int:id>/DeleteProfile', views.DeleteProfile.as_view()),
    path('<int:id>/DeleteMessage', views.DeleteMessage.as_view()),
]