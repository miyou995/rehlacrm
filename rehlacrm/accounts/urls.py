from django.urls import path
from .views import SignupView, SignupsuccessView
from django.contrib.auth import views as auth_views
from .froms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from .views import UserView, UserUpdateView, UserListView, UserAddView,UserChangeView, add_user, change_password
app_name= 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name="signup"),
    path('signup_success/', SignupsuccessView.as_view(), name="signup_success"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html",form_class=AuthenticationForm,),name="login",),
    path('logout/' , auth_views.LogoutView.as_view(), name= 'logout' ),
    path('userdetail', login_required(UserView.as_view()), name="userdetail"),
    path('edituser/<int:pk>/', login_required(UserUpdateView.as_view()), name="edituser"),
    path('userlist/', login_required(UserListView.as_view()), name="userlist"),
    path('useradd/', login_required(add_user), name="useradd"),
    path('changeuser/<int:pk>/', login_required(UserChangeView.as_view()), name="changeuser"),
    path('change_password/<int:pk>/', login_required(change_password), name="change_password"),
]




