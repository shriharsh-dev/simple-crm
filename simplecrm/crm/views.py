from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Customer, Interaction
from .forms import CustomerForm, InteractionForm

# Create your views here.
class DashboardView(generic.TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_customers"] = Customer.objects.count()
        context['active_customers'] = Customer.objects.filter(status='active').count()
        context['leads']=Customer.objects.filter(status='lead').count()
        context['recent_interactions']=Interaction.objects.order_by('-date')[:5]
        return context
    
class CustomerCreateView(generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('customer-list')

class CustomerUpdateView(generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'

    def get_success_url(self):
        return reverse_lazy('customer-detail', kwargs={'pk':self.object.pk})
    
class CustomerDeleteView(generic.DeleteView):
    model = Customer
    template_name = 'crm/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

    def add_interaction(request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.method == 'POST':
            form = InteractionForm(request.POST)
            if form.is_valid():
                interaction = form.save(commit=False)
                interaction.customer = customer
                interaction.save()
                return redirect('customer-detail', pk=customer.pk)
            
        return redirect('customer-detail',pk=customer.pk)