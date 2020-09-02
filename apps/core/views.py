from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from .models import Person, HammerBarbecue, Invitation
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime,date



class Home(TemplateView):
    template_name = "home.html"

    def post(self,request, *args, **kwargs):
        current_user = request.POST.get('username', None)
        
        try:
            Person.objects.get(username=current_user)
            return redirect('core:dashboard', username = current_user)
        except:
            return redirect('core:home')
    


class RegisterUser(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        name_in_request = self.request.POST.get('name')
        username_in_request = self.request.POST.get('username')
        person = Person.objects.create(
            name = name_in_request,
            username = username_in_request,
        )
        
        return reverse('core:dashboard', kwargs={'username': person.username})



class Dashboard(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        user = self.kwargs['username']

        context['news'] = Invitation.objects.filter(
                                participant__username=user,
                                barbecue__date__gte=date.today()
                            ).exclude(
                                    barbecue__host__username=user
                                ).order_by('-id')

        context['alls'] = Invitation.objects.filter(participant__username=user, presence=True , barbecue__date__lt=date.today()).order_by('-id')
        context['created_me'] = HammerBarbecue.objects.filter(host__username=user).order_by('-id')
        context['current_user'] = user

        return context
    


class DetailBarbecue(TemplateView):
    template_name = "my_barbecue.html"

    def get_context_data(self, **kwargs):
        context = super(DetailBarbecue, self).get_context_data(**kwargs)
        churras_id = self.kwargs['id_churras']
        churras = HammerBarbecue.objects.get(pk=churras_id)
        invitations = Invitation.objects.filter(barbecue=churras_id)
        
        current_date = date.today()
        
        value_contribution = 0
        for invitation in invitations:
            value_contribution+=invitation.contribution
        

        context['guests'] = invitations
        context['churras'] = churras
        context['total_spent'] = churras.spent_drinks + churras.spent_foods 
        context['contributions'] = value_contribution
        
        status = "em aberto"
        if churras.date < current_date:
            status = "fechado"

        context['status'] = status
        
        return context



class DetailInvitation(TemplateView):
    template_name =  "my_ invitation.html"

    def get_context_data(self, **kwargs):
        context = super(DetailInvitation, self).get_context_data(**kwargs)
        id_invict = self.kwargs['id_invict']
        invict = Invitation.objects.get(pk=id_invict)

        context['invict'] = invict
        context['guests'] = invitations = Invitation.objects.filter(barbecue=invict.barbecue , presence=True)
        
        current_date = date.today()
        status = "em aberto"
        if invict.barbecue.date < current_date:
            status = "fechado"

        context['status'] = status


        return context

    def post(self,request, *args, **kwargs):
        user = self.kwargs['username']

        id_invict = self.kwargs['id_invict']
        name = request.POST.get('guest_name', None)
        value = request.POST.get('value_contribute', None)
        consumes_alcohol = request.POST.get('consumes_alcohol', None)

        invitation = Invitation.objects.get(pk=id_invict)
        invitation.guest = name
        invitation.contribution = value
        invitation.presence = True

        if consumes_alcohol == "on":
            invitation.consumes_alcohol = True
        else:
            invitation.consumes_alcohol = False

        invitation.save()

    
        return redirect('core:dashboard', username = user)



class CreateBarbecue(TemplateView):
    template_name = "create.html"


    def get_context_data(self, **kwargs):
        context = super(CreateBarbecue, self).get_context_data(**kwargs)
        user = self.kwargs['username']

        context['persons'] = Person.objects.all().exclude(username=user)
        context['current_user'] = user

        return context

    def post(self,request, *args, **kwargs):
        location = request.POST.get('location')
        date = request.POST.get('date')
        spent_drinks = request.POST.get('spent_drinks')
        spent_foods = request.POST.get('spent_foods')
        guests_list = request.POST.get('guests').split(',')

        churras = HammerBarbecue.objects.create(
            host=Person.objects.get(username=self.kwargs['username']),
            location = location,
            date = date,
            spent_drinks = spent_drinks,
            spent_foods=spent_foods
        )

        for guest in guests_list:
            invitation_sended = Invitation.objects.create(
                participant=Person.objects.get(pk=guest), 
                barbecue=churras
            )
            

        return redirect('core:dashboard', username = self.kwargs['username'])



class CancelParticipation(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # name_in_request = self.request.POST.get('name')
        cancel = self.request.POST.get('cancel')
        invict = Invitation.objects.get(pk=self.kwargs['id_invict'])


        if cancel == "minha":
            invict.presence = False
            invict.guest = ""
            invict.contribution = 20
        
        else:
            invict.guest = ""
            if invict.consumes_alcohol:
                invict.contribution = 20
            else:
                invict.contribution = 10

        invict.save()
        
        return reverse('core:detail_inviction', kwargs={
            'username': invict.participant.username, 
            'id_invict':invict.id
        })
