from datetime import date

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Goal, SavingsConfig, SavingsEntry, Opportunity, MONTH_CHOICES

DEFAULT_GOALS = [
    dict(name="Concours Ingénieur Informaticien – Génie Logiciel", when_label="Dès maintenant",
         objective="Préparer la prochaine session sérieusement.", start_month=0, end_month=9,
         deadline_month=6, deadline_label="Prépa intensive", color="#3E6E63", order=1),
    dict(name="UNA", when_label="Maintenant → déc. 2026",
         objective="Laisser une vraie chance à la liste d'attente.", start_month=0, end_month=3,
         deadline_month=3, deadline_label="Point de décision", color="#B9852F", order=2),
    dict(name="INP-HB", when_label="Léger maintenant, actif après la fenêtre UNA",
         objective="Construire le projet doctoral et trouver un directeur.", start_month=3, end_month=9,
         deadline_month=5, deadline_label="Préinscription", color="#5B7FBF", order=3),
    dict(name="Kômian", when_label="Maintenant",
         objective="Attendre le retour sans en dépendre.", start_month=0, end_month=1,
         deadline_month=1, deadline_label="Retour attendu", color="#8A6FBF", order=4),
    dict(name="Plan professionnel B", when_label="Dès maintenant",
         objective="Trouver une activité si Kômian n'aboutit pas.", start_month=1, end_month=9,
         deadline_month=None, deadline_label="", color="#C1685A", order=5),
    dict(name="Gabon 2027", when_label="Dès maintenant",
         objective="Préparer le voyage financièrement et logistiquement.", start_month=0, end_month=11,
         deadline_month=10, deadline_label="Départ", color="#4FA391", order=6),
]


def _seed_goals_if_empty():
    if not Goal.objects.exists():
        for g in DEFAULT_GOALS:
            Goal.objects.create(**g)


# ---------- Auth ----------

def login_view(request):
    if request.session.get("authenticated"):
        return redirect("dashboard")
    error = None
    if request.method == "POST":
        pwd = request.POST.get("password", "")
        if pwd == settings.APP_PASSWORD:
            request.session["authenticated"] = True
            return redirect("dashboard")
        error = "Mot de passe incorrect."
    return render(request, "tracker/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("login")


# ---------- Chantiers (dashboard) ----------

def dashboard_view(request):
    _seed_goals_if_empty()
    if request.method == "POST":
        if "add_goal" in request.POST:
            Goal.objects.create(
                name=request.POST.get("name", "").strip() or "Nouvel objectif",
                when_label=request.POST.get("when_label", "").strip(),
                objective=request.POST.get("objective", "").strip(),
                start_month=int(request.POST.get("start_month", 0)),
                end_month=int(request.POST.get("end_month", 1)),
                order=Goal.objects.count() + 1,
            )
            messages.success(request, "Objectif ajouté.")
        return redirect("dashboard")

    goals = Goal.objects.all()
    return render(request, "tracker/dashboard.html", {"goals": goals, "months": MONTH_CHOICES, "active": "dash"})


def cycle_status(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    goal.status = goal.next_status()
    goal.save()
    return redirect(request.META.get("HTTP_REFERER", reverse("dashboard")))


def update_period(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if request.method == "POST":
        goal.start_month = int(request.POST.get("start_month", goal.start_month))
        goal.end_month = int(request.POST.get("end_month", goal.end_month))
        if goal.start_month > goal.end_month:
            goal.start_month, goal.end_month = goal.end_month, goal.start_month
        goal.save()
    return redirect(request.META.get("HTTP_REFERER", reverse("dashboard")))


def delete_goal(request, pk):
    Goal.objects.filter(pk=pk).delete()
    return redirect(request.META.get("HTTP_REFERER", reverse("dashboard")))


# ---------- Feuille de route ----------

def roadmap_view(request):
    _seed_goals_if_empty()
    goals = Goal.objects.all()
    return render(request, "tracker/roadmap.html", {"goals": goals, "months": MONTH_CHOICES, "active": "road"})


# ---------- Épargne Gabon ----------

def savings_view(request):
    config = SavingsConfig.load()
    if request.method == "POST":
        if "save_config" in request.POST:
            config.target_amount = int(request.POST.get("target_amount") or 0)
            target_date = request.POST.get("target_date")
            config.target_date = target_date or None
            config.save()
        elif "add_entry" in request.POST:
            amount = int(request.POST.get("amount") or 0)
            if amount > 0:
                SavingsEntry.objects.create(
                    amount=amount, note=request.POST.get("note", "").strip()
                )
        return redirect("savings")

    entries = SavingsEntry.objects.all()
    total = sum(e.amount for e in entries)
    remaining = max(0, config.target_amount - total)
    pct = min(100, round(total / config.target_amount * 100)) if config.target_amount else 0

    months_left, monthly_needed = None, None
    if config.target_date:
        today = date.today()
        months_left = max(
            1,
            (config.target_date.year - today.year) * 12 + (config.target_date.month - today.month),
        )
        monthly_needed = -(-remaining // months_left)  # arrondi supérieur

    return render(request, "tracker/savings.html", {
        "config": config, "entries": entries, "total": total,
        "remaining": remaining, "pct": pct,
        "months_left": months_left, "monthly_needed": monthly_needed,
        "active": "save",
    })


def delete_entry(request, pk):
    SavingsEntry.objects.filter(pk=pk).delete()
    return redirect("savings")


# ---------- Opportunités ----------

SEARCH_LINKS = [
    ("Stages informatique Abidjan", "stage informatique Abidjan"),
    ("Emploi IA Côte d'Ivoire", "recrutement intelligence artificielle Côte d'Ivoire"),
    ("Réseaux / IoT Abidjan", "emploi réseaux informatique IoT Abidjan"),
    ("Concours fonction publique CI", "avis concours fonction publique Côte d'Ivoire 2027"),
]


def opportunities_view(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            Opportunity.objects.create(
                title=title,
                url=request.POST.get("url", "").strip(),
                note=request.POST.get("note", "").strip(),
            )
        return redirect("opportunities")

    opportunities = Opportunity.objects.all()
    return render(request, "tracker/opportunities.html", {
        "opportunities": opportunities, "search_links": SEARCH_LINKS, "active": "opp",
    })


def delete_opportunity(request, pk):
    Opportunity.objects.filter(pk=pk).delete()
    return redirect("opportunities")
