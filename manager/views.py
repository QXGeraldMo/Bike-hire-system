from datetime import datetime

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from customers.decrators import allowed_users
from customers.models import Order, destination_location, vehicle_list

from plotly.offline import plot
import plotly.graph_objects as go


# Create your views here.
from manager.forms import EnterTimeForm

def MloginPage(request):
    if request.user.is_authenticated:
        return redirect('makequery')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('makequery')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'manager/managerlogin.html', context)


#@login_required(login_url='manager/login')
from manager.models import temp

# def showpage(request):
#     if request.method == 'GET':
#         return render(request, 'manager/managerQuery.html')
#     elif request.method == 'POST':
#         form = EnterTimeForm(request.POST)
#         return render(request, 'manager/managerQuery.html', {form: form})
@allowed_users(allowed_roles=['manager'])
def MakeQuery(request):
    #allorders = Order.objects.all()
    #have = temp.objects.all()
    #form = EnterTimeForm()
    if request.method == 'GET' and not request.GET.get('page'):
        form = EnterTimeForm()
        temp.objects.all().delete()
        return render(request, 'manager/managerQuery.html', {'form': form})
    if request.method == 'POST':
        form = EnterTimeForm(request.POST)
        form.save()
        start = form['start'].value()
        # start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        end = form['end'].value()
        # end = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        allorders = Order.objects.filter(start__gt=start, end__lte=end)
        cur = temp()
        for o in allorders:
            cur.order_id = o.order_id
            cur.v_id = o.v_id
            cur.start = o.start
            cur.end = o.end
            cur.customer = o.customer
            cur.duration = o.duration
            cur.destination = o.destination
            cur.departure = o.departure
            cur.save()
        allorders = temp.objects.all()
        p = request.GET.get('page', 1)
        paginator = Paginator(allorders, 5)
        try:
            pages = paginator.get_page(p)
        except PageNotAnInteger:
            pages = paginator.get_page(1)
        except EmptyPage:
            pages = paginator.get_page(paginator.num_pages)
        context = {'form': form, 'pages': pages}
        return render(request, 'manager/managerQuery.html', context)
    elif request.GET.get('page'):
        form = EnterTimeForm()
        allorders = temp.objects.all()
        p = request.GET.get('page', 1)
        paginator = Paginator(allorders, 5)
        try:
            pages = paginator.get_page(p)
        except PageNotAnInteger:
            pages = paginator.get_page(1)
        except EmptyPage:
            pages = paginator.get_page(paginator.num_pages)
        context = {'form': form, 'pages': pages}
        return render(request, 'manager/managerQuery.html', context)





def view_1(request):
    if request.method == "GET":
        print('get1111111')
        orders = Order.objects.all()
        print(orders)
        destinations = destination_location.objects.all()

        # Generate dictionary
        locations = dict(
            (
                destination.street_name,
                len([n for n in orders.filter(departure=destination)])
            )
            for destination in destinations
        )

        data = [
            go.Bar(x=list(locations.keys()), y=list(locations.values()))
        ]
        layout = {
            'title': 'Place of Departure - Frequency',
            'title_x': 0.5,
            'height': 450,
            'width': 600,
            'xaxis_title': 'Departure',
            'yaxis_title': 'Times',
            'plot_bgcolor': 'black',
        }
        plot_div = plot(
            {'data': data, 'layout': layout}, output_type='div'
        )
        context = {
            'plot_div1': plot_div
        }
    else:
        context = {}
    return render(request, 'manager/managerQuery.html', context=context)



def view_2(request):
    if request.method == "GET":
        print("get22222222")
        orders = Order.objects.all()
        destinations = destination_location.objects.all()
        locations = dict(
            (
                destination.street_name,
                len([n for n in orders.filter(destination=destination)])
            )
            for destination in destinations
        )

        data = [
            go.Bar(x=list(locations.keys()), y=list(locations.values()))
        ]
        layout = {
            'title': 'Destination - Frequency',
            'title_x': 0.5,
            'height': 450,
            'width': 600,
            'xaxis_title': 'Destination',
            'yaxis_title': 'Times',
            'plot_bgcolor': 'black',
        }
        plot_div = plot(
            {'data': data, 'layout': layout}, output_type='div'
        )

        context = {
            'plot_div2': plot_div
        }
    else:
        context = {}
    return render(request, 'manager/managerQuery.html', context=context)




