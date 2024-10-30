from django.shortcuts import render,redirect
from .models import Noticia
from .forms import NoticiaForm

# Create your views here.
def index(request):
    noticias = Noticia.objects.all()
    contexto={
        'noticias': noticias
    }
    return render(request, 'noticia/index.html',contexto)

def pre_cadastro_noticia(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('noticias') # procura uma rota com name 'noticias'
    else:
        form = NoticiaForm()

def cadastrar_noticias(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save() 
            return redirect('cadastro_sucesso')  
    else:
        form = NoticiaForm()

    contexto = {
        'form': form
    }
    return render(request, 'noticia/cadastrar_noticia.html', contexto)

