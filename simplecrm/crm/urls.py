from django.urls import path
from . import views
from .views import login_view, register_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path("register/", register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('customers/<int:pk>/add-interaction/', views.add_interaction, name='add-interaction'),
]