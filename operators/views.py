from django.http import HttpResponse
from django.shortcuts import redirect, render
from operators.forms import *
from customers.models import *
from django.contrib import messages
import folium
from folium.plugins import MarkerCluster
from customers.decrators import allowed_users, unauthenticated_user, admin
from io import BytesIO
from customers.utils import check_code
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def image_code(request):
    img, code_string = check_code()
    # request.session['image_code'] = code_string
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def loginOperator(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('operators')
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'loginOperator.html', context)


def logoutOperator(request):
    logout(request)
    return redirect('index')


@allowed_users(allowed_roles=['admin'])
def operators(request):
    current_location = vehicle_list()
    status = vehicle_list()
    repair = vehicle_list()
    bikes = vehicle_list()
    current_latitude = bikes.latitude
    current_longitude = bikes.longitude
    folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(folium_Map)
    all_bikes = vehicle_list.objects.all()
    type = bikes.v_type


    for bike in all_bikes:
        type = bike.v_type
        if type == True:
            type = "Bike"
        else:
            type = "Scooter"

        folium.Marker([bike.latitude, bike.longitude], tooltip="Click for more",
                      popup="id:" + str(bike.id) + "\nType:" + type + "\nStreet:" + str(bike.location) +
                            "\nBattery:" + str(bike.battery)).add_to(marker_cluster)
    folium_Map.add_child(marker_cluster)
    folium_Map = folium_Map._repr_html_()

    context = {
        'location': current_location,
        'bikes': bikes,
        'status': status,
        'repair': repair,
        'bikes_id': bikes,
        'current_latitude': current_latitude,
        'current_longitude': current_longitude,
        'map': folium_Map,
        'type': type,
    }

    return render(request, "op_main.html", context=context)


@allowed_users(allowed_roles=['admin'])
def operators_track(request):
    form = TrackBike(request.POST)
    current_location = vehicle_list()
    status = vehicle_list()
    repair = vehicle_list()
    bikes = vehicle_list()
    track = False
    current_latitude = bikes.latitude
    current_longitude = bikes.longitude
    type = bikes.v_type
    battery = bikes.battery
    charge = False

    folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)

    marker_cluster = MarkerCluster().add_to(folium_Map)
    all_bikes = vehicle_list.objects.all()

    for bike in all_bikes:
        type = bike.v_type
        if type == True:
            type = "Bike"
        else:
            type = "Scooter"
        folium.Marker([bike.latitude, bike.longitude], tooltip="Click for more",
                      popup="id:" + str(bike.id) + "\nType:" + type + "\nStreet:" + str(bike.location) +
                            "\nBattery:" + str(bike.battery)).add_to(marker_cluster)

    folium_Map.add_child(marker_cluster)

    if request.method == 'POST' and 'track' in request.POST:
        form = TrackBike(request.POST)
        track = True
        if form.is_valid():
            bikes = form.cleaned_data.get("bike_id")
            current_location = bikes.location
            current_latitude = bikes.latitude
            current_longitude = bikes.longitude
            status = bikes.status
            repair = bikes.repair
            battery = bikes.battery
            type = bikes.v_type
            if battery <= 10:
                charge = True
            else:
                charge = False

            if type == True:
                type = "Bike"
            else:
                type = "Electric scooter"

            folium.CircleMarker([current_latitude, current_longitude], tooltip="Click for more", fill=True,
                                fill_color="#DC143C", color="#DC143C", popup="id:" + str(bikes.id) +
                                                                             "\nType:" + type +
                                                                             "\nStreet:" +
                                                                             str(current_location) +
                                                                             "\nBattery:" +
                                                                             str(bikes.battery)).add_to(folium_Map)

    folium_Map = folium_Map._repr_html_()

    context = {
        'location': current_location,
        'bikes': bikes,
        'status': status,
        'repair': repair,
        'form': form,
        'bikes_id': bikes,
        'track': track,
        'current_latitude': current_latitude,
        'current_longitude': current_longitude,
        'map': folium_Map,
        'type': type,
        'charge': charge,
    }
    return render(request, "op_track.html", context=context)


