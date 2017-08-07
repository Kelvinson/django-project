import django_tables2 as tables
from .models import Person,FDataFrame,ADataFrame

class PersonTable(tables.Table):
    class Meta:
        model = ADataFrame
        
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
