import datetime
from django.core.management.base import BaseCommand
from gym.models import (
    Entrenador, Miembro, TipoMembresia, Membresia,
    ClaseGrupal, Inscripcion, Pago,
)


class Command(BaseCommand):
    help = "Carga datos de ejemplo para el gimnasio"

    def handle(self, *args, **options):
        Entrenador.objects.all().delete()
        Miembro.objects.all().delete()
        TipoMembresia.objects.all().delete()

        e1 = Entrenador.objects.create(nombre="Lucas", apellido="Fernandez", especialidad="Musculación", telefono="351-1111111")
        e2 = Entrenador.objects.create(nombre="Sofia", apellido="Gomez", especialidad="Yoga y pilates", telefono="351-2222222")
        e3 = Entrenador.objects.create(nombre="Martin", apellido="Diaz", especialidad="Crossfit", telefono="351-3333333")

        mensual = TipoMembresia.objects.create(nombre="Mensual", precio=15000, duracion_dias=30)
        trimestral = TipoMembresia.objects.create(nombre="Trimestral", precio=40000, duracion_dias=90)
        anual = TipoMembresia.objects.create(nombre="Anual", precio=140000, duracion_dias=365)

        m1 = Miembro.objects.create(nombre="Juan", apellido="Perez", dni="30111222", email="juan@mail.com", estado="activo")
        m2 = Miembro.objects.create(nombre="Ana", apellido="Lopez", dni="30333444", email="ana@mail.com", estado="activo")
        m3 = Miembro.objects.create(nombre="Carlos", apellido="Ramirez", dni="30555666", email="carlos@mail.com", estado="inactivo")

        hoy = datetime.date.today()
        Membresia.objects.create(miembro=m1, tipo=mensual, fecha_inicio=hoy, fecha_fin=hoy + datetime.timedelta(days=30))
        Membresia.objects.create(miembro=m2, tipo=trimestral, fecha_inicio=hoy, fecha_fin=hoy + datetime.timedelta(days=90))

        Pago.objects.create(miembro=m1, monto=15000, metodo="efectivo")
        Pago.objects.create(miembro=m2, monto=40000, metodo="tarjeta")

        c1 = ClaseGrupal.objects.create(nombre="Spinning", entrenador=e1, dia="lunes", hora_inicio="18:00", hora_fin="19:00", cupo_maximo=15)
        c2 = ClaseGrupal.objects.create(nombre="Yoga", entrenador=e2, dia="martes", hora_inicio="09:00", hora_fin="10:00", cupo_maximo=10)
        c3 = ClaseGrupal.objects.create(nombre="Crossfit", entrenador=e3, dia="miercoles", hora_inicio="19:00", hora_fin="20:00", cupo_maximo=12)

        Inscripcion.objects.create(miembro=m1, clase=c1)
        Inscripcion.objects.create(miembro=m2, clase=c2)

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados correctamente."))