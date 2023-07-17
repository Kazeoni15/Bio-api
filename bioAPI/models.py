# I wrote this code

from django.db import models

class ProteinSequence(models.Model):
    protein_id = models.CharField(max_length=255, primary_key=True)
    sequence = models.TextField()



class PfamDescription(models.Model):
    domain_id = models.CharField(max_length=255, primary_key=True)
    pfam_description = models.CharField(max_length=255)


class ProteinDomain(models.Model):
    protein_id = models.ForeignKey(ProteinSequence, on_delete=models.CASCADE)
    organism_taxa_id = models.IntegerField()
    organism_clade_identifier = models.CharField(max_length=255)
    organism_scientific_name = models.CharField(max_length=255)
    domain_description = models.CharField(max_length=255)
    domain_id = models.ForeignKey(PfamDescription, on_delete=models.CASCADE)
    domain_start_coordinate = models.IntegerField()
    domain_end_coordinate = models.IntegerField()
    protein_length = models.IntegerField()

print('this is my code')

# end of code I wrote

