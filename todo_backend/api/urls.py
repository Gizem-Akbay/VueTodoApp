from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api.views import LabelView,TodoView, UserCreate

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('newuser/', UserCreate, name="new_user"),
    path('labels/', LabelView, name='labels'),
    path('labels/todo/<int:todo_id>/', LabelView, name='todo'),
    path('todos/', TodoView, name='todos'),
    path('todos/shared-to-me/', TodoView, name='shared_todos'),
    path('todos/<int:todo_id>/', TodoView, name="todo"),
    path('todos/<int:todo_id>/users/', TodoView, name="users")
]
