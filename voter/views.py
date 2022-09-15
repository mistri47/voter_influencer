from django.shortcuts import render

from polling_station.models import PollingStation
from .models import Voter
# Create your views here.
from django.db.models import Q


def voters(request):

    if request.method == 'POST':
        mobile = request.POST['mobile']
        voter_id = request.POST['voter_id']
        booth_id = request.POST['booth']
        polling_booth = None

        if booth_id:
            polling_booth = PollingStation.objects.get(pk=booth_id)

        voters = Voter.objects.filter(
            Q(mobile = mobile) |
            Q(polling_booth=polling_booth)
        )

        return render(request, 'voter/voters.html', {
            'voters': voters
        })

    booths = PollingStation.objects.all() # Later filter for permissions
    return render(request, 'voter/voters.html', {
        'booths': booths
    })



