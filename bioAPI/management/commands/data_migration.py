# I wrote this code

import csv
from django.core.management.base import BaseCommand
from bioAPI.models import PfamDescription, ProteinDomain, ProteinSequence

class Command(BaseCommand):
    help = 'Migrate data from CSV files to the database'

    def handle(self, *args, **options):
        self.stdout.write('Migrating data...')

        # Read and migrate the data from each CSV file
        self.migrate_sequences()
        self.migrate_pfam_descriptions()
        self.migrate_assignment_data_set()

        self.stdout.write('Data migration completed.')

    def migrate_sequences(self):
        # Open and read the sequences CSV file
        with open('data/protein.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                row_values = list(row.values())
                # Create ProteinSequence objects and save them
                protein_sequence = ProteinSequence(protein_id=row_values[0], sequence=row_values[1])
                protein_sequence.save()

    def migrate_pfam_descriptions(self):
        # Open and read the pfam descriptions CSV file
        with open('data/pfam.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                row_values = list(row.values())
                # Create PfamDescription objects and save them
                pfam_description = PfamDescription(domain_id=row_values[0], pfam_description=row_values[1])
                pfam_description.save()

    def migrate_assignment_data_set(self):
        # Open and read the assignment data set CSV file
        with open('data/dataset.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                row_values = list(row.values())

                # Get or create the associated ProteinSequence object
                protein_sequence, created = ProteinSequence.objects.get_or_create(protein_id=row_values[0])

                # Get or create the associated PfamDescription object
                pfam_description, created = PfamDescription.objects.get_or_create(domain_id=row_values[5])

                # Create ProteinDomain object and save it
                protein_domain = ProteinDomain(
                    protein_id=protein_sequence,
                    organism_taxa_id=row_values[1],
                    organism_clade_identifier=row_values[2],
                    organism_scientific_name=row_values[3],
                    domain_description=row_values[4],
                    domain_id=pfam_description,
                    domain_start_coordinate=row_values[6],
                    domain_end_coordinate=row_values[7],
                    protein_length=row_values[8]
                )
                protein_domain.save()

print("this is my code")
# End of code I wrote