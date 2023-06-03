from django.shortcuts import render, redirect
import folium
from .models import vehicle_list, destination_location, Order
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random as rd
from datetime import datetime
from io import BytesIO
from customers.utils import check_code
from django.http import HttpResponse
from folium.plugins import MarkerCluster
from .decrators import unauthenticated_user


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('show_all_vehicles')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'customers/registerCustomer.html', context)


def image_code(request):
    img, code_string = check_code()
    # request.session['image_code'] = code_string
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


# @unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('show_all_vehicles')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('show_all_vehicles')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'customers/loginCustomer.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'customers/index.html')


@login_required(login_url='login')
def show_all_vehicles(request):
    m = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    dep_loc_list = []

    if request.method == 'POST':
        c_place = request.POST.get('v_choose')
        c_destination = request.POST.get('v_des')
        print(c_place)
        print(c_destination)
        # departure_name = destination_location.objects.get(street_name=c_place)
        # bike_id = vehicle_list.objects.filter(location=departure_name.id)
        street_key = destination_location.objects.get(street_name=c_place)
        vehicles = vehicle_list.objects.filter(location=street_key.street_id)
        print(vehicles[0])
        # type = vehicles[0].v_type
        # if type == True:
        #     type = "Bike"
        # else:
        #     type = "Electric scooter"

        # for i in bike_id:
        #     print(bike_id)

        destination1 = destination_location.objects.get(street_name=c_destination)

        create_order = Order(order_id=rd.randint(1, 100), departure=c_place,
                             destination=c_destination, v_id=vehicles[0])
        create_order.save()

        # vehicle_list.objects.filter(pk=bike_id.id).update(location=destination1)
        # vehicle_list.objects.filter(pk=bike_id.id).update(latitude=destination1.latitude)
        # vehicle_list.objects.filter(pk=bike_id.id).update(longitude=destination1.longitude)
        # vehicle_list.objects.filter(pk=bike_id.id).update(status=True)

        vehicle_list.objects.filter(pk=vehicles[0].id).update(location=destination1.street_id,
                                                              latitude=destination1.latitude,
                                                              longitude=destination1.longitude,
                                                              status=True)

        request.session["order_id"] = create_order.order_id
        request.session['departure'] = c_place
        request.session['destination'] = destination1.street_name
        return redirect('hire_vehicle')

    v_list = vehicle_list.objects.all()
    d_list = destination_location.objects.all()


    for v in v_list:
        if not v.repair:
            if v.v_type:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(
                                  v.id) + "\nType:Bike" + "\nStreet:" + str(v.location) + "\nBattery:" + str(
                                  v.battery)).add_to(marker_cluster)
            else:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(v.id) + "\nType:Scooter" + "\nStreet:" + str(v.location)).add_to(marker_cluster)
            dep_loc_list.append(str(v.location))

    m.add_child(marker_cluster)
    # Get Html Representation of Map object
    m = m._repr_html_()
    context = {'m': m, 'v_list': v_list, 'd_list': d_list, 'dep_loc_list':dep_loc_list}
    return render(request, 'customers/show_all_vehicles.html', context)


def hire_vehicle(request):
    departure = request.session['departure']
    destination = request.session['destination']
    order_id = request.session["order_id"]
    m1 = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m1)
    now_time = datetime.now(timezone.utc)
    total_hired_time = now_time
    price = 0.0
    minutes = 0.0
    order1 = Order.objects.get(order_id=order_id)
    vehicle = order1.v_id
    vehicle = vehicle_list.objects.get(id=vehicle.id)
    vehicle_id = vehicle.id
    soc = vehicle.battery

    if request.method == 'POST' and 'return_bike' in request.POST:
        end_time = datetime.now(timezone.utc)
        order1 = Order.objects.get(order_id=order_id)
        s_time = order1.start
        print(s_time)
        print(end_time)
        total_hired_time = end_time - s_time
        Order.objects.filter(order_id=order_id).update(end=str(end_time))
        Order.objects.filter(order_id=order_id).update(duration=str(total_hired_time))
        print(total_hired_time)
        hours = total_hired_time.total_seconds() / (60 * 60)
        total_price = round(hours * 10, 3)
        print(order1.v_id)
        # vehicle = order1.v_id
        # vehicle = vehicle_list.objects.get(id=vehicle.id)
        soc = vehicle.battery - hours * 20
        # vehicle_id = vehicle.id

        if soc > 0:
            vehicle_list.objects.filter(id=order1.v_id.id).update(battery=soc)
        else:
            vehicle_list.objects.filter(id=order1.v_id.id).update(battery=0)

        request.session['duration'] = str(total_hired_time)
        request.session['order_id'] = order_id
        request.session['total_price'] = total_price
        return redirect('duration_price')

    if request.method == 'POST' and 'report' in request.POST:
        order1 = Order.objects.get(order_id=order_id)
        v_damage_id = order1.v_id.id
        vehicle_list.objects.filter(id=v_damage_id).update(repair=True)
        return redirect('report')

    v_list = vehicle_list.objects.all()
    for v in v_list:
        if v.status:
            if v.v_type:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(
                                  v.id) + "\nType:Bike" + "\nStreet:" + str(v.location) + "\nBattery:" + str(
                                  v.battery)).add_to(marker_cluster)
            else:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(v.id) + "\nType:Scooter" + "\nStreet:" + str(v.location)).add_to(marker_cluster)

    # Get Html Representation of Map object
    m1.add_child(marker_cluster)
    m1 = m1._repr_html_()
    context = {'m1': m1, 'total_hire_time': total_hired_time, 'departure': departure, 'destination': destination,
               'vehicle_id': vehicle_id, 'SOC': soc}
    return render(request, 'customers/hirebike.html', context)


def report(request):
    if request.method == "POST":
        return redirect('show_all_vehicles')
    return render(request, 'customers/report.html')


def duration_price(request):
    duration = request.session['duration']
    order_id = request.session['order_id']
    total_price = request.session['total_price']

    order1 = Order.objects.get(order_id=order_id)
    bike_id = order1.v_id.id
    current_bike = vehicle_list.objects.get(id=bike_id)
    check_repair = current_bike.repair

    vehicle = order1.v_id
    vehicle = vehicle_list.objects.get(id=vehicle.id)
    vehicle_id = vehicle.id
    soc = vehicle.battery

    m2 = folium.Map(location=[55.873543, -4.289058], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m2)
    v_list = vehicle_list.objects.all()
    for v in v_list:
        if v.status:
            if v.v_type:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(
                                  v.id) + "\nType:Bike" + "\nStreet:" + str(v.location) + "\nBattery:" + str(
                                  v.battery)).add_to(marker_cluster)
            else:
                folium.Marker([v.latitude, v.longitude], tooltip="Click for more",
                              popup="id:" + str(v.id) + "\nType:Scooter" + "\nStreet:" + str(v.location)).add_to(marker_cluster)
    m2.add_child(marker_cluster)
    m2 = m2._repr_html_()

    if request.method == 'POST':
        request.session['total_price'] = total_price
        return redirect('payment')

    o1 = Order.objects.get(order_id=order_id)
    v_id = o1.v_id
    print(v_id)
    vehicle_list.objects.filter(id=v_id.id).update(status=False)

    context = {'m2': m2, 'duration': duration, 'total_price': total_price, 'SOC' : soc}
    return render(request, 'customers/duration_price.html', context)


def payment(request):
    total_price = request.session['total_price']
    if request.method == "POST":
        card_number = request.POST.get('card_number')
        print(card_number)

        # Credit card number verification
        digits = [int(x) for x in reversed(card_number)]
        even_digits = [d * 2 for d in digits[1::2]]
        even_digits = [d // 10 + d % 10 for d in even_digits]
        even_sum = sum(even_digits)
        odd_sum = sum(digits[::2])
        if (odd_sum + even_sum) % 10 == 0:
            messages.info(request, "Payment Successful!! ")
            messages.info(request, 'Thank you! Your payment is complete')
        else:
            messages.info(request, "Credit card number is invalid")

    context = {'total_price': total_price}
    return render(request, 'customers/payment.html', context)
