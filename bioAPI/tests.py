# I wrote this code

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.management import call_command


class ProteinTests(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        self.client = APIClient()

    def test_add_new_protein_record(self):
        url = reverse('addData')
        data = {
            'protein_id': 'A0A099S8J7',
            'sequence': 'MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA',
            'organism_taxa_id': 53326,
            'organism_clade_identifier': 'E',
            "organism_scientific_name": "Ancylostoma ceylanicum",
            'protein_length': 101,
            'domain_id': 'PF451650',
            'domain_description': 'PeptidaseC13family',
            'pfam_description': 'PeptidaseC13legumain',
            'domain_start_coordinate': 40,
            'domain_end_coordinate': 94,



        }
        response = self.client.post(url, data)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Protein entry added successfully.')
        # Add additional assertions to check the response data or database state if needed

    def test_get_protein_by_id(self):
        protein_id = 'A0A016S8J7'
        url = reverse('protein-by-id', args=[protein_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions to check the response data

    def test_get_pfam_by_id(self):
        pfam_id = 'PF00360'
        url = reverse('pfam-by-id', args=[pfam_id])
        response = self.client.get(url)
        print(response.data, response.status_code, "test-pfams")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions to check the response data

    def test_get_proteins_by_taxa_id(self):
        taxa_id = 55661
        url = reverse('proteins-by-taxa-id', args=[taxa_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions to check the response data

    def test_get_pfams_by_taxa_id(self):
        taxa_id = 55661
        url = reverse('pfams-by-taxa-id', args=[taxa_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions to check the response data

    def test_get_protein_coverage(self):
        protein_id = 'A0A016S8J7'
        url = reverse('protein_coverage-by-protein-id', args=[protein_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions to check the response data



print("This is my code")

# end of code I wrote