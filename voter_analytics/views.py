from collections import Counter
from django.shortcuts import render
from .models import Voter
from django.views.generic import ListView, DetailView
import plotly
import plotly.graph_objects as go 
import plotly.offline as pyo 
from django.db.models import Q, Count

# Create your views here.
class VotersView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=max_dob)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        for election, voted in elections.items():
            if voted:
                queryset = queryset.filter(**{election: True})
        
        print(queryset.count())
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Voter List View'  
        
        get_copy = self.request.GET.copy()

        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
    
    def get_queryset(self):
        voter_id = self.kwargs['pk']
        return Voter.objects.filter(pk=voter_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Voter Detail View'
        return context

class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = super().get_queryset()
        
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        filters = Q()
        if party_affiliation:
            filters &= Q(party_affiliation=party_affiliation)
        if min_dob:
            filters &= Q(date_of_birth__year__gte=min_dob)
        if max_dob:
            filters &= Q(date_of_birth__year__lte=max_dob)
        if voter_score:
            filters &= Q(voter_score=voter_score)
        if v20state:
            filters &= Q(v20state=True)
        if v21town:
            filters &= Q(v21town=True)
        if v21primary:
            filters &= Q(v21primary=True)
        if v22general:
            filters &= Q(v22general=True)
        if v23town:
            filters &= Q(v23town=True)

        queryset = Voter.objects.filter(filters)

        context['voters'] = queryset

        # Histogram: Distribution by Year of Birth
        birth_year = queryset.values_list('date_of_birth__year', flat=True)
        counts = dict(Counter(birth_year))
        year = list(counts.keys())
        frequency = list(counts.values())

        dob_hist = go.Bar(x=year, y=frequency, name="Voters by Date of Birth")
        dob_hist_div = pyo.plot({"data": [dob_hist]}, auto_open=False, output_type="div")
        context['dob_div'] = dob_hist_div


        # Pie Chart: Distribution by Party Affiliation
        party_count = queryset.values('party_affiliation').annotate(count=Count('party_affiliation')) 
        party_labels = [item['party_affiliation'] for item in party_count]
        party_values = [item['count'] for item in party_count]

        pie_fig = go.Pie(labels=party_labels, values=party_values, name="Voters by Party Affiliation")
        pie_div = pyo.plot({"data": [pie_fig]}, auto_open=False, output_type="div")
        context['pie_div'] = pie_div

        # Histogram: Distribution by Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {election: queryset.filter(**{election: True}).count() for election in elections}
        election_values = list(election_counts.values())

        election_hist = go.Bar(x=elections, y=election_values, name="Voters by Election Participation")
        election_hist_div = pyo.plot({"data": [election_hist]}, auto_open=False, output_type="div")
        context['election_div'] = election_hist_div

        return context
