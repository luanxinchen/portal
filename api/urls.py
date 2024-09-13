from rest_framework.routers import DefaultRouter
from api.views import login
from api.views.portal import site,contact,notify,users

router = DefaultRouter()
router.register('login', login.LoginViewSet, 'login')
router.register('site', site.SiteViewSet, 'site')
router.register('site_category', site.SiteCateGoryViewSet, 'site_category')
router.register('contact', contact.ContactViewSet, 'contact')
router.register('contact_category', contact.ContactCateGoryViewSet, 'contact_category')
router.register('notify', notify.NotificationViewSet, 'notify')
router.register('users', users.UserViewSet, 'users')

urlpatterns = [
]
urlpatterns += router.urls