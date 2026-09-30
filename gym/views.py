from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone

from .models import (
    Miembro, Entrenador, ClaseGrupal, Membresia, Pago, Asistencia, Inscripcion
)
from .forms import MiembroForm, PagoForm, MembresiaForm, InscripcionForm


def dashboard(request):
    contexto = {
        "total_miembros": Miembro.objects.count(),
        "miembros_activos": Miembro.objects.filter(estado="activo").count(),
        "total_entrenadores": Entrenador.objects.count(),
        "total_clases": ClaseGrupal.objects.count(),
        "ingresos_totales": Pago.objects.aggregate(total=Sum("monto"))["total"] or 0,
        "asistencias_hoy": Asistencia.objects.filter(fecha=timezone.now().date()).count(),
        "proximas_clases": ClaseGrupal.objects.select_related("entrenador").order_by("dia", "hora_inicio")[:5],
    }
    return render(request, "gym/dashboard.html", contexto)


# ---------- Miembros ----------

def miembro_list(request):
    query = request.GET.get("q", "")
    miembros = Miembro.objects.all()
    if query:
        miembros = miembros.filter(nombre__icontains=query) | miembros.filter(apellido__icontains=query)
    return render(request, "gym/miembro_list.html", {"miembros": miembros, "query": query})


def miembro_detail(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    return render(request, "gym/miembro_detail.html", {"miembro": miembro})


def miembro_create(request):
    if request.method == "POST":
        form = MiembroForm(request.POST, request.FILES)
        if form.is_valid():
            miembro = form.save()
            messages.success(request, "Miembro creado correctamente.")
            return redirect("gym:miembro_detail", pk=miembro.pk)
    else:
        form = MiembroForm()
    return render(request, "gym/miembro_form.html", {"form": form, "titulo": "Nuevo miembro"})


def miembro_update(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == "POST":
        form = MiembroForm(request.POST, request.FILES, instance=miembro)
        if form.is_valid():
            form.save()
            messages.success(request, "Miembro actualizado.")
            return redirect("gym:miembro_detail", pk=miembro.pk)
    else:
        form = MiembroForm(instance=miembro)
    return render(request, "gym/miembro_form.html", {"form": form, "titulo": "Editar miembro"})


def miembro_delete(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == "POST":
        miembro.delete()
        messages.success(request, "Miembro eliminado.")
        return redirect("gym:miembro_list")
    return render(request, "gym/miembro_confirm_delete.html", {"miembro": miembro})


def marcar_asistencia(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    Asistencia.objects.create(miembro=miembro)
    messages.success(request, f"Asistencia registrada para {miembro}.")
    return redirect("gym:miembro_detail", pk=miembro.pk)


# ---------- Entrenadores ----------

def entrenador_list(request):
    entrenadores = Entrenador.objects.annotate(cantidad_clases=Count("clases"))
    return render(request, "gym/entrenador_list.html", {"entrenadores": entrenadores})


# ---------- Clases ----------

def clase_list(request):
    clases = ClaseGrupal.objects.select_related("entrenador").annotate(inscriptos=Count("inscripciones"))
    return render(request, "gym/clase_list.html", {"clases": clases})


def clase_detail(request, pk):
    clase = get_object_or_404(ClaseGrupal, pk=pk)
    inscripciones = clase.inscripciones.select_related("miembro")
    return render(request, "gym/clase_detail.html", {"clase": clase, "inscripciones": inscripciones})


def inscripcion_create(request):
    if request.method == "POST":
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscripción realizada.")
            return redirect("gym:clase_list")
    else:
        form = InscripcionForm()
    return render(request, "gym/inscripcion_form.html", {"form": form})


# ---------- Membresias ----------

def membresia_list(request):
    membresias = Membresia.objects.select_related("miembro", "tipo").order_by("-fecha_inicio")
    return render(request, "gym/membresia_list.html", {"membresias": membresias})


def membresia_create(request):
    if request.method == "POST":
        form = MembresiaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membresía creada.")
            return redirect("gym:membresia_list")
    else:
        form = MembresiaForm()
    return render(request, "gym/membresia_form.html", {"form": form})


# ---------- Pagos ----------

def pago_list(request):
    pagos = Pago.objects.select_related("miembro").order_by("-fecha_pago")
    return render(request, "gym/pago_list.html", {"pagos": pagos})


def pago_create(request):
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago registrado.")
            return redirect("gym:pago_list")
    else:
        form = PagoForm()
    return render(request, "gym/pago_form.html", {"form": form})