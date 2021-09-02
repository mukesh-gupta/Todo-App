from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Todo
from .Forms import TodoForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.utils.timezone import datetime


# Create your views here.
def home(request):
    users=User.objects.all().exclude(is_superuser=True)
    todos= Todo.objects.values('user').annotate(title=Count('title'))
    return render(request,'App/home.html',{'todos':todos,'users':users})

@login_required(login_url='login')
def index(request):
    user=request.user
    if user.is_authenticated:
        todos=Todo.objects.filter(user=request.user,datecompleted__isnull=True)

    return render(request,'App/index.html',{'todos':todos})


@login_required(login_url='login')
def create(request):
    user=request.user
    if user.is_authenticated:
        if request.method=="POST":
            form = TodoForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                try:
                    todoForm=form.save(commit=False)
                    todoForm.user=request.user
                    todoForm.save()
                    messages.info(request, ' Added 1 Item in list !')
                    return redirect('list')
                except ValueError:
                    messages.warning(request, 'Anonymous User')
                    return render(request, 'App/create.html', {'forms': form})

            else:
                messages.warning(request,'invalid Form  data')
                return render(request, 'App/create.html', {'forms': form})

        else:
            form = TodoForm()
            return render(request, 'App/create.html', {'forms': form})





@login_required(login_url='login')
def TodoList(request):
    user=request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request, 'App/list.html', {'todos': todos})




@login_required(login_url='login')
def TodoDetail(request,pk):
    user = request.user
    if user.is_authenticated:
        todo=get_object_or_404(Todo,pk=pk,user=request.user)
    return render(request,'App/detail.html',{'todo':todo})


@login_required(login_url='login')
def TodoUpdate(request,pk):
    user = request.user
    if user.is_authenticated:
        todo = get_object_or_404(Todo, pk=pk,user=request.user)
        form=TodoForm(request.POST or None, request.FILES or None,instance=todo)
        if request.method=="POST":
            if form.is_valid():
                form.save()
                messages.info(request, "List 1 item  Updated !")
                return redirect('list')

        else:
            return render(request,'App/update.html',{'form':form})



@login_required(login_url='login')
def TodoDelete(request,pk):
    user = request.user
    if user.is_authenticated:
        todo=get_object_or_404(Todo,pk=pk,user=request.user)
        if request.method=="POST":
            todo.delete()
            messages.info(request, "1 item Deleted !")
            return redirect('list')
        else:
            return render(request,'App/delete.html',{'todo':todo})


@login_required(login_url='login')
def TodoComp(request):
    user = request.user
    if user.is_authenticated:
        todos=Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'App/complete.html',{'todos':todos})



@login_required(login_url='login')
def TodoCopmpleted(request, pk):
    user = request.user
    if user.is_authenticated:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'POST':
            todo.datecompleted = timezone.now()
            todo.save()
            messages.info(request, "List 1 item Completed !")
            return redirect('list')
        else:
            return render(request, 'App/completed.html', {'todo': todo})




@login_required(login_url='login')
def todo_pdf(request, pk):
    user = request.user
    todo = get_object_or_404(Todo, pk=pk)
    template_path = 'App/pdf_generator.html'
    date = datetime.now()
    context = {
        'todo': todo,
        'date':date,
        'users':user
    }
    response = HttpResponse(content_type='application/pdf')
    filename = f'Todo-{todo.title.capitalize()}-{date}.pdf'
    response['content-Disposition'] = 'filename=%s' % filename
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('page not found')
    return response



































