from django.urls import path
from . import views

app_name = "gym"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("miembros/", views.miembro_list, name="miembro_list"),
    path("miembros/nuevo/", views.miembro_create, name="miembro_create"),
    path("miembros/<int:pk>/", views.miembro_detail, name="miembro_detail"),
    path("miembros/<int:pk>/editar/", views.miembro_update, name="miembro_update"),
    path("miembros/<int:pk>/eliminar/", views.miembro_delete, name="miembro_delete"),
    path("miembros/<int:pk>/asistencia/", views.marcar_asistencia, name="marcar_asistencia"),

    path("entrenadores/", views.entrenador_list, name="entrenador_list"),

    path("clases/", views.clase_list, name="clase_list"),
    path("clases/<int:pk>/", views.clase_detail, name="clase_detail"),
    path("inscripciones/nueva/", views.inscripcion_create, name="inscripcion_create"),

    path("membresias/", views.membresia_list, name="membresia_list"),
    path("membresias/nueva/", views.membresia_create, name="membresia_create"),

    path("pagos/", views.pago_list, name="pago_list"),
    path("pagos/nuevo/", views.pago_create, name="pago_create"),
]