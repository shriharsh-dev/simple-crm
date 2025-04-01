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

class CustomerListView(generic.ListView):
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'

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

class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'crm/customer_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all interactions for this customer, ordered by most recent first
        context['interactions'] = self.object.interactions.order_by('-date')
        # Create an empty interaction form with the current customer pre-selected
        context['interaction_form'] = InteractionForm(initial={'customer': self.object})
        return context

def add_interaction(request, pk):
    # Get the customer or return 404 if not found
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            # Create interaction but don't save to database yet
            interaction = form.save(commit=False)
            # Set the customer for this interaction
            interaction.customer = customer
            # Now save to database
            interaction.save()
            # Redirect back to customer detail page
            return redirect('customer-detail', pk=customer.pk)
    
    # If form not valid or not a POST request, just redirect back to customer detail
    return redirect('customer-detail', pk=customer.pk)