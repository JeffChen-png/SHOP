from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^profile/$', views.profilepage, name='profile'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    url(r'^password-change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    url(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]