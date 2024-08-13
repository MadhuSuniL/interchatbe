from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView, UserSearchView, SimilarBioUsersView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Explore Users
    path('search', UserSearchView.as_view(), name = 'users_search'),
    path('similar-bio-search', SimilarBioUsersView.as_view(), name = 'similar-bio-search'),
    # path('search', UserSearchView.as_view(), name = ' users_search'),
]
