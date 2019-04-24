
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView)
from django.template.loader import render_to_string
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.http import JsonResponse
from django.contrib import messages
from main.todo.forms import TodoForm
from main.todo.models import Todo
from main.todo.task import inline_task_checker


# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

def todo_list(request):
    todos_list = Todo.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(todos_list, 10)
    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)
    return render(request, 'todo.html', {'todos': todos})


def save_todo_form(request, form, template_name, messages=None):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            todos = Todo.objects.all()
            data['html_todo_list'] = render_to_string('includes/partial_todo_list.html', {
                'todos': todos,
                'msgs': messages
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        return save_todo_form(
            request, 
            form,
            'includes/partial_todo_create.html',
            # messages.success(request, ('Item has been added to list'))
        )
    else:
        form = TodoForm()
        return save_todo_form(
            request, 
            form, 
            'includes/partial_todo_create.html',
        )


def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk) 
    inline_task_checker(pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        return save_todo_form(
            request,
            form,
            'includes/partial_todo_update.html',
            # messages.success(request, ('Item has been updated to list'))
        )
    else:
        form = TodoForm(instance=todo)
        return save_todo_form(
            request, 
            form, 
            'includes/partial_todo_update.html'
        )


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    data = dict()
    if request.method == 'POST':
        todo.delete()
        data['form_is_valid'] = True
        todos = Todo.objects.all()
        data['html_todo_list'] = render_to_string('includes/partial_todo_list.html', {
            'todos': todos
        })
    else:
        context = {'todo': todo}
        data['html_form'] = render_to_string(
            'includes/partial_todo_delete.html', context, request=request)
    return JsonResponse(data)


