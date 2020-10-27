from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Procedure, OwnerProcedure

@registry.register_document
class OwnerProcedureDocument(Document):

    pet_id = fields.IntegerField(attr='pet')
    user_id = fields.IntegerField(attr='user')
    class Index:
        name = 'owner_procs'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = OwnerProcedure
        fields = ['id', 'name', 'description', 'proc_date']
        
@registry.register_document
class VetProcedureDocument(Document):

    pet_id = fields.IntegerField(attr='pet')
    user_id = fields.IntegerField(attr='user')
    class Index:
        name = 'vet_procs'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}
        
    class Django:
        model = Procedure
        fields = ['id', 'purpose', 'symptoms', 'diagnosis',
                    'recomms', 'recipe', 'proc_date']