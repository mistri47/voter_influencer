from django.shortcuts import render

from .models import PollingStation
from .tasks import pdf_to_images_task, draw_boxes_around_voter_details_task, crop_voter_details_images_task, update_voter_id_task, update_details_task
# Create your views here.

def details(request, id):
    polling_station = PollingStation.objects.get(pk=id)

    return render(request, 'polling_stations/station_details.html', {
        'polling_station': polling_station
    })  


def list_items(request):
    polling_stations = PollingStation.objects.all()
    return render(request, 'polling_stations/polling_stations.html', {
        'polling_stations': polling_stations
    })  



def add(request):
    if request.method == 'POST':
        number = request.POST['number']
        name = request.POST['name']

    return render(request, 'polling_stations/add_polling_station.html', {
    })   

def update(request, id):
    pass

def delete(request, id):
    pass


def create_images_from_pdf(request, booth_id):
    pdf_to_images_task.delay()
    return render(request, 'pages/home.html', {})  

def draw_boxes_around_voter_details(request, booth_id):
    draw_boxes_around_voter_details_task.delay()
    return render(request, 'pages/home.html', {})  

def crop_voter_details_images(request, booth_id):
    crop_voter_details_images_task.delay()
    return render(request, 'pages/home.html', {})  

def read_voter_id(request, booth_id):
    update_voter_id_task.delay()
    return render(request, 'pages/home.html', {})

def capture_details(request, booth_id):
    update_details_task.delay()
    return render(request, 'pages/home.html', {})
 