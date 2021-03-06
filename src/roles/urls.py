from __future__ import unicode_literals

from django.conf.urls import url

from roles import views

urlpatterns = [
    url(r'^choose$', views.ChooseRoleView.as_view(), name='choose'),
    url(r'^request$', views.CreateRoleView.as_view(), name='request'),
    url(r'^(?P<pk>\d+)/reports/connections_table$', views.ReportConnectionsTable.as_view(),
        name='report_connections_table'),
    url(r'^(?P<pk>\d+)/reports/connections_diagram$', views.ReportConnectionsDiagram.as_view(),
        name='report_connections_diagram'),
    url(r'^(?P<pk>\d+)/reports/connections_diagram.json$', views.ReportConnectionsData.as_view(),
        name='report_connections_json'),
    url(r'^(?P<pk>\d+)/reports/full_roles$', views.ReportFullRolesData.as_view(), name='report_full_roles'),
    url(r'^(?P<pk>\d+)/reports/dual_connections$', views.ReportDualConnections.as_view(),
        name='report_dual_connections'),
    url(r'^(?P<pk>\d+)$', views.RoleView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/edit$', views.EditRoleView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete', views.DeleteRoleView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/connections$', views.EditConnectionsView.as_view(), name='edit_connections'),
    url(r'^(?P<pk>\d+)/new_connection$', views.AddConnectionView.as_view(), name='add_connection'),
    url(r'^$', views.RolesView.as_view(), name='all'),
]
