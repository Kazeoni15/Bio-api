"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# I wrote this code

from django.contrib import admin
from django.urls import path
from django.urls import path
from bioAPI.views import ProteinDetailView
from bioAPI.views import PfamDetailView
from bioAPI.views import ProteinsByTaxaView
from bioAPI.views import PfamsByTaxaView
from bioAPI.views import ProteinCoverageView
from bioAPI.views import Home
from bioAPI.views import AddData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/protein/<str:protein_id>', ProteinDetailView.as_view(), name='protein-by-id'),
    path('api/pfam/<str:pfam_id>', PfamDetailView.as_view(), name='pfam-by-id'),
    path('api/proteins/<int:taxa_id>', ProteinsByTaxaView.as_view(), name='proteins-by-taxa-id'),
    path('api/pfams/<int:taxa_id>', PfamsByTaxaView.as_view(), name='pfams-by-taxa-id'),
    path('api/coverage/<str:protein_id>', ProteinCoverageView.as_view(), name='protein_coverage-by-protein-id'),
    path('', Home, name='home'),
    path('api/protein/', AddData, name="addData")
]

print("this is my code: urls.py")

# end of code I wrote