from datetime import date, time
from django import forms
from .models import Paciente, Cita

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'edad', 'telefono', 'correo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()
        if len(apellido) < 3:
            raise forms.ValidationError("El apellido debe tener al menos 3 caracteres.")
        return apellido

    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad < 1 or edad > 120:
            raise forms.ValidationError("La edad debe estar entre 1 y 120 años.")
        return edad

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        if not telefono.isdigit() or len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos numéricos.")
        return telefono

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'fecha', 'hora', 'motivo', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'hora': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise forms.ValidationError("No se pueden registrar citas en fechas anteriores a hoy.")
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data['hora']
        if hora < time(8, 0) or hora > time(18, 0):
            raise forms.ValidationError("Las citas solo pueden ser entre las 8:00 y las 18:00 horas.")
        return hora

    def clean_motivo(self):
        motivo = self.cleaned_data['motivo'].strip()
        if len(motivo) < 10:
            raise forms.ValidationError("El motivo debe tener al menos 10 caracteres.")
        return motivo

    def clean(self):
        datos = super().clean()
        fecha = datos.get('fecha')
        hora = datos.get('hora')
        estado = datos.get('estado')

        # Solo revisamos choques si la cita que se guarda quedará activa
        if fecha and hora and estado in ('Pendiente', 'Confirmada'):
            ocupadas = Cita.objects.filter(
                fecha=fecha,
                hora=hora,
                estado__in=['Pendiente', 'Confirmada'],
            ).exclude(pk=self.instance.pk)

            if ocupadas.exists():
                raise forms.ValidationError(
                    "No es posible registrar la cita: el horario seleccionado ya está ocupado."
                )
        return datos