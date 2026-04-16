# from django.contrib import admin
# from django.urls import path
# from .views import home_view,  topic_selection_view, chat_view , set_language_view
# from django.urls import path, include
# from .views import home_view,  topic_selection_view, chat_view, chat_api
# from .views import home_view, path_selection_view, module_selection_view, topic_selection_view, chat_view, chat_api, set_language_view


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('allauth.urls')), # This adds login/logout/social routes
# # --- Add this to your urlpatterns ---
#     path('set-language/', set_language_view, name='set_language'),
#     path('', home_view, name='home'),
#     # path('start/', learning_options_view, name='learning_options'),
#     # Step 1: Select a Learning Path (e.g., Computer vs Programming)
#     path('start/', path_selection_view, name='path_selection'),
    
#     # Step 2: Select a Module within that Path (e.g., Excel, Basics)
#     path('courses/<str:path_slug>/', module_selection_view, name='module_selection'),

#     # Step 3: Module Cover Page (Start Learning Button)
#     path('learn/<str:module_slug>/', topic_selection_view, name='topic_selection'),
    
    
# # Changed from 'path' to 'module_slug'
#     path('learn/<str:module_slug>/', topic_selection_view, name='topic_selection'),
#     path('chat/', chat_view, name='chat'),
#     # Update the chat URLs
#     path('chat/', chat_view, name='chat'), # General chat
#     path('chat/<int:topic_id>/', chat_view, name='chat_topic'), # Chat about a specific topic
#     path('api/chat/', chat_api, name='chat_api'), # The AJAX endpoint
# ]



from django.contrib import admin
from django.urls import path, include
# Import the new views we created. Note: 'learning_options_view' is removed.
from .views import (
    home_view, 
    path_selection_view, 
    module_selection_view, 
    topic_selection_view, 
    chat_view, 
    chat_api, 
    dashboard_view,
    set_language_view,
    about_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # Step 1: Select a Learning Path (e.g., Computer vs Programming)
    # Replaces the old 'learning_options' route
    path('start/', path_selection_view, name='path_selection'),
    
    # Step 2: Select a Module within that Path (e.g., Excel, Basics)
    path('courses/<str:path_slug>/', module_selection_view, name='module_selection'),
    
    # Step 3: Module Cover Page (Start Learning Button)
    path('learn/<str:module_slug>/', topic_selection_view, name='topic_selection'),
    
    path('chat/', chat_view, name='chat'),
    path('chat/<int:topic_id>/', chat_view, name='chat_topic'),
    path('api/chat/', chat_api, name='chat_api'),
    path('set-language/', set_language_view, name='set_language'),
    path('about/', about_view, name='about'),
]