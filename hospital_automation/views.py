from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
from datetime import date
from hospital_automation.serializers import PatientSerializer
from django.contrib.auth.decorators import login_required
from django.db.models import Count

counter = 1
counter_for_dispensary = 1
counter_for_test = 1
alloted_doctor = ""


@login_required
def doctors(request):
    user_group = request.user.groups.values_list('name', flat=True)
    if not user_group:
        return redirect('accounts/login')
    if user_group[0] == 'Doctor':
        patient = list(Patient.objects.values().filter(is_seen=False, assigned_doctor=(
            request.user.first_name + " " + request.user.last_name)))
        print(request.user.username)
        return render(request, 'incoming_patient.html', {'incoming_patient': patient})
    return redirect('index')


def receive_patient(request):
    global counter
    global alloted_doctor
    if request.method == 'GET' and counter == 0 and alloted_doctor == (request.user.first_name + " " + request.user.last_name):
        incoming_patient = list(Patient.objects.values().filter(is_seen=False, assigned_doctor=(
            request.user.first_name + " " + request.user.last_name)).order_by('-id')[:1])

        serializer = PatientSerializer(
            incoming_patient, many=True, context={'request': request})
        counter = 1
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)


@login_required
def reception(request):
    user_group = request.user.groups.values_list('name', flat=True)
    if not user_group:
        return redirect('accounts/login')
    if(user_group[0] == 'Receptionist'):
        global counter
        global alloted_doctor
        if request.method == 'GET':
            return render(request, 'reception.html', {})
        elif request.method == 'POST':
            first_name = request.POST['First Name']
            last_name = request.POST['Last Name']
            father_name = request.POST['Father name']
            address = request.POST['Address']
            city = request.POST['City']
            state = request.POST['State']
            zip_code = request.POST['Postal/ZIP code']
            country = request.POST['Country']
            country_code = request.POST['country code']
            contact_number = request.POST['Contact Number']
            date = request.POST['todays date']
            problem = request.POST['problem']
            alloted_doctor = request.POST['Doctor name']
            Patient.objects.create(first_name=first_name, last_name=last_name, guardian_name=father_name, address=address,
                                   city=city, state=state, zip_code=zip_code, country=country,
                                   country_code=country_code, phone_number=contact_number, date=date, problem_name=problem, assigned_doctor=alloted_doctor)
            counter = 0
            return redirect('reception')
    return redirect('index')


@csrf_exempt
def autocomplete(request, id):
    if request.is_ajax():
        queryset = User_type.objects.filter(
            specialization__startswith=request.GET['search'])

        list = []

        for problem in queryset:
            if problem.specialization not in list:
                list.append(problem.specialization)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'reception.html', {})


def prescriptions(request, patient_id):
    patient_prescriptions = Patient.objects.values().filter(id=patient_id)
    return render(request, 'patient_prescriptions.html', {'prescriptions': patient_prescriptions})


def load_doctors(request):
    if request.is_ajax():
        problem = request.GET.get('problem')
        doctor_id = User_type.objects.values(
            'user_id').filter(specialization=problem)
        doctors = User.objects.values(
            'first_name', 'last_name').filter(id__in=doctor_id)
        list = []
        for doctor in doctors:
            list.append(doctor['first_name'] + " " + doctor['last_name'])

        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'reception.html', {})


def send_prescriptions(request, patient_id):
    global counter_for_dispensary
    global counter_for_test
    diagnosis = request.POST['diagnosis']
    blood_pressure = request.POST['bp']
    weight = request.POST['weight']
    sugar = request.POST['sugar']
    list_of_medicines = request.POST.getlist('medicine')
    morning_intake = request.POST.getlist('checkbox1[]')
    afternoon_intake = request.POST.getlist('checkbox2[]')
    evening_intake = request.POST.getlist('checkbox3[]')
    tests = request.POST['tests']
    medicine_intake = 1
    for medicine in list_of_medicines:
        Patient_history.objects.create(date=date.today(), diagnosis=diagnosis, blood_pressure=blood_pressure, weight=weight,
                                       sugar=sugar, medicine=medicine, morning_intake=True if str(
                                           medicine_intake) in morning_intake else False,
                                       afternoon_intake=True if str(medicine_intake) in afternoon_intake else False, evening_intake=True if str(medicine_intake) in evening_intake else False,
                                       days=1, tests=tests, user_id=patient_id)
        medicine_intake = medicine_intake + 1
    patient = Patient.objects.get(id=patient_id)
    patient.is_seen = True
    patient.save()
    counter_for_dispensary = 0
    if tests is not "":
        counter_for_test = 0
    return redirect('doctors')


def doctor_details(request):

    doctor_id = User_type.objects.values('user_id').filter(flag=1)
    doctor_specializations = User_type.objects.values(
        'specialization').filter(flag=1)
    doctors_name = User.objects.values(
        'first_name', 'last_name').filter(id__in=doctor_id)
    doctors_list = []

    for name in range(0, len(doctors_name)):
        doctors_display_details = {}
        doctors_display_details['first_name'] = doctors_name[name]['first_name']
        doctors_display_details['last_name'] = doctors_name[name]['last_name']
        doctors_display_details['specialization'] = doctor_specializations[name]['specialization']
        doctors_list.append(doctors_display_details)
    return render(request, 'doctor_details.html', {'doctors_list': doctors_list})


def helpers(request):
    helper_details = Helpers_nurses.objects.values()
    return render(request, 'helpers.html', {'helper_details': helper_details})


def index(request):
    if request.user.is_authenticated:
        user_group = request.user.groups.values_list('name', flat=True)
        if not user_group:
            return redirect('accounts/login')
        else:
            if user_group[0] == 'Receptionist':
                return redirect('reception')
            elif user_group[0] == 'Doctor':
                return redirect('doctors')
            elif user_group[0] == 'Dispensary':
                return redirect('dispensary')
            else:
                return redirect('test')
    return redirect('accounts/login')


@login_required
def patient_to_dispensary(request):
    user_group = request.user.groups.values_list('name', flat=True)
    if not user_group:
        return redirect('accounts/login')
    if user_group[0] == 'Dispensary':
        patient_ids = Patient_history.objects.values(
            'user_id').distinct().filter(is_done_with_dispensary=False)
        patient_names = list(Patient.objects.values(
            'id', 'first_name', 'last_name').filter(id__in=patient_ids))
        return render(request, 'dispensary.html', {'incoming_patient': patient_names})
    return redirect('index')


@login_required
def receive_incoming_patient_to_dispensary(request):
    global counter_for_dispensary
    if request.method == 'GET' and counter_for_dispensary == 0:
        patient_ids = Patient_history.objects.values(
            'user_id').distinct().filter(is_done_with_dispensary=False)
        patient_names = list(Patient.objects.values('id', 'first_name', 'last_name', 'guardian_name',
                                                    'problem_name', 'assigned_doctor').filter(id__in=patient_ids).order_by('-id')[:1])
        serializer = PatientSerializer(
            patient_names, many=True, context={'request': request})
        counter_for_dispensary = 1
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)


@login_required
def medication_of_patient(request, patient_id):
    medication = Patient_history.objects.values(
        'medicine', 'morning_intake', 'afternoon_intake', 'evening_intake').filter(user_id=patient_id)
    patient_and_doctor_name = Patient.objects.values(
        'first_name', 'last_name', 'assigned_doctor').filter(id=patient_id)
    return render(request, 'medication.html', {'medication': medication, 'patient_and_doctor_name': patient_and_doctor_name})


@login_required
def is_done_with_patient(request, patient_id):
    patient_history = Patient_history.objects.values().filter(user_id=patient_id)
    patient_history.update(is_done_with_dispensary=True)
    return redirect('dispensary')


@login_required
def patient_records(request):
    patients = Patient.objects.all()
    print(patients)
    return render(request, 'patient_records.html', {'patients': patients})


@login_required
def patient_detail(request, patient_id):
    records = Patient_history.objects.filter(user_id=patient_id)
    patient_info = Patient.objects.filter(id=patient_id)
    return render(request, 'patient_detail.html', {'records': records, 'patient_info': patient_info[0]})


@login_required
def test(request):
    user_group = request.user.groups.values_list('name', flat=True)
    if not user_group:
        return redirect('accounts/login')
    if user_group[0] == 'Test':
        patient_ids = Patient_history.objects.values('user_id').distinct().filter(
            is_done_with_test=False).exclude(tests__exact='')
        print(patient_ids)
        patient_names = list(Patient.objects.values('id', 'first_name', 'last_name', 'guardian_name',
                                                    'problem_name', 'assigned_doctor').filter(id__in=patient_ids).order_by('id'))
        return render(request, 'test.html', {'incoming_patient': patient_names})
    return redirect('index')


@login_required
def receive_incoming_patient_for_test(request):
    global counter_for_test
    if request.method == 'GET' and counter_for_test == 0:
        patient_ids = Patient_history.objects.values('user_id').distinct().filter(
            is_done_with_test=False).exclude(tests__exact='')
        patient_names = list(Patient.objects.values('id', 'first_name', 'last_name',
                                                    'guardian_name', 'problem_name', 'assigned_doctor').filter(id__in=patient_ids)[:1])
        serializer = PatientSerializer(
            patient_names, many=True, context={'request': request})
        counter_for_test = 1
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)


@login_required
def patient_to_test(request, patient_id):
    user_group = request.user.groups.values_list('name', flat=True)
    if not user_group:
        return redirect('accounts/login')
    if user_group[0] == 'Test':
        test_for_patient = Patient_history.objects.values(
            'tests').distinct().filter(user_id=patient_id).exclude(tests__exact='')
        patient_and_doctor_name = Patient.objects.values(
            'first_name', 'last_name', 'assigned_doctor').filter(id=patient_id)
        return render(request, 'test_for_particular_patient.html', {'test_for_patient': test_for_patient, 'patient_and_doctor_name': patient_and_doctor_name})
    return redirect('index')


def patient_is_done_with_test(request, patient_id):
    patient_history = Patient_history.objects.values().filter(user_id=patient_id)
    patient_history.update(is_done_with_test=True)
    return redirect('test')


def statistics(request):
    number_of_patient_seen_by_doctors = Patient.objects.values(
        "assigned_doctor").annotate(Count("assigned_doctor")).order_by('assigned_doctor')
    doctors_seen_details = {}
    for patients in number_of_patient_seen_by_doctors:
        doctors_seen_details[str(patients['assigned_doctor'])
                             ] = patients['assigned_doctor__count']
    return render(request, 'statistics.html', {'doctors_seen_details': doctors_seen_details})


@csrf_exempt
def autocomplete_medicine(request, id):
    if request.is_ajax():
        queryset = Medicines.objects.filter(
            name__startswith=request.GET['search'])

        list = []

        for problem in queryset:
            if problem.name not in list:
                list.append(problem.name)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'patient_prescriptions.html', {})


def error_404_view(request, exception):
    return render(request, 'errors/404.html')
