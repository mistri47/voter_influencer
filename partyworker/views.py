from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
User = get_user_model()

from partyworker.models import PartyWorker, WorkerType

from voter.models import Caste


def list_items(request):

    booth_id = None
    if request.method == 'POST':
        booth_id = request.POST['booth_id']

    worker_types = WorkerType.objects.all()
    workers = PartyWorker.objects.all()

    return render(request, 'worker/workers.html', {
        'workers': workers,
        'worker_types': worker_types
    })


def add_item(request):

    worker_types = WorkerType.objects.all()
    caste_names = Caste.objects.all()

    if request.method == 'POST':
        mobile = request.POST['mobile']
        full_name = request.POST['full_name']
        gender = request.POST['gender']
        worker_type_id = request.POST['worker_type']
        caste_id = request.POST['caste']

        user = User.objects.create_user(mobile, f"{mobile}@example.com", str(mobile))
        user.save()

        worker_type = WorkerType.objects.get(pk=worker_type_id)
        caste = Caste.objects.get(pk=caste_id)

        PartyWorker(
            user = user,
            mobile = mobile,
            full_name = full_name,
            gender = gender,
            worker_type = worker_type,
            caste = caste
        ).save()
        return redirect('list_workers')

    return render(request, 'worker/add_worker.html', {
        'worker_types': worker_types,
        'caste_names': caste_names
    })
      

def update_item(request, id):

    worker_types = WorkerType.objects.all()
    caste_names = Caste.objects.all()
    worker = PartyWorker.objects.get(pk=id)

    if request.method == 'POST':
        print("Updating")
        full_name = request.POST['full_name']
        print(full_name)
        gender = request.POST['gender']
        worker_type_id = request.POST['worker_type']
        caste_id = request.POST['caste']

        worker_type = WorkerType.objects.get(pk=worker_type_id)
        caste = Caste.objects.get(pk=caste_id)

        worker.full_name = full_name
        worker.gender = gender
        worker.worker_type = worker_type
        worker.caste = caste
        worker.save()

        return redirect('list_workers')

    return render(request, 'worker/edit_worker.html', {
        'worker_types': worker_types,
        'caste_names': caste_names,
        'worker': worker
    })
            

def delete_item(request, id):
    return redirect('list_workers')
    pass