def view_3(request):
    orders = Order.objects.all()

    date_hour = []
    for order in orders:
        date_hour.append(order.start.hour)
    d = {}
    for i in range(0, 24):
        d[i] = 0
    count = 0
    for i in set(date_hour):
        for j in date_hour:
            if i == j:
                count += 1
        d[i] = count
        count = 0
    print(d)

    data = [
        go.Line(x=list(d.keys()), y=list(d.values()))
    ]

    xaxis = {
        'showgrid': False,
        'zeroline': True,
        'nticks': 24,
    }
    layout = {
        'title': 'Period - Frequency',
        'title_x': 0.5,
        'height': 450,
        'width': 600,
        'xaxis': xaxis,
        'xaxis_title': 'Period',
        'yaxis_title': 'Frequencies',
        'plot_bgcolor': 'black',
    }

    plot_div = plot(
        {'data': data, 'layout': layout}, output_type='div'
    )
    # plot_div.yaxis.set_minor_locator(plot_div.MultipleLocator(1))

    context = {
        'plot_div3': plot_div
    }
    #return render(request, 'home.html', context=context)
    return render(request, 'manager/managerQuery.html', context=context)

def view_4(request):
    vehicles = vehicle_list.objects.all()
    destinations = destination_location.objects.all()

    v = []
    for vehicle in vehicles:
        v.append(str(vehicle.location))

    locations = []
    for destination in destinations:
        locations.append(destination.street_name)

    d = {}
    count = 0
    for i in sorted(locations):
        for j in sorted(v):
            if j == i:
                count += 1
        d[i] = count
        count = 0
    print(d)
    '''
    c = sorted(d.keys(), key=lambda word: word.lower())
    print(c)
    '''

    data = [
        go.Bar(x=list(d.keys()), y=list(d.values()))
    ]
    layout = {
        'title': 'Location - Vehicle',
        'title_x': 0.5,
        'height': 450,
        'width': 600,
        'xaxis_title': 'Locations',
        'yaxis_title': 'Vehicles',
        'plot_bgcolor': 'black',
    }

    plot_div = plot(
        {'data': data, 'layout': layout}, output_type='div'
    )
    context = {
        'plot_div4': plot_div
    }
    return render(request, 'manager/managerQuery.html', context=context)

def view_5(request):
    vehicles = vehicle_list.objects.all()

    v = []
    for vehicle in vehicles:
        v.append(vehicle.battery)

    d = {'Needs Charging': 0, 'Insufficient Electricity': 0, 'Sufficient Electricity': 0, 'Fully Charged': 0}
    for i in v:
        if i <= 20:
            d['Needs Charging'] += 1
        elif 20 < i <= 40:
            d['Insufficient Electricity'] += 1
        elif 40 < i <= 80:
            d['Sufficient Electricity'] += 1
        elif 80 < i <= 100:
            d['Fully Charged'] += 1
        else:
            print("Error!")

    color = ['#FF4500', '#FFA500', '00FFFF', '00FF00']

    data = [
        go.Pie(labels=list(d.keys()),
               values=list(d.values()),
               pull=[0.2, 0.1, 0, 0],
               marker=dict(
                   colors=color,
                   line=dict(color='#000000', width=0.5)
               )
               )
    ]
    layout = {
        'title': 'Vehicle Battery Status',
        'title_x': 0.3,
        'height': 450,
        'width': 600,
    }

    plot_div = plot(
        {'data': data, 'layout': layout}, output_type='div'
    )
    context = {
        'plot_div5': plot_div
    }
    return render(request, 'manager/managerQuery.html', context=context)



def managerlogout(request):
    logout(request)
    return redirect('index')






