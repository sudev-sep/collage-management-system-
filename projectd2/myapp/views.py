from django.shortcuts import render
from .models import Department, Student, Teacher, User,Notes
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect


def home(request):
    return render(request, 'home.html')

from django.shortcuts import get_object_or_404

def register_h(request):
    if request.method == "POST":
        FIRSTNAME = request.POST['FIRSTNAME']
        LASTNAME = request.POST['LASTNAME']
        EMAIL = request.POST['EMAIL']
        ADDRESS = request.POST['ADDRESS']
        PHONE_NUMBER = request.POST['PHONE_NUMBER']
        USERNAME = request.POST['USERNAME']
        PASSWORD = request.POST['PASSWORD']
        DEPARTMENT = request.POST['department']
        PICTURE = request.FILES.get('PICTURE')
        usertype = request.POST['usertype']

        department = get_object_or_404(Department, id=DEPARTMENT)
        
        if usertype == "Student":
            GUARDIAN = request.POST['GUARDIAN']

            new_user = User.objects.create_user(
                first_name=FIRSTNAME,
                last_name=LASTNAME,
                email=EMAIL,
                username=USERNAME,
                password=PASSWORD,
                address=ADDRESS,
                phone_number=PHONE_NUMBER,
                department=department, 
                picture=PICTURE,
                usertype="Student",
                is_active=False
            )
            Student.objects.create(student_id=new_user, guardian=GUARDIAN)

        elif usertype == "Teacher":
            SALARY = request.POST['SALARY']
            EXPERIENCE = request.POST['EXPERIENCE']

            new_user = User.objects.create_user(
                first_name=FIRSTNAME,
                last_name=LASTNAME,
                email=EMAIL,
                username=USERNAME,
                password=PASSWORD,
                address=ADDRESS,
                phone_number=PHONE_NUMBER,
                department=department, 
                picture=PICTURE,
                usertype="Teacher",
                is_active=False,
                is_staff=False
            )
            Teacher.objects.create(teacher_id=new_user, salary=SALARY, experience=EXPERIENCE)

        return HttpResponse("<script>alert('Registration successful');window.location.href='/login';</script>")
    departments = Department.objects.all()
    return render(request, 'register_h.html', {"departments": departments})



def admin_h(request):
    return render(request,'admin_h.html')  

def teacher_h(request):
    if request.user.usertype != "Teacher":
        return HttpResponseForbidden("Access denied. Teacher only.")
    teacher = Teacher.objects.get(teacher_id=request.user.id)
    student=Student.objects.all()
    pics = request.FILES.get('PICTURE')


    return render(request, 'teacher_h.html', {'teacher': teacher,'students':student})


def student_h(request):
    if request.user.usertype != "Student":
        return HttpResponseForbidden("Access denied. Student only.")
    
    student = Student.objects.get(student_id=request.user.id)
    return render(request, 'student_h.html', {'student': student})


def login_view(request):
     if request.method=="POST":
        USERNAME=request.POST['USERNAME']
        PASSWORD=request.POST['PASSWORD']
        userpass=authenticate(request,username=USERNAME,password=PASSWORD)
        if userpass is not None and userpass.is_superuser==1:
            return redirect('admin_h')
        elif userpass is not None and userpass.is_staff==1:
            login(request,userpass)
            request.session['teacher_id']=userpass.id
            return redirect('teacher_h')
        elif userpass is not None and userpass.is_active==1:
            login(request,userpass)
            request.session['student_id']=userpass.id
            return redirect('student_h')
        else:
            return HttpResponse('invalid login')
     else:
        return render(request, 'login.html')
     
def teacher_admin(request):
    teachers = Teacher.objects.select_related('teacher_id').all()
    return render(request, 'teacher_admin.html', {
        'teachers': teachers,  
    })

def student_admin(request):
    students = Student.objects.select_related('student_id').all()
    return render(request, 'student_admin.html', {
        'students': students,})


