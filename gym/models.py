from django.db import models
from django.urls import reverse


class Entrenador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_contratacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Miembro(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
        ("suspendido", "Suspendido"),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="activo")
    foto = models.ImageField(upload_to="miembros/", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse("gym:miembro_detail", args=[self.pk])


class TipoMembresia(models.Model):
    nombre = models.CharField(max_length=50)  # Mensual, Trimestral, Anual
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_dias = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"


class Membresia(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name="membresias")
    tipo = models.ForeignKey(TipoMembresia, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.miembro} - {self.tipo.nombre}"


class ClaseGrupal(models.Model):
    DIA_CHOICES = [
        ("lunes", "Lunes"), ("martes", "Martes"), ("miercoles", "Miércoles"),
        ("jueves", "Jueves"), ("viernes", "Viernes"), ("sabado", "Sábado"), ("domingo", "Domingo"),
    ]
    nombre = models.CharField(max_length=100)  # Spinning, Yoga, Crossfit...
    entrenador = models.ForeignKey(Entrenador, on_delete=models.SET_NULL, null=True, related_name="clases")
    dia = models.CharField(max_length=15, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupo_maximo = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.nombre} - {self.get_dia_display()} {self.hora_inicio}"


class Inscripcion(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name="inscripciones")
    clase = models.ForeignKey(ClaseGrupal, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("miembro", "clase")

    def __str__(self):
        return f"{self.miembro} -> {self.clase}"


class Pago(models.Model):
    METODO_CHOICES = [
        ("efectivo", "Efectivo"), ("tarjeta", "Tarjeta"), ("transferencia", "Transferencia"),
    ]
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name="pagos")
    membresia = models.ForeignKey(Membresia, on_delete=models.SET_NULL, null=True, blank=True, related_name="pagos")
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default="efectivo")

    def __str__(self):
        return f"Pago de {self.miembro} - ${self.monto}"


class Asistencia(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name="asistencias")
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.miembro} - {self.fecha}"