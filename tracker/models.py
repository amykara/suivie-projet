from django.db import models

MONTH_CHOICES = [
    (0, "Sept 26"), (1, "Oct 26"), (2, "Nov 26"), (3, "Déc 26"),
    (4, "Jan 27"), (5, "Fév 27"), (6, "Mars 27"), (7, "Avr 27"),
    (8, "Mai 27"), (9, "Juin 27"), (10, "Juil 27"), (11, "Août 27"),
]

STATUS_CHOICES = [
    (0, "À faire"),
    (1, "En cours"),
    (2, "En bonne voie"),
]

COLOR_CHOICES = [
    ("#3E6E63", "Vert forêt"),
    ("#B9852F", "Ochre"),
    ("#5B7FBF", "Bleu"),
    ("#8A6FBF", "Violet"),
    ("#C1685A", "Terracotta"),
    ("#4FA391", "Vert d'eau"),
]


class Goal(models.Model):
    name = models.CharField("Nom", max_length=200)
    when_label = models.CharField("Quand (texte libre)", max_length=120, blank=True)
    objective = models.TextField("Objectif", blank=True)
    status = models.IntegerField("Statut", choices=STATUS_CHOICES, default=0)
    start_month = models.IntegerField("Mois de début", choices=MONTH_CHOICES, default=0)
    end_month = models.IntegerField("Mois de fin", choices=MONTH_CHOICES, default=1)
    deadline_month = models.IntegerField(
        "Mois de l'échéance", choices=MONTH_CHOICES, null=True, blank=True
    )
    deadline_label = models.CharField("Libellé de l'échéance", max_length=120, blank=True)
    color = models.CharField("Couleur", max_length=7, choices=COLOR_CHOICES, default="#3E6E63")
    order = models.IntegerField("Ordre", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    def next_status(self):
        return (self.status + 1) % 3

    def status_label(self):
        return dict(STATUS_CHOICES)[self.status]

    def deadline_pct(self):
        if self.deadline_month is None:
            return None
        return round((self.deadline_month + 0.5) / 12 * 100, 1)

    def grid_columns(self):
        return self.start_month + 2, self.end_month + 3


class SavingsConfig(models.Model):
    """Singleton : un seul enregistrement pour l'objectif d'épargne."""
    target_amount = models.PositiveIntegerField("Objectif (FCFA)", default=800000)
    target_date = models.DateField("Date du voyage", null=True, blank=True)

    def __str__(self):
        return f"Objectif: {self.target_amount} FCFA"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SavingsEntry(models.Model):
    amount = models.PositiveIntegerField("Montant (FCFA)")
    note = models.CharField("Note", max_length=200, blank=True)
    created_at = models.DateTimeField("Date", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.amount} FCFA — {self.note}"


class Opportunity(models.Model):
    title = models.CharField("Titre", max_length=200)
    url = models.URLField("Lien", blank=True)
    note = models.CharField("Note / statut", max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
