from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Hostel, Type, Student, Room


def main_page(request):
    return render(request, 'base.html', {})


def room_list(request):
    rooms_filtered = Room.objects.all()
    request_get_str = ''
    if 'room' in request.GET and request.GET['room'] != '':
        rooms_filtered = rooms_filtered.filter(room_number__contains=request.GET.get('room'))
        request_get_str += 'room='+request.GET['room']
    if 'spaceFrom' in request.GET and request.GET['spaceFrom'] != '':
        rooms_filtered = rooms_filtered.filter(count_place__gte=int(request.GET['spaceFrom']))
        if request_get_str != '':
            request_get_str += '&'
        request_get_str += 'spaceFrom=' + request.GET['spaceFrom']
    if 'spaceTo' in request.GET and request.GET['spaceTo'] != '':
        rooms_filtered = rooms_filtered.filter(count_place__lte=int(request.GET['spaceTo']))
        if request_get_str != '':
            request_get_str += '&'
        request_get_str += 'spaceTo=' + request.GET['spaceTo']
    if 'hostel' in request.GET and request.GET['hostel'] != '' and int(request.GET['hostel']) > -1:
        rooms_filtered = rooms_filtered.filter(hostel_id=int(request.GET['hostel']))
        if request_get_str != '':
            request_get_str += '&'
        request_get_str += 'hostel=' + request.GET['hostel']
    if 'type' in request.GET and request.GET['type'] != '' and int(request.GET['type']) > -1:
        rooms_filtered = rooms_filtered.filter(type_id=int(request.GET['type']))
        if request_get_str != '':
            request_get_str += '&'
        request_get_str += 'type=' + request.GET['type']
    if 'freeSpace' in request.GET and request.GET['freeSpace'] != '':
        if request_get_str != '':
            request_get_str += '&'
        request_get_str += 'freeSpace=' + request.GET['freeSpace']

    ret_rooms = []
    for room in rooms_filtered:
        students = [i.__str__() for i in Student.objects.filter(room_id__exact=room.id)]
        students_str = "Никого нет"
        if len(students) > 0:
            students_str = students[0]
            for s in students[1:]:
                students_str += ', {}'.format(s)

        if 'freeSpace' not in request.GET or request.GET['freeSpace'] == '' or room.count_place-len(students) >= int(request.GET["freeSpace"]):
            ret_rooms.append({'id': room.id,
                              'name': room.__str__(),
                              'room_number': room.room_number,
                              'count_place': room.count_place,
                              'hostel_name': room.hostel.name,
                              'hostel_address': room.hostel.address,
                              'free_space': room.count_place-len(students),
                              'students': students_str,
                              'room_type': room.type.name})


    page = request.GET.get('page')
    if request_get_str != '':
        request_get_str += '&'
    paginator = Paginator(ret_rooms, 5)

    paged_rooms = paginator.get_page(page)

    pages_str_list = [str(i+1) for i in range(paged_rooms.paginator.num_pages)]

    print("request:", request_get_str)
    return render(request, 'room_list.html', {"Hostels": Hostel.objects.all(),
                                                   "Types": Type.objects.all(),
                                                   "Rooms": paged_rooms,
                                                   'request': request.GET,
                                                   'request_str': request_get_str,
                                                   'pages_list': pages_str_list})
