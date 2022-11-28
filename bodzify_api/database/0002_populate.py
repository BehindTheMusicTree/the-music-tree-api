from django.db import migrations

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesLabels
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeLabels

def populateCriteriaTypes(apps, schemaEditor):
    CriteriaType = apps.get_model('bodzify_api', 'CriteriaType')
    CriteriaType(label=CriteriaTypesLabels.GENRE).save()
    CriteriaType(label=CriteriaTypesLabels.TAG).save()

def populatePlaylistTypes(apps, schemaEditor):
    PlaylistType = apps.get_model('bodzify_api', 'PlaylistType')
    PlaylistType(label=PlaylistTypeLabels.GENRE).save()
    PlaylistType(label=PlaylistTypeLabels.TAG).save()
    PlaylistType(label=PlaylistTypeLabels.CUSTOM).save()

class Migration(migrations.Migration):

    dependencies = [
        ('bodzify_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populateCriteriaTypes),
        migrations.RunPython(populatePlaylistTypes)
    ]
