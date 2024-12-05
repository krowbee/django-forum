from django.urls import path
from . import views


urlpatterns = [
     path('', views.HomepageView.as_view(), name='homepage'),
     path('accounts/profile/', views.ProfileView.as_view(), name='my-profile'),
     path('accounts/profile/create_profile/', views.CreateProfileView.as_view(), name='create-profile'),
     path('accounts/profile/update_profile/', views.UpdateProfileView.as_view(), name='update-profile'),
     path('accounts/profile/<int:profile_id>', views.ProfileView.as_view(), name='user-profile'),
     path('<slug:category_slug>/', views.CategoryTopicsView.as_view(), name='category-topics'),
     path('<slug:category_slug>/<slug:subcategory_slug>/', views.SubcategoryTopicsView.as_view(), name='subcategory-topics'),
     path('<slug:category_slug>/<slug:subcategory_slug>/create_topic/', views.CreateTopicView.as_view(), name='create-topic'),
     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/', views.TopicView.as_view(), name='topic'),
     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/create_post/',
          views.CreatePostView.as_view(), name='create-post'),

     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/<int:post_id>/create_comment/',
          views.CreateCommentView.as_view(), name='create-comment'),

     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/delete_topic/',
          views.DeleteTopicView.as_view(), name='delete-topic'),

     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/<int:post_id>/delete_post/',
          views.DeletePostView.as_view(), name='delete-post'),

     path('<slug:category_slug>/<slug:subcategory_slug>/<int:topic_id>/<int:post_id>/<int:comment_id>/delete_comment',
          views.DeleteCommentView.as_view(), name='delete-comment'),
]
