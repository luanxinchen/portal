from rest_framework.routers import DefaultRouter
from api.views import login

router = DefaultRouter()
router.register('login', login.LoginViewSet, 'login')


urlpatterns = [
]
urlpatterns += router.urls