from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q


from cga_case.models import CaseCategory, CaseSection, Case
from cga_case.forms import CaseSearchForm
from itertools import chain
from collections import OrderedDict
# Create your views here.


class CaseCategoriesView(ListView):
    model = CaseCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case_search_form'] = CaseSearchForm()
        return context


def case_search(request):
    case_search_form = CaseSearchForm(request.POST)
    keyword = str(request.POST.get('search_field'))

    filter_criteria = Q(name__icontains=keyword)
    case_categories = CaseCategory.objects.filter(filter_criteria)

    filter_criteria = Q(name__icontains=keyword)
    case_sections = CaseSection.objects.filter(filter_criteria)

    filter_criteria = Q(title__icontains=keyword) | Q(legal_resources__icontains=keyword) | \
                      Q(handling_point__icontains=keyword) | Q(cautions__icontains=keyword)
    cases = Case.objects.filter(filter_criteria)

    context = {'case_search_form': case_search_form,
               'keyword': keyword,
               'case_categories': case_categories,
               'case_sections': case_sections,
               'cases': cases}

    return render(request, template_name='cga_case/search_result.html', context=context)


class CaseSectionsView(ListView):
    model = CaseSection

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseSectionsView, self).get_context_data(object_list=None, **kwargs)
        context['category'] = self.kwargs.get('case_category_name')
        return context

    def get_queryset(self):
        category = get_object_or_404(CaseCategory, name=self.kwargs.get('case_category_name'))
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


@method_decorator(login_required, name='dispatch')
class CaseUpdateView(UpdateView):
    model = Case
    fields = ['legal_resources', 'handling_point', 'cautions', 'flow_chart']
    template_name = 'cga_case/case_update.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super(CaseUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseUpdateView, self).get_context_data(object_list=None, **kwargs)
        case = get_object_or_404(Case, title=self.kwargs.get('case_title'))
        context['category'] = case.is_one_of.is_part_of
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Case, title=self.kwargs.get('case_title'))

    def form_valid(self, form):
        messages.success(self.request, "Updated successfully.")
        return super(CaseUpdateView, self).form_valid(form)

    def get_success_url(self):
        case = self.get_object()
        return reverse_lazy('case_update', kwargs={'case_title': case.title})


@method_decorator(login_required, name='dispatch')
class CaseCreateView(CreateView):
    model = Case
    fields = ['serial_number', 'title']
    template_name = 'cga_case/case_create.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super(CaseCreateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseCreateView, self).get_context_data(object_list=None, **kwargs)
        case_section = get_object_or_404(CaseSection, name=self.kwargs.get('case_section_name'))
        context['section'] = case_section
        context['category'] = case_section.is_part_of
        return context

    def get_object(self, queryset=None):
        section = get_object_or_404(CaseSection, name=self.kwargs.get('case_section_name'))
        return section

    def get_initial(self):
        initial = super(CaseCreateView, self).get_initial()
        initial['is_one_of'] = self.get_object()
        return initial

    def form_valid(self, form):
        case = form.instance
        case.is_one_of = self.get_initial().get('is_one_of')
        case.save()
        messages.success(self.request, 'Case created successfully: {}. Please update the content.'.format(case.title))
        return super(CaseCreateView, self).form_valid(form)

