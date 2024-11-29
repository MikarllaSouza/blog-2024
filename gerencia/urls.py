from django.urls import path

from . import views

app_name = 'gerencia'

urlpatterns = [
    path('', views.inicio_gerencia, name='gerencia_inicial'),
    path('noticias/', views.listagem_noticia, name='listagem_noticia'),
    path('noticias/cadastro', views.cadastrar_noticia, name='cadastro_noticia'),
    path('noticias/editar/<int:id>', views.editar_noticia, name='editar_noticia'),
    # Add your URL patterns here
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categoria/criar/', views.categoria_create, name='categoria_create'),
    path('categoria/editar/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('categoria/excluir/<int:pk>/', views.categoria_delete, name='categoria_delete'),
]