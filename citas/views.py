from django.shortcuts import render, get_object_or_404
from .models import Paciente, Cita


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