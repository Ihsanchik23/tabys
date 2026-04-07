from django.urls import path
from .views import (
    home_view,
    jobs_view,
    order_detail_view,
    register_view,
    login_view,
    logout_view,
    create_order_view,
    edit_profile_view,
    profile_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('jobs/', jobs_view, name='jobs'),
    path('jobs/<int:order_id>/', order_detail_view, name='order_detail'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('create-order/', create_order_view, name='create_order'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('profile/', profile_view, name='profile'),
]