from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Procedure, OwnerProcedure

@registry.register_document
class OwnerProcedureDocument(Document):
    class Index:
        name = 'owner_procs'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = OwnerProcedure
        fields = ['id', 'pet_id', 'user_id', 'name', 'description', 'proc_date']
        
@registry.register_document
class VetProcedureDocument(Document):
    class Index:
        name = 'vet_procs'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = Procedure
        fields = ['id', 'pet_id', 'user_id', 'purpose', 'symptoms',
                  'diagnosis', 'recomms', 'recipe', 'proc_date']