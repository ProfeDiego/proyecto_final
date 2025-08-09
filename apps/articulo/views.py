from .models import Articulo,  Categoria
from apps.comentario.models import Comentario
from .forms import ArticuloForm, NuevaCategoriaForm
from apps.comentario.forms import ComentarioForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

#Todos los artículos
class ArticuloListView(ListView):
    model = Articulo
    template_name = "articulo/articulos.html" 
    context_object_name = "articulos" 

    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha_publicacion')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha_publicacion')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context


#Artículo individual
class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = "articulo/post.html" 
    success_url = 'articulos'
    context_object_name = "articulos" 
    pk_url_kwarg = "id" 
    queryset = Articulo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(articulo_id=self.kwargs['id'])
        return context

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            messages.success(self.request, 'Comentario creado con éxito.')
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.articulo_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.articulo:articulo_detalle', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


#Artículo creación
class ArticuloCreateView(LoginRequiredMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulo/articulo_form.html'

    def get_success_url(self):
            messages.success(self.request, '¡Artículo creado con éxito!')
            return reverse_lazy('apps.articulo:articulos')


#Artículo modificación
class ArticuloUpdateView(LoginRequiredMixin, UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulo/articulo_form.html'

    def get_success_url(self):
            messages.success(self.request, '¡Artículo modificado con éxito!')
            return reverse_lazy('apps.articulo:articulos')


#Articulo borrar
class ArticuloDeleteView(DeleteView):
    model = Articulo
    template_name = 'articulo/articulo_eliminar.html'

    def get_success_url(self):
        messages.success(self.request, '¡Borrado con éxito!')
        return reverse_lazy('apps.articulo:articulos')

class ArticuloPorCategoriaView(ListView):
    model = Articulo
    template_name = 'articulo/articulos_por_categoria.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        return Articulo.objects.filter(categoria_id=self.kwargs['pk'])
    
#Categorías
class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'articulo/crear_categoria.html'

    def get_success_url(self):
        messages.success(self.request, '¡Categoría creada con éxito!')
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.articulo:articulo_crear')

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'articulo/categoria_lista.html'
    context_object_name = 'categorias'

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'articulo/categoria_eliminar.html'
    success_url = reverse_lazy('apps.articulo:categoria_lista')




# class ArticuloView(View):
#     template_name = 'articulos/articulo.html'

#     def get(self, request, categoria=None, orden=None, fecha=None):
#         orden = request.GET.get('orden')
#         fecha = request.GET.get('fecha')
#         print('fecha:', fecha)
        
#         if categoria:
#             articulos = Articulo.objects.filter(categoria__nombre=categoria)
#         else:
#             articulos = Articulo.objects.all()
            
#         if orden == 'ascendente':
#             articulos = articulos.order_by('titulo')
#         elif orden == 'descendente':
#             articulos = articulos.order_by('-titulo')
        
#         if fecha:
#             articulos = articulos.filter(fecha_publicacion__date=fecha)
            
#         categorias = Categoria.objects.all()
        
#         return render(request, 'articulos/articulo.html', {'articulos' : articulos, 'categorias': categorias})



# def existe_articulo(id):
#     for i in Articulo:
#         if i.id == id:
#             return i
#     return None


# def leer_articulo(request, id):
# 	try:
# 		articulos = existe_articulo(id)
# 	except Exception:
# 		articulos  = Articulo.objects.get(id = id)
# 		comentarios = Comentario.objects.filter(articulo=id)

# 	form = ComentarioForm(request.POST or None)
# 	if form.is_valid():
# 		print(f"Form is valid: {form.is_valid()}")
# 		if not form.is_valid():
# 			print(form.errors)
# 		if request.user.is_authenticated:
# 			aux         =  form.save(commit=False)
# 			aux.articulo = articulos
# 			aux.usuario = request.user
# 			aux.save()
# 			form        = ComentarioForm()

# 		else:
			
# 			return redirect('usuario:login')
            
# 	context = {
		
# 		'articulos': articulos,
# 		'form': form,
# 		'comentarios': comentarios,
# 	}
# 	return render(request,'articulos/post.html', context)


# def articulo_crear(request):
#     if request.method == 'POST':
#         form = ArticuloForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(f'Form is valid: {form.is_valid()}')
#             form.save()
#             return redirect('articulos')
#     else:
#         form = ArticuloForm()
#     return render(request, 'articulos/articulo_form.html', {'form': form})

# def articulo_actualizar(request, pk):
#     articulo = get_object_or_404(Articulo, pk=pk)
#     if request.method == 'POST':
#         form = ArticuloForm(request.POST, request.FILES, instance=articulo)
#         if form.is_valid():
#             form.save()
#             return redirect('articulos')
#     else:
#         form = ArticuloForm(instance=articulo)
#     return render(request, 'articulos/articulo_form.html', {'form': form})