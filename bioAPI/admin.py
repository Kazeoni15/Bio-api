from django.contrib import admin
from bioAPI.models import ProteinDomain, ProteinSequence, PfamDescription
# Register your models here.

# this is my code
admin.site.register(ProteinDomain)
admin.site.register(ProteinSequence)
admin.site.register(PfamDescription)

print('This is my code: admin.py')

# end of code I wrote