from django.urls import path
from . import views

app_name = 'hungry'

urlpatterns = [
    path('', views.index, name='index'),
    path('page/register/', views.register_user_page, name='user-register'),
    path('user/register/', views.add_new_user, name='register'),
    path('user/registered/', views.registered, name='registered'),
    path('user/logout/', views.logout_user, name='logout-user'),
    path('login/page/', views.login_page, name='login-page'),
    path('login/user/', views.login_user, name='login-user'),
    path('user/settings/', views.user_settings, name='user-settings'),
    path('places/', views.PlaceListView.as_view(), name='places-list'),
    path('place/<int:place_id>/', views.place_detail, name='place-detail'),
    path('goods/filter/', views.filter, name='goods-filter'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('good/<int:pk>/', views.GoodDetailView.as_view(), name='good-detail'),
    path('place/userphotos/<int:place_id>/', views.userphotos, name='userphotos'),
    path('visited/add/<int:place_id>/', views.add_or_remove_place_to_visited, name='visited'),
    path('place/menu/edit_page/<int:place_id>/', views.menu_edit_page, name='menu-edit-page'),
    path('place/menu/edit/<int:place_id>/', views.menu_edit, name='menu-edit'),
    path('place/menu/add/<int:place_id>/', views.menu_add, name='menu-add'),
    path('good/rate/<int:good_id>', views.add_good_rating, name='rate-good'),
    path('place/new/add', views.add_new_place, name='place-add'),
    path('place/comment/add/<int:place_id>', views.add_comment, name='comment-add'),
    path('user/detail/<int:pk>/', views.user_detail, name='user-detail'),
    path('user/settings/save/', views.user_settings_apply, name='user-apply'),
    path('place/userphoto/add/<int:place_id>', views.place_photo_add, name='photo-add'),
    # API
    path('api/place/list/', views.PlaceListAPIView.as_view(), name='api-place-list'),
    path('api/good/list/', views.GoodListAPIView.as_view(), name='api-good-list'),
]
