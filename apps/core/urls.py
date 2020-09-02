from django.urls import path
from .views import Home, Dashboard, DetailBarbecue, CreateBarbecue, RegisterUser, DetailInvitation, CancelParticipation

app_name = 'core'

urlpatterns = [

    path('', Home.as_view(), name='home'),
    path('churrascos/<str:username>/', Dashboard.as_view(), name='dashboard'),
    path('convites/<str:username>/<int:id_churras>/', DetailBarbecue.as_view(), name='detail'),
    path('meu-convite/<str:username>/<int:id_invict>/', DetailInvitation.as_view(), name='detail_inviction'),
    path('meu-churrasco/<str:username>/', CreateBarbecue.as_view(), name='create'),
    
    path('cancelar-participação/<int:id_invict>/', CancelParticipation.as_view(), name='cancel_participation'),
    
    path('novo-usuario/', RegisterUser.as_view(), name='register'),


]
