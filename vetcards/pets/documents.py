from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Pet

@registry.register_document
class PetDocument(Document):
    class Index:
        name = 'pets'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = Pet
        fields = ['id', 'user_id', 'name', 'species', 'breed', 
                  'color', 'birth_date', 'gender', 'chip']