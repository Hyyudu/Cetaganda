# coding: utf-8

from django.conf.urls import *

from roles import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cabinet$', views.CabinetView.as_view(), name='cabinet'),
    url(r'^roles/new$', views.CreateGameView.as_view(), name='new_game'),
    url(r'^roles/(?P<pk>\d+)$', views.GameView.as_view(), name='game'),
    url(r'^roles/(?P<pk>\d+)/edit$', views.EditGameView.as_view(), name='edit_game'),
    url(r'^roles/(?P<pk>\d+)/fields$', views.GameFieldsView.as_view(), name='edit_game_fields'),
    url(r'^roles/(?P<pk>\d+)/groups$', views.GameGroupsView.as_view(), name='edit_game_groups'),
    url(r'^roles/(?P<pk>\d+)/topics$', views.GameTopicsView.as_view(), name='edit_game_topics'),
    url(r'^roles/(?P<pk>\d+)/new_free_role$', views.CreateFreeRoleView.as_view(), name='new_free_role'),
    url(r'^roles/(?P<pk>\d+)/new_role$', views.CreateRoleView.as_view(), name='new_role'),
    url(r'^roles/(?P<pk>\d+)/reports/connections_table$', views.ReportConnectionsTable.as_view(),
        name='report_connections_table'),
    url(r'^roles/(?P<pk>\d+)/reports/connections_diagram$', views.ReportConnectionsDiagram.as_view(),
        name='report_connections_diagram'),
    url(r'^roles/(?P<pk>\d+)/reports/connections_diagram.json$', views.ReportConnectionsData.as_view(),
        name='report_connections_json'),
    url(r'^roles/(?P<pk>\d+)/reports/full_roles$', views.ReportFullRolesData.as_view(), name='report_full_roles'),
    url(r'^roles/(?P<pk>\d+)/reports/dual_connections$', views.ReportDualConnections.as_view(),
        name='report_dual_connections'),
    url(r'^roles/(?P<pk>\d+)$', views.RoleView.as_view(), name='role'),
    url(r'^roles/(?P<pk>\d+)/edit$', views.EditRoleView.as_view(), name='edit_role'),
    url(r'^roles/(?P<pk>\d+)/delete', views.DeleteRoleView.as_view(), name='delete_role'),
    url(r'^roles/(?P<pk>\d+)/connections$', views.EditConnectionsView.as_view(), name='edit_role_connections'),
    url(r'^roles/(?P<pk>\d+)/new_connection$', views.AddConnectionView.as_view(), name='add_connection'),
    url(r'^registration', views.RegistrationView.as_view(), name='registration'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
)
