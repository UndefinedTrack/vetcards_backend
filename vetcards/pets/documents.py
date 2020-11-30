from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Pet
from users.models import User

@registry.register_document
class PetDocument(Document):

    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'patronymic': fields.TextField(),
        'last_name': fields.TextField()
    })
    class Index:

        name = 'pets'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 
                  'color', 'birth_date', 'gender', 'chip', 'sterilized', 'vaccinated', 
                  'contraindications', 'notes', 'weight', 'avatar']
        related_models = [User]

    def get_queryset(self):
        return super(PetDocument, self).get_queryset().select_related(
            'user'
        )
        
    def get_instances_from_related(self, related_instance):
        pass