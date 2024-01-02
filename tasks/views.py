from django.db.models import F
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Photo
from .forms import TaskForm

# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = ['Low', 'Medium', 'High']
        return context
    
    def get_queryset(self):
        queryset = Task.objects.all().order_by(F('priority').desc())
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        creation_date = self.request.GET.get('creation_date')
        if creation_date:
            queryset = queryset.filter(
                creation_date_date = creation_date
            )
        due_date = self.request.GET.get('due_date')
        if due_date:
            queryset = queryset.filter(
                due_date__date=due_date
            )

        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(
                priority=priority
            )

        is_complete = self.request.GET.get('is_complete')
        if is_complete == '1':
            queryset = queryset.filter(is_complete=True)
        elif is_complete == '0':
            queryset = queryset.filter(is_complete=False)

        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')