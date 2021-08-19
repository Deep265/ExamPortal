from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('about/',views.About.as_view(),name='about'),
    path('',views.PostListView.as_view(),name='post_list'),
    path('drafts/',views.DraftListView.as_view(),name='drafts'),
    path('new/',views.PostCreateView,name='new_post'),
    path('detail/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('update/<int:pk>/',views.PostUpdateView.as_view(),name='post_update'),
    path('detail/<int:pk>/comment/',views.add_comments,name='add_comment'),
    path('publish/<int:pk>/',views.publish,name='publish'),
    path('detail/<int:pk>/comment/delete/',views.DeleteComment,name='delete_comment'),
    path('detail/<int:pk>/approve/',views.approve_comment,name='approve_comment'),
    path('detail/<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete'),
]