def logout_view(request):
    logout(request)
    return redirect('home')


def delete_s(request,id):
    x=Student.objects.get(id=id)
    user_id=x.student_id.id
    x.delete()
    user=User.objects.get(id=user_id)
    user.delete()
    return HttpResponse("<script> alert('deleted'); window.location.href='/student_admin';</script>")

def delete_t(request,id):
    x=Teacher.objects.get(id=id)
    user_id=x.teacher_id.id
    x.delete()
    user=User.objects.get(id=user_id)
    user.delete()
    return HttpResponse("<script> alert('deleted'); window.location.href='/teacher_admin';</script>")

def approve_student(request, id):
    stud = Student.objects.select_related('student_id').get(id=id)
    stud.student_id.is_active = True
    stud.student_id.save()
    return redirect('student_admin')

def approve_teacher(request, id):
    teach = Teacher.objects.select_related('teacher_id').get(id=id)
    teach.teacher_id.is_staff = True
    teach.teacher_id.is_active = True
    teach.teacher_id.save()
    return redirect('teacher_admin')


def add_department(request):
    if request.method == "POST":
        dept_name = request.POST['dept_name']
        Department.objects.create(department=dept_name)
        return redirect('admin_h')  
    return render(request, 'add_department.html')


def view_students (request):
    students = Student.objects.select_related('student_id', 'student_id__department').all().order_by("student_id__department")
    return render(request, 'view_students.html', {'students': students})


def teacher_edit(request, id):
    teacher = get_object_or_404(Teacher.objects.select_related("teacher_id"), id=id)
    user = teacher.teacher_id
    department = Department.objects.all() 
    
    if not teacher:
        return redirect("teacher_h")   
    if request.method == "POST":
        user.first_name = request.POST["FIRSTNAME"]
        user.last_name = request.POST["LASTNAME"]
        user.email = request.POST["EMAIL"]
        user.address = request.POST["ADDRESS"]
        user.phone_number = request.POST["PHONE_NUMBER"]
        teacher.salary = request.POST["SALARY"]
        teacher.experience = request.POST["EXPERIENCE"]
        if 'PICTURE' in request.FILES:
            user.picture = request.FILES['PICTURE']
        user.department = Department.objects.get(id=request.POST["department"])

        user.save()
        teacher.save()
        return redirect("teacher_h")   

    return render(request, "teacher_edit.html", {"teacher": teacher,"departments": department})


def notes(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("file")
        if title and file:
            Notes.objects.create(teacher=teacher, title=title, file=file)
            return redirect("teacher_h")  

    return render(request, "notes.html", {"teacher": teacher, "notes": teacher.notes.all()})



def student_edit(request, id):
    student = get_object_or_404(Student.objects.select_related("student_id"), id=id)
    user = student.student_id
    department = Department.objects.all() 
    
    if not student:
        return redirect("student_h")   
    if request.method == "POST":
        user.first_name = request.POST["FIRSTNAME"]
        user.last_name = request.POST["LASTNAME"]
        user.email = request.POST["EMAIL"]
        user.address = request.POST["ADDRESS"]
        user.phone_number = request.POST["PHONE_NUMBER"]
        student.guardian = request.POST["GUARDIAN"]
        if 'PICTURE' in request.FILES:
            user.picture = request.FILES['PICTURE']
        user.department = Department.objects.get(id=request.POST["department"])

        user.save()
        student.save()
        return redirect("student_h")   

    return render(request, "student_edit.html", {"student": student,"departments": department})


def view_teachers(request):
    teacher = Teacher.objects.select_related('teacher_id', 'teacher_id__department').all().order_by("teacher_id__department")
    return render(request, 'view_teachers.html', {'teachers': teacher})


def view_notes(request):
    notes = Notes.objects.select_related('teacher', 'teacher__teacher_id').all().order_by('-uploaded_at')
    return render(request, 'view_notes.html', {'notes': notes})


def index(request):
    return render(request, 'index.html')