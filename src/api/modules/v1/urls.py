from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny

router = SimpleRouter()

app_name = 'v1'


schema_view = get_schema_view(
    title='API Schema, Socrates 2.0 😜', 
    version='v1.0',
    permission_classes = [AllowAny]
)

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('schema/', schema_view),
    path('', include(router.urls))

    
]
