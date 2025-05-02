from django.db import models
import os

def person_photo_path(instance, filename):
    # Fonction pour déterminer le chemin d'enregistrement
    return os.path.join('persons', str(instance.id), filename)

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    nom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dateNaissance = models.CharField(max_length=50)
    photo = models.ImageField(
        upload_to=person_photo_path,
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        # Supprime l'ancienne photo si elle existe lors de la mise à jour
        if self.pk:
            old_photo = Person.objects.get(pk=self.pk).photo
            if old_photo and old_photo != self.photo:
                old_photo.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Supprime la photo lors de la suppression de la personne
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)




class FamilyRelation(models.Model):
    RELATION_TYPES = [
        ('spouse', 'Conjoint'),
        ('child', 'Enfant'),
    ]

    from_person = models.ForeignKey(Person, related_name='outgoing_relations', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='incoming_relations', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=RELATION_TYPES)

    class Meta:
        unique_together = ('from_person', 'to_person', 'type')

    def __str__(self):
        return f"{self.from_person} -> {self.to_person} ({self.get_type_display()})"