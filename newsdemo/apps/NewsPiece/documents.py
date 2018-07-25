from django_elasticsearch_dsl import DocType, Index
from .models import NewsPiece

newspiece = Index('newspieces')

newspiece.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@newspiece.doc_type
class NewsPieceDocument(DocType):
    class Meta:
        model = NewsPiece

        fields = [
            'author',
            'time_issued',
            'title',
            'text',
        ]