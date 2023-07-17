# I wrote this code
from django.http import JsonResponse
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from bioAPI.models import ProteinDomain, PfamDescription, ProteinSequence
from bioAPI.serializers import ProteinDomainSerializer, PfamDescriptionSerializer, ProteinSequenceSerializer



class ProteinDetailView(APIView):
    def get(self, request, protein_id):
        # Retrieve the ProteinSequence object or return a 404 response
        protein_sequence = get_object_or_404(ProteinSequence, protein_id=protein_id)

        # Retrieve the ProteinDomain objects based on the protein_id
        protein_domains = ProteinDomain.objects.filter(protein_id=protein_id)

        # Check if protein_domains is empty
        if not protein_domains:
            return Response({'error': 'No protein domains found for the given protein ID'}, status=404)

        # Retrieve all PfamDescription objects using a bulk query
        pfam_ids = protein_domains.values_list('domain_id_id', flat=True)
        pfam_descriptions = PfamDescription.objects.filter(domain_id__in=pfam_ids)

        # Create a dictionary mapping Pfam IDs to descriptions
        pfam_descriptions_dict = {pfam.domain_id: pfam.pfam_description for pfam in pfam_descriptions}

        # Create a list to store the domain data
        domain_data = []

        # Iterate over the protein_domains queryset and retrieve the required information
        for protein_domain in protein_domains:
            pfam_id = protein_domain.domain_id_id

            domain_info = {
                'pfam_id': {
                    'domain_id': pfam_id,
                    'domain_description': pfam_descriptions_dict.get(pfam_id)
                },
                'description': protein_domain.domain_description,
                'start': protein_domain.domain_start_coordinate,
                'stop': protein_domain.domain_end_coordinate
            }
            domain_data.append(domain_info)

        # Create the response JSON
        response_data = {
            'protein_id': protein_id,
            'sequence': protein_sequence.sequence,
            'taxonomy': {
                'taxa_id': protein_domains[0].organism_taxa_id,
                'clade': protein_domains[0].organism_clade_identifier,
                'genus': protein_domains[0].organism_scientific_name.split(" ")[0],
                'species': " ".join(protein_domains[0].organism_scientific_name.split(" ")[1:])
            },
            'domains': domain_data
        }

        return Response(response_data, status=200)


class PfamDetailView(APIView):
    def get(self, request, pfam_id):
        print(request, pfam_id)
        # Retrieve the PfamDescription object or return a 404 response
        pfam_description = get_object_or_404(PfamDescription, domain_id=pfam_id)

        # Create the response JSON
        response_data = {
            'domain_id': pfam_id,
            'domain_description': pfam_description.pfam_description
        }

        return Response(response_data, status=200)


class ProteinsByTaxaView(APIView):
    def get(self, request, taxa_id):
        # Retrieve all ProteinDomain objects for the given taxa ID
        protein_domains = ProteinDomain.objects.filter(organism_taxa_id=taxa_id)

        # Check if protein_domains is empty
        if not protein_domains:
            return Response({'error': 'No proteins found for the given taxa ID'}, status=404)

        # Create a list of dictionaries containing the protein ID and the ID of the ProteinDomain object
        proteins_list = [
            {
                'id': protein_domain.id,
                'protein_id': protein_domain.protein_id.protein_id
            }
            for protein_domain in protein_domains
        ]

        return Response(proteins_list, status=200)




class PfamsByTaxaView(APIView):
    def get(self, request, taxa_id):
        try:
            # Retrieve the ProteinDomain objects for the given taxa ID
            protein_domains = ProteinDomain.objects.filter(organism_taxa_id=taxa_id)

            if not protein_domains:
                return Response({'error': 'No Pfams found for the given taxa ID'}, status=404)
            # Create a list of dictionaries to store the Pfam IDs and descriptions
            pfams = []

            # Iterate over the ProteinDomain objects and retrieve the corresponding PfamDescription
            for protein_domain in protein_domains:
                pfam_descriptions = PfamDescription.objects.get(domain_id=protein_domain.domain_id_id)

                # Create a dictionary for each Pfam ID and description
                pfam = {
                    'id': protein_domain.id,
                    'pfam_id': {
                        'domain_id': protein_domain.domain_id_id,
                        'domain_description': pfam_descriptions.pfam_description
                    }
                }

                pfams.append(pfam)

            # Create the response JSON

            response_data = pfams

            return Response(response_data, status=200)

        except ProteinDomain.DoesNotExist:
            return Response({'error': 'No protein domains found for the given taxa ID'}, status=404)


class ProteinCoverageView(APIView):
    def get(self, request, protein_id):
        # Retrieve the ProteinDomain objects for the given protein ID
        protein_domains = ProteinDomain.objects.filter(protein_id=protein_id)

        # Check if protein_domains is empty
        if not protein_domains:
            return Response({'error': 'No protein domains found for the given protein ID'}, status=404)

        # Calculate the coverage
        total_coverage = 0
        for protein_domain in protein_domains:
            domain_length = protein_domain.domain_end_coordinate - protein_domain.domain_start_coordinate
            coverage = domain_length / protein_domain.protein_length
            total_coverage += coverage

        # Create the response JSON
        response_data = {
            'coverage': total_coverage
        }

        return Response(response_data, status=200)




def Home(request):
    return render(request, 'home.html')


@api_view(['GET', 'POST'])
def AddData(request):
    if request.method == 'POST':

        # print(request.POST)
        protein_id = request.POST.get('protein_id')
        sequence = request.POST.get('sequence')
        taxa_id = request.POST.get('organism_taxa_id')
        clade = request.POST.get('organism_clade_identifier')
        scientific_name = request.POST.get('organism_scientific_name')
        length = request.POST.get('protein_length')
        domain_id = request.POST.get('domain_id')
        pfam_description = request.POST.get('pfam_description')
        domain_description = request.POST.get('domain_description')
        start = request.POST.get('domain_start_coordinate')
        end = request.POST.get('domain_end_coordinate')


        protein_sequence_serializer = ProteinSequenceSerializer(data=request.data)
        pfam_description_serializer = PfamDescriptionSerializer(data=request.data)
        protein_domain_serializer = ProteinDomainSerializer(data=request.data)

        protein_sequence_serializer.is_valid(raise_exception=True)
        pfam_description_serializer.is_valid(raise_exception=True)
        protein_domain_serializer.is_valid(raise_exception=True)

        protein_sequence_data = protein_sequence_serializer.validated_data
        pfam_description_data = pfam_description_serializer.validated_data
        protein_domain_data = protein_domain_serializer.validated_data

        protein_sequence = ProteinSequence.objects.create(protein_id=protein_sequence_data['protein_id'], sequence=protein_sequence_data['sequence'])
        pfam_description = PfamDescription.objects.create(domain_id=pfam_description_data['domain_id'], pfam_description= pfam_description)
        protein_domain = ProteinDomain.objects.create(
            protein_id_id=protein_id,
            organism_taxa_id=taxa_id,
            organism_clade_identifier=clade,
            organism_scientific_name=scientific_name,
            domain_description=pfam_description,
            domain_id_id=domain_id,
            domain_start_coordinate=start,
            domain_end_coordinate=end,
            protein_length=length
        )

        return Response({'message': 'Protein entry added successfully.'})

    return render(request, 'protein.html')



print("This is my code: views.py")

# end of code I wrote
