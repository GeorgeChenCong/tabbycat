from django.shortcuts import get_object_or_404

from debate.models import Tournament, Round
from django.core.cache import cache

class DebateMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'tournament_slug' in view_kwargs:
            cached_key = "%s_%s" % (view_kwargs['tournament_slug'], 'object')
            cached_tournament_object = cache.get(cached_key)

            if cached_tournament_object:
                request.tournament = cached_tournament_object
            else:
                request.tournament = get_object_or_404(Tournament,
                                                   slug=view_kwargs['tournament_slug'])
                cache.set(cached_key, request.tournament, None)

            if 'round_seq' in view_kwargs:
                cached_key = "%s_%s_%s" % (view_kwargs['tournament_slug'], view_kwargs['round_seq'], 'object')
                cached_round_object = cache.get(cached_key)
                if cached_round_object:
                    request.round = cached_round_object
                else:
                    request.round = get_object_or_404(Round,
                                                  tournament=request.tournament,
                                                  seq=view_kwargs['round_seq'])
                    cache.set(cached_key, request.round, None)

        return None

