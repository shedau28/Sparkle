from ast import Pass


from django.urls import path
from .views import *

urlpatterns = [
    path("", login_page, name='login_page'),
    path("login_page/", login_page, name='login_page'),
    path("login/", login, name='login'),
    path("logout_page/", logout_page, name='logout_page'),
    path("register_page/", register_page, name='register_page'),
    path("register/", register, name='register'),
    path("profile_page/", profile_page, name='profile_page'),
    path("update_data/", update_data, name='update_data'),
    path("upload_image/", upload_image, name='upload_image'),



    path("index/", index, name='index'),
    path("service_page/", service_page, name='service_page'),
    path("service_detail_view/<int:pk>", ServiceDetailView.as_view(), name='service_detail_view'),
    path("add_to_cart/", add_to_cart, name='add_to_cart'),


    path("index_paytm/", index_paytm, name='index_paytm'),
        # payment
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),

]