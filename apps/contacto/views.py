from django.shortcuts import render
from .forms import ContactoForm
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.


class ContactoUsuario(CreateView):
    template_name = 'contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Consulta enviada.')
        return super().form_valid(form)

        


# def contacto(request):
#     data = {'form': ContactoForm()}

#     if request.method == 'POST':
#         formulario = ContactoForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             messages.success(request, 'Consulta enviada')
#         else:
#             data['form'] = formulario
    
#     return render(request, 'contacto.html', data)

    # if request.method == 'POST':
    #     form = ContactoForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         asunto = 'Confirmación de contacto'
    #         mensaje = 'Gracias por contactarnos. Hemos recibido tu mensaje correctamente.'
    #         desde_email = 'tu_correo@example.com'
    #         mail_contacto = [form.cleaned_data['email']]  # El destinatario es la dirección de correo electrónico ingresada en el formulario

    #         send_mail(asunto, mensaje, desde_email, mail_contacto)
    #         return render(request, 'mensaje_enviado.html')
    #     else:
    #         form = ContactoForm()

    # return render(request, 'contacto.html', {'form': form})