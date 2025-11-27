from django.urls import path


from .views import RegisterView, LoginView, LogoutView, CookieTokenRefreshView, UserView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="refresh"),
    path("user/", UserView.as_view(), name="user-detail"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
