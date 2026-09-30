from django import forms
from .models import Miembro, Pago, Membresia, Inscripcion


class StyledFormMixin:
    """Le agrega clases de estilo a cada campo automáticamente."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            elif isinstance(widget, (forms.FileInput, forms.ClearableFileInput)):
                pass  # se estiliza aparte como avatar circular
            else:
                widget.attrs.setdefault("class", "form-control")


class MiembroForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ["nombre", "apellido", "dni", "email", "telefono", "fecha_nacimiento", "estado", "foto"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "foto": forms.FileInput(),
        }


class PagoForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["miembro", "membresia", "monto", "metodo"]


class MembresiaForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ["miembro", "tipo", "fecha_inicio", "fecha_fin", "activa"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class InscripcionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["miembro", "clase"]