@allowed_users(allowed_roles=['admin'])
def operators_move(request):
    bikes = vehicle_list()
    form = MoveBike(request.POST)
    form_loc = StartLocation(request.POST)
    move = False
    des_location = destination_location()
    current_location = vehicle_list()
    current_latitude = bikes.latitude
    current_longitude = bikes.longitude
    type = bikes.v_type


    folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    all_bikes = vehicle_list.objects.all()
    marker_cluster = MarkerCluster().add_to(folium_Map)

    for bike in all_bikes:
        type = bike.v_type
        if type == True:
            type = "Bike"
        else:
            type = "Scooter"
        folium.Marker([bike.latitude, bike.longitude], tooltip="Click for more",
                      popup="id:" + str(bike.id) + "\nType:" + type + "\nStreet:" + str(bike.location) +
                            "\nBattery:" + str(bike.battery)).add_to(marker_cluster)
    folium_Map.add_child(marker_cluster)

    if request.method == 'POST':
        form = MoveBike(request.POST)
        form_loc = StartLocation(request.POST)

        if form.is_valid() and form_loc.is_valid():
            bikes = form.cleaned_data.get("bike_id_move")
            current_location = bikes.location
            des_location = form_loc.cleaned_data.get("bike_start_location")
            current_latitude = bikes.latitude
            current_longitude = bikes.longitude
            type = bikes.v_type
            if type == True:
                type = "Bike"
            else:
                type = "Scooter"


            folium.Marker([current_latitude, current_longitude], tooltip="Click for more",
                          popup="id:" + str(bikes.id) + "\nType:" + type + "\nStreet:" + str(current_location) +
                                "\nBattery:" + str(bikes.battery)).add_to(folium_Map)
            folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)

    if 'move' in request.POST:
        move = True
        vehicle_list.objects.filter(id=bikes.id).update(location=des_location.street_id,
                                                        latitude=des_location.latitude,
                                                        longitude=des_location.longitude)

        folium.Marker([des_location.latitude, des_location.longitude], tooltip="Click for more",
                      popup="id:" + str(bikes.id) + "\nType:" + type + "\nStreet:" + str(des_location.street_name) +
                            "\nBattery:" + str(bikes.battery)).add_to(folium_Map)

    folium_Map = folium_Map._repr_html_()
    context = {
        'form': form,
        'move': move,
        'form_loc': form_loc,
        'cur_location': current_location,
        'des_location': des_location,
        'bikes_id': bikes,
        'current_latitude': current_latitude,
        'current_longitude': current_longitude,
        'map': folium_Map,
        'type': type,
    }
    return render(request, "op_move.html", context=context)


@allowed_users(allowed_roles=['admin'])
def operators_repair(request):
    form = RepairBike(request.POST)
    bikes = vehicle_list()
    repair = False
    folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    all_bikes = vehicle_list.objects.all()
    type = bikes.v_type


    marker_cluster = MarkerCluster().add_to(folium_Map)

    for bike in all_bikes:
        type = bike.v_type
        if type == True:
            type = "Bike"
        else:
            type = "Scooter"


        folium.Marker([bike.latitude, bike.longitude], tooltip="Click for more",
                      popup="id:" + str(bike.id) + "\nType:" + type + "\nStreet:" + str(bike.location) +
                            "\nBattery:" + str(bike.battery)).add_to(marker_cluster)

    folium_Map.add_child(marker_cluster)

    if request.method == 'POST':
        form = RepairBike(request.POST)

        if form.is_valid():
            bikes = form.cleaned_data.get("bike_id_repair")

        if request.method == 'POST' and 'repair' in request.POST:
            repair = True
            vehicle_list.objects.filter(id=bikes.id).update(repair=False)

    folium_Map = folium_Map._repr_html_()

    context = {
        'form': form,
        'bikes_id': bikes,
        'repair': repair,
        'map': folium_Map,
        'type': type,
    }
    return render(request, "op_repair.html", context=context)


@allowed_users(allowed_roles=['admin'])
def operators_charge(request):
    form = ChargeBike(request.POST)
    bikes = vehicle_list()
    charge = False
    type = bikes.v_type

    folium_Map = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    all_bikes = vehicle_list.objects.all()

    marker_cluster = MarkerCluster().add_to(folium_Map)

    for bike in all_bikes:
        type = bike.v_type
        if type == True:
            type = "Bike"
        else:
            type = "Scooter"
        folium.Marker([bike.latitude, bike.longitude], tooltip="Click for more",
                      popup="id:" + str(bike.id) + "\nType:" + type + "\nStreet:" + str(bike.location) +
                            "\nBattery:" + str(bike.battery)).add_to(marker_cluster)

    folium_Map.add_child(marker_cluster)

    if request.method == 'POST':
        form = ChargeBike(request.POST)

        if form.is_valid():
            bikes = form.cleaned_data.get("bike_id_charge")

        if request.method == 'POST' and 'charge' in request.POST:
            charge = True
            vehicle_list.objects.filter(id=bikes.id).update(battery=100)

    folium_Map = folium_Map._repr_html_()

    context = {
        'form': form,
        'bikes_id': bikes,
        'charge': charge,
        'map': folium_Map,
        'type': type,
    }
    return render(request, "op_charge.html", context=context)
