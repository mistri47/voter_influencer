from django.shortcuts import render

# Create your views here.
from voter.models import AgentType

def workers(request):

    booth_id = None
    if request.method == 'POST':
        booth_id = request.POST['booth_id']

    agent_types = AgentType.objects.all()
    return render(request, 'pages/workers.html', {
        'agent_types': agent_types,
        'id': booth_id
    })