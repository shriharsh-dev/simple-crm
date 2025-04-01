from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Customer, Interaction
from django.contrib.auth.models import User
from .forms import CustomerForm, InteractionForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid credentials, try again.")
            return redirect('login')

    return render(request, 'crm/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'crm/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'crm/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Get the logged-in user

        # Only fetch data that belongs to the current user
        context["total_customers"] = Customer.objects.filter(user=user).count()
        context['active_customers'] = Customer.objects.filter(user=user, status='active').count()
        context['leads'] = Customer.objects.filter(user=user, status='lead').count()
        context['recent_interactions'] = Interaction.objects.filter(user=user).order_by('-date')[:5]
        
        return context
    
class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('customer-list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)  # Restrict update access

    def get_success_url(self):
        return reverse_lazy('customer-detail', kwargs={'pk': self.object.pk})

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    template_name = 'crm/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)  # Restrict delete access

class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = 'crm/customer_detail.html'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)  # Restrict access

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = self.object.interactions.order_by('-date')
        context['interaction_form'] = InteractionForm(initial={'customer': self.object})
        return context


def add_interaction(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    # Ensure customer belongs to logged-in user
    if customer.user != request.user:
        messages.error(request, "You are not allowed to modify this customer's data.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.customer = customer
            interaction.user = request.user  # Ensure interaction belongs to user
            interaction.save()
            return redirect('customer-detail', pk=customer.pk)
    
    return redirect('customer-detail', pk=customer.pk)
