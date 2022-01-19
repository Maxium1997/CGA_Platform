from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView


from cga_case.models import CaseCategory, CaseSection, Case
# Create your views here.


class CaseCategoriesView(ListView):
    model = CaseCategory


class CaseSectionsView(ListView):
    model = CaseSection

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseSectionsView, self).get_context_data(object_list=None, **kwargs)
        context['category'] = self.kwargs.get('category_name')
        return context

    def get_queryset(self):
        category = get_object_or_404(CaseCategory, name=self.kwargs.get('category_name'))
        return CaseSection.objects.filter(is_part_of=category)


class CaseDetailView(DetailView):
    model = Case

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseDetailView, self).get_context_data(object_list=None, **kwargs)
        case = get_object_or_404(Case, title=self.kwargs.get('case_title'))
        context['category'] = case.is_one_of.is_part_of
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Case, title=self.kwargs.get('case_title'))
