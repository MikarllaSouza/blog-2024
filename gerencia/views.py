from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, NoticiaFilterForm, NoticiaForm
from .models import Categoria, Noticia


# Create your views here.
@login_required(login_url='usuarios:login')
def inicio_gerencia(request):
    return render(request, 'gerencia/inicio.html')

def listagem_noticia(request):
    formularioFiltro = NoticiaFilterForm(request.GET or None)
    
    noticias = Noticia.objects.filter(usuario=request.user)  # Filtra pelo usuário logado

    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['titulo']:
            noticias = noticias.filter(titulo__icontains=formularioFiltro.cleaned_data['titulo'])
        if formularioFiltro.cleaned_data['data_publicacao_inicio']:
            noticias = noticias.filter(data_publicacao__gte=formularioFiltro.cleaned_data['data_publicacao_inicio'])
        if formularioFiltro.cleaned_data['data_publicacao_fim']:
            noticias = noticias.filter(data_publicacao__lte=formularioFiltro.cleaned_data['data_publicacao_fim'])
        if formularioFiltro.cleaned_data['categoria']:
            noticias = noticias.filter(categoria=formularioFiltro.cleaned_data['categoria'])
    
    contexto = {
        'noticias': noticias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_noticia.html',contexto)


def cadastrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Cria instância sem salvar
            noticia.usuario = request.user  # Atribui o autor (usuário logado)
            noticia.save()  # Salva a notícia no banco
            return redirect('gerencia:listagem_noticia')  # Redireciona para página de sucesso
    else:
        form = NoticiaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_noticia.html', contexto)

@login_required(login_url='usuarios:login')
def editar_noticia(request, id):
    noticia = Noticia.objects.get(id=id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia_editada = form.save(commit=False)  # Não salva ainda
            noticia_editada.usuario = request.user 
            noticia_editada.save()  # Salva com o usuário intacto
            return redirect('gerencia:listagem_noticia')
    else:
        form = NoticiaForm(instance=noticia)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_noticia.html',contexto)




def index(request):
    categoria_nome = request.GET.get('categoria')  # Obtém o parâmetro 'categoria' da URL
    search_query = request.GET.get('search')  # Obtém o parâmetro de busca

    # Filtra as notícias com base na categoria ou na busca
    noticias = Noticia.objects.all()
    if categoria_nome:
        categoria = Categoria.objects.filter(nome=categoria_nome).first()
        if categoria:
            noticias = noticias.filter(categoria=categoria)

    if search_query:
        noticias = noticias.filter(titulo__icontains=search_query)  # Filtra por título, ignorando maiúsculas/minúsculas

    categorias = Categoria.objects.all()  # Pega todas as categorias para exibir no template

    contexto = {
        'noticias': noticias,
        'categorias': categorias,
        'categoria_selecionada': categoria_nome,
        'search_query': search_query,
    }
    return render(request, 'gerencia/index.html', contexto)

@login_required(login_url='usuarios:login')
def categoria_list(request):
    search_term = request.GET.get('search', '')
    qs = Categoria.objects.all()
    
    if search_term:
        qs = qs.filter(nome__icontains=search_term)
    
    qs = qs.annotate(nome_lower=Lower('nome')).order_by('nome_lower')

    paginator = Paginator(qs, 10)  # Paginação
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    
    context = {
        'categorias': categorias,
        'action': request.get_full_path(),
    }
    return render(request, 'gerencia/categoria_list.html', context)


@login_required(login_url='usuarios:login')
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia:categoria_list')
    else:
        form = CategoriaForm()

    return render(request, 'gerencia/categoria_form.html', {'form': form})


@login_required(login_url='usuarios:login')
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('gerencia:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'gerencia/categoria_form.html', {'form': form})


@login_required(login_url='usuarios:login')
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('gerencia:categoria_list')

    return render(request, 'gerencia/categoria_confirm_delete.html', {'categoria': categoria})