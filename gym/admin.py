from django.contrib import admin
from .models import (
    Entrenador, Miembro, TipoMembresia, Membresia,
    ClaseGrupal, Inscripcion, Pago, Asistencia,
)

admin.site.site_header = "Pulso · Panel de administración"
admin.site.site_title = "Pulso admin"
admin.site.index_title = "Gestión del gimnasio"


class MembresiaInline(admin.TabularInline):
    model = Membresia
    extra = 0
    autocomplete_fields = ["tipo"]


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0
    fields = ("monto", "metodo", "membresia")


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    autocomplete_fields = ["miembro"]


@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "dni", "estado", "fecha_inscripcion")
    list_display_links = ("nombre", "apellido")
    list_editable = ("estado",)
    list_filter = ("estado",)
    search_fields = ("nombre", "apellido", "dni")
    date_hierarchy = "fecha_inscripcion"
    readonly_fields = ("fecha_inscripcion",)
    fieldsets = (
        ("Datos personales", {
            "fields": ("nombre", "apellido", "dni", "fecha_nacimiento", "foto"),
        }),
        ("Contacto", {
            "fields": ("email", "telefono"),
        }),
        ("Estado en el gimnasio", {
            "fields": ("estado", "fecha_inscripcion"),
        }),
    )
    inlines = [MembresiaInline, PagoInline]


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "especialidad", "telefono")
    search_fields = ("nombre", "apellido")


@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_dias")
    search_fields = ("nombre",)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ("miembro", "tipo", "fecha_inicio", "fecha_fin", "activa")
    list_editable = ("activa",)
    list_filter = ("activa", "tipo")
    search_fields = ("miembro__nombre", "miembro__apellido", "tipo__nombre")
    autocomplete_fields = ["miembro", "tipo"]


@admin.register(ClaseGrupal)
class ClaseGrupalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "entrenador", "dia", "hora_inicio", "hora_fin", "cupo_maximo")
    list_editable = ("cupo_maximo",)
    list_filter = ("dia",)
    search_fields = ("nombre",)
    autocomplete_fields = ["entrenador"]
    inlines = [InscripcionInline]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("miembro", "clase", "fecha_inscripcion")
    autocomplete_fields = ["miembro", "clase"]


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("miembro", "monto", "metodo", "fecha_pago")
    list_filter = ("metodo",)
    date_hierarchy = "fecha_pago"
    autocomplete_fields = ["miembro", "membresia"]


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("miembro", "fecha", "hora_entrada")
    list_filter = ("fecha",)
    autocomplete_fields = ["miembro"]