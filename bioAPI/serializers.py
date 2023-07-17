# I wrote this code

from rest_framework import serializers
from bioAPI.models import ProteinSequence, ProteinDomain, PfamDescription

class ProteinSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinSequence
        fields = ['protein_id', 'sequence']


class PfamDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PfamDescription
        fields = ['domain_id', 'pfam_description']


class ProteinDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinDomain
        fields = ['protein_id_id', 'organism_taxa_id', 'organism_clade_identifier', 'organism_scientific_name',
                  'domain_description', 'domain_id_id', 'domain_start_coordinate', 'domain_end_coordinate',
                  'protein_length']

print('This is my code: serializers.py')

# end of code I wrote