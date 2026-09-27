from django.db import migrations, models

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


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Goal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Nom")),
                ("when_label", models.CharField(blank=True, max_length=120, verbose_name="Quand (texte libre)")),
                ("objective", models.TextField(blank=True, verbose_name="Objectif")),
                ("status", models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Statut")),
                ("start_month", models.IntegerField(choices=MONTH_CHOICES, default=0, verbose_name="Mois de début")),
                ("end_month", models.IntegerField(choices=MONTH_CHOICES, default=1, verbose_name="Mois de fin")),
                ("deadline_month", models.IntegerField(blank=True, choices=MONTH_CHOICES, null=True, verbose_name="Mois de l'échéance")),
                ("deadline_label", models.CharField(blank=True, max_length=120, verbose_name="Libellé de l'échéance")),
                ("color", models.CharField(choices=COLOR_CHOICES, default="#3E6E63", max_length=7, verbose_name="Couleur")),
                ("order", models.IntegerField(default=0, verbose_name="Ordre")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="SavingsConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("target_amount", models.PositiveIntegerField(default=800000, verbose_name="Objectif (FCFA)")),
                ("target_date", models.DateField(blank=True, null=True, verbose_name="Date du voyage")),
            ],
        ),
        migrations.CreateModel(
            name="SavingsEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.PositiveIntegerField(verbose_name="Montant (FCFA)")),
                ("note", models.CharField(blank=True, max_length=200, verbose_name="Note")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Date")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Titre")),
                ("url", models.URLField(blank=True, verbose_name="Lien")),
                ("note", models.CharField(blank=True, max_length=300, verbose_name="Note / statut")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]