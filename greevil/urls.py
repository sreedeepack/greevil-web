from django.conf.urls import url
import greevil.views
from django.views.generic import TemplateView
from django.urls import path



urlpatterns = [
    url(r'^$', greevil.views.start, name='sb_admin_start'),
    path('register/', TemplateView.as_view(
        template_name="greevil/register.html"),
        name='sb_admin_register'
    ),
    path('register/confirm/', TemplateView.as_view(
        template_name="greevil/confirm.html"),
        name='sb_admin_confirm'
    ),
    path('forgot_password/', TemplateView.as_view(
        template_name="greevil/forgot_password.html"),
        name='sb_admin_forgot_password'
    ),
    path('404/', TemplateView.as_view(
        template_name="greevil/sb_admin_404.html"),
        name='sb_admin_404'
    ),
    url(r'^login/$', greevil.views.login, name='sb_admin_login'),
    url(r'^dashboard/$', greevil.views.dashboard, name='sb_admin_dashboard'),
    # url("register/confirm/success", greevil.views.login, name='sb_admin_login_after_confirm'),
    url(r'^charts/$', greevil.views.charts, name='sb_admin_charts'),
    url(r'^tables/$', greevil.views.tables, name='sb_admin_tables'),
    url(r'^forms/$', greevil.views.forms, name='sb_admin_forms'),
    url(r'^bootstrap-elements/$', greevil.views.bootstrap_elements, name='sb_admin_bootstrap_elements'),
    url(r'^bootstrap-grid/$', greevil.views.bootstrap_grid, name='sb_admin_bootstrap_grid'),
    url(r'^rtl-dashboard/$', greevil.views.rtl_dashboard, name='sb_admin_rtl_dashboard'),
    url(r'^blank/$', greevil.views.blank, name='sb_admin_blank'),
]