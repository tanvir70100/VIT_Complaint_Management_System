from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lodge/', views.lodge_complaint, name='lodge_complaint'),
    path('active/', views.active_complaints, name='active_complaints'),
    path('previous/', views.previous_complaints, name='previous_complaints'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:complaint_id>/edit/', views.edit_complaint, name='edit_complaint'),
]