from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Paciente, Cita
from .forms import PacienteForm, CitaForm


def inicio(request):
    return render(request, 'citas/inicio.html')


def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'citas/lista_pacientes.html', {'pacientes': pacientes})


def detalle_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    citas = Cita.objects.filter(paciente=paciente)
    return render(request, 'citas/detalle_paciente.html', {
        'paciente': paciente,
        'citas': citas,
    })


def lista_citas(request):
    citas = Cita.objects.select_related('paciente').order_by('fecha', 'hora')
    return render(request, 'citas/lista_citas.html', {'citas': citas})


def citas_pendientes(request):
    citas = Cita.objects.select_related('paciente').filter(estado='Pendiente').order_by('fecha', 'hora')
    return render(request, 'citas/citas_pendientes.html', {'citas': citas})

def nuevo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente registrado correctamente.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'citas/formulario.html', {
        'form': form,
        'titulo': 'Registrar paciente',
        'volver': 'lista_pacientes',
    })


def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'citas/formulario.html', {
        'form': form,
        'titulo': 'Editar paciente',
        'volver': 'lista_pacientes',
    })


def nueva_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita médica registrada correctamente.')
            return redirect('lista_citas')
        for error in form.non_field_errors():
            messages.error(request, error)
    else:
        form = CitaForm()
    return render(request, 'citas/formulario.html', {
        'form': form,
        'titulo': 'Programar cita',
        'volver': 'lista_citas',
    })


def editar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita médica actualizada correctamente.')
            return redirect('lista_citas')
        for error in form.non_field_errors():
            messages.error(request, error)
    else:
        form = CitaForm(instance=cita)
    return render(request, 'citas/formulario.html', {
        'form': form,
        'titulo': 'Editar cita',
        'volver': 'lista_citas',
    })


@require_POST
def cancelar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.estado = 'Cancelada'
    cita.save()
    messages.success(request, 'La cita ha sido cancelada correctamente.')
    return redirect('lista_citas')


@require_POST
def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    messages.success(request, 'La cita ha sido eliminada correctamente.')
    return redirect('lista_citas')