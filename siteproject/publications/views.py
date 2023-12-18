from django.views.generic import DetailView
from .models import Publication


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publications/publication.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
