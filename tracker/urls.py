from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("", views.dashboard_view, name="dashboard"),
    path("goal/<int:pk>/cycle/", views.cycle_status, name="cycle_status"),
    path("goal/<int:pk>/period/", views.update_period, name="update_period"),
    path("goal/<int:pk>/delete/", views.delete_goal, name="delete_goal"),

    path("feuille-de-route/", views.roadmap_view, name="roadmap"),

    path("epargne/", views.savings_view, name="savings"),
    path("epargne/entry/<int:pk>/delete/", views.delete_entry, name="delete_entry"),

    path("opportunites/", views.opportunities_view, name="opportunities"),
    path("opportunites/<int:pk>/delete/", views.delete_opportunity, name="delete_opportunity"),
]
