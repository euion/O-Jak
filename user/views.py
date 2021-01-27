from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def login(request):
    if request.method == "POST":
        student_ID = request.POST.get('student_ID', None)
        password = request.POST.get('password', None)
        
        res_data = {}
        if not student_ID and password:
            res_data['error'] = '모든 값을 입력하세요!'
        
        else:
            member = User.objects.get(username=student_ID)
            
            print(member)
            
            if check_password(password, member.password):
                # session!
                request.session['user'] = member
                
                # redirect!
                return redirect('/')
                
            else:
                res_data['error'] = '비밀번호가 다릅니다!'
            
        return render(request, 'User/login.html', res_data)
    
    else:
        return render(request, 'User/login.html')
    

    
def signup(request):
    if request.method == "POST":
        #User 객체
        student_ID = request.POST.get('student_ID', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        
        
        #Profile 객체
        name = request.POST.get('name', None) # 이름
        smoke = request.POST.get('smoke', None) # 흡연유무 1: 유, 0: 무
        if smoke == 'male' :
            smoke = 1
        elif smoke == 'female':
            smoke = 0
            
        gender = request.POST.get('gender', None) # 남/여
        if gender == 'male' :
            gender = 1
        elif gender == 'female':
            gender = 0
        
        tendency = request.POST.get('tendency', None) # 성향
        if tendency == 'male':
            tendency = 1
        elif tendency == 'female':
            tendency = 0
        
        lifetime = request.POST.get('lifetime', None) # 아침형/저녁형
        if lifetime == 'male':
            lifetime = 1
        elif lifetime == 'female':
            lifetime = 0
        
        major = request.POST.get('major', None) # 전공
        age = request.POST.get('age', None) #나이
        religion = request.POST.get('religion', None) #종교
        #labtop = request.POST.get('labtop', None) # 노트북 유무 1: 유, 0: 무
        labtop = int(request.POST.getlist('labtop')[0]) # ++ 0처리는 따로 추가적으로 해주어야함
        
        
        police = 0 # 신고 유무 1: 유, 0: 무
        admin = 0 # 유저 권한 1: 관리자, 0: 사용자
        sleepinghabit = request.POST.get('sleepinghabit', None) # 잠버릇종류
        
        print(student_ID)
        print(password)
        print(re_password)
        print(name)
        print(smoke)
        print(gender)
        print(tendency)
        print(lifetime)
        print(labtop)
        print(age)
        print(age)
        print(sleepinghabit)
        
        res_data = {}
        if not (student_ID and password and re_password):
            res_data['error'] = '모든 값을 입력하세요!'

        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
            print(res_data)
        #elif 학번 필터
        else:
            
            user = User(
                username = student_ID, 
                password = make_password(password)
            )
            
            user.save()
            
            profile = Profile(
                user = user,
                name = name,
                smoke = smoke,
                gender = gender,
                tendency = tendency,
                lifetime = lifetime,
                major = major,
                age = age,
                religion = religion,
                labtop = labtop,
                police = police,
                admin = admin,
                sleepinghabit = sleepinghabit
            )
        
            profile.save()
            
            return redirect('login/')

        return render(request, 'User/signup.html', res_data)
    
    else:
        return render(request, 'User/signup.html')