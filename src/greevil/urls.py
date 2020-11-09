import greevil.views
from django.conf.urls import url

urlpatterns = [

    url(r'^$', greevil.views.dashboard, name='sb_admin_start'),
    # path('register/', TemplateView.as_view(
    #      template_name="greevil/register.html"),
    #      'sb_admin_register',
    #      ),
    # path('register/confirm/', TemplateView.as_view(
    #     template_name="greevil/confirm.html"),
    #      name='sb_admin_confirm'
    #      ),
    url(r'^register/$', greevil.views.register, name='sb_admin_register'),
    url(r'^register/confirm/$', greevil.views.register_confirm, name='sb_admin_confirm'),
    url(r'^login/$', greevil.views.login, name='sb_admin_login'),
    url(r'^dashboard/$', greevil.views.dashboard, name='sb_admin_dashboard'),
    url(r'^start/$', greevil.views.start, name='start'),
    url(r'^add_friend/$', greevil.views.add_friend, name='add_friend'),
    url(r'^add_expense/$', greevil.views.add_expense, name='add_expense'),
    url(r'delete_expense/$', greevil.views.delete_expense, name='delete_expense'),

    url(r'^charts/$', greevil.views.charts, name='sb_admin_charts'),
    url(r'^tables/$', greevil.views.tables, name='sb_admin_tables'),
    url(r'^forms/$', greevil.views.forms, name='sb_admin_forms'),
    url(r'^bootstrap-elements/$', greevil.views.bootstrap_elements, name='sb_admin_bootstrap_elements'),
    url(r'^bootstrap-grid/$', greevil.views.bootstrap_grid, name='sb_admin_bootstrap_grid'),
    url(r'^rtl-dashboard/$', greevil.views.rtl_dashboard, name='sb_admin_rtl_dashboard'),
    url(r'^add/$', greevil.views.add, name='sb_admin_add'),
    url(r'^add/expense/$', greevil.views.add_expense_view, name='sb_admin_add_exp'),

    url(r"^forgot/$", greevil.views.forgot_view, name='sb_admin_forgot_password'),
    url(r"^forgot/confirm/$", greevil.views.forgot_confirm_view, name='sb_admin_forgot_confirm'),

    # path('forgot/', TemplateView.as_view(
    #     template_name="greevil/forgot_password.html"),
    #      name='sb_admin_forgot_password'
    #      ),
    # path('forgot/confirm/', TemplateView.as_view(
    #     template_name="greevil/forgot_confirm.html"),
    #      name='sb_admin_forgot_confirm'
    #      ),
]
