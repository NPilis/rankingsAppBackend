from django.db.models import Q
from .models import Ranking

class RankingSearch:
    def __init__(self, query):
        self.query = query
        self.keywords = set(term for term in self.query.split() if len(term) >= 3)
    
    def get_results(self):
        if not self.keywords:
            return None
        init = self.keywords.pop()
        results = Q(title__icontains=init)
        for term in self.keywords:
            results |= Q(title__icontains=term)
        return Ranking.objects.filter(results, status="public")