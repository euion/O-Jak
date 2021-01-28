from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

question_list = {
    '당신의 성별은 무엇인가요?': dict(enumerate(['남자', '여자'])),
    '룸메이트가 흡연하는 분이어도 괜찮나요?': dict(enumerate(['흡연', '비흡연'])),
    '외향적인 사람과 내향적인 사람 중에 어떤 사람이 편하신가요?': dict(enumerate(['외향적', '내향적'])),
    '아침과 저녁 중에 언제 활동하는 사람을 생각하시나요?': dict(enumerate(['아침형', '저녁형'])),
    '종교를 가지고 있나요?': dict(enumerate(['네', '아니오'])),
    '노트북을 가지고 있나요?': dict(enumerate(['네', '아니오'])),
    '어떤 기숙사 방을 신청하실 건가요?': dict(enumerate(['일반동 2인실(578)', '신축동 숲전망(M) 2인실(1,234)', '신축동 캠퍼스전망(A) 2인실(1,282)', '신축동 캠퍼스전망(S) 2인실(1,330)'])),
    '잠버릇이 있나요?': dict(enumerate(['네', '아니오']))
}

def login(request):
    if not request.session.get('name'):
        if request.method == "POST":
            student_ID = request.POST.get('student_ID', None)
            password = request.POST.get('password', None)
            
            res_data = {}
            if not student_ID and password:
                res_data['error'] = '모든 값을 입력하세요!'
            
            else:
                member = User.objects.get(username=student_ID)
                
                member_profile = Profile.objects.filter(user=member)
                print(member_profile[0])
                
                if check_password(password, member.password):
                    # session!
                    request.session['user'] = member.id
                    request.session['name'] = member_profile[0].name
                    
                    # redirect!
                    return redirect('/main/home')
                    
                else:
                    res_data['error'] = '비밀번호가 다릅니다!'
                
            return render(request, 'User/login.html', res_data)
        
        else:
            return render(request, 'User/login.html')
    else:
        return redirect('/main/home')

def logout(request):
    if 'user' in request.session and 'name' in request.session:
        request.session.clear()
    return redirect('/main/home')

def signup_question(request):
    if 'signup_name' in request.session and 'signup_student_ID' in request.session and 'signup_student_Number' in request.session and 'signup_password' in request.session and 'signup_major' in request.session and 'signup_age' in request.session:
        if request.method == "POST":
            #User 객체
            '''
            name = request.POST.get('name', None)
            student_ID = request.POST.get('student_ID', None)
            student_Number = request.POST.get('student_Number', None)
            password = request.POST.get('password', None)
            '''

            name = request.session['signup_name']
            signup_student_ID = request.session['signup_student_ID']
            #학번
            student_Number = request.session['signup_student_Number']
            password = request.session['signup_password']

            #전공
            major = request.session['signup_major']

            #나이
            age = request.session['signup_age']

            #Profile 객체
            gender = request.POST.get('gender', None) # 남/여
            # answer.. '남자', '여자'
            if gender == "남자":
                gender = 1
            elif gender == "여자":
                gender = 0

            smoke = request.POST.get('smoke', None) # 흡연유무 1: 유, 0: 무
            # answer.. '흡연', '비흡연'
            if smoke == '흡연':
                smoke = 1
            elif smoke == '비흡연':
                smoke = 0
            
            tendency = request.POST.get('tendency', None) # 성향
            # answer.. '외향적', '내향적'
            if tendency == '외향적':
                tendency = 1
            elif tendency == '내향적':
                tendency = 0
            
            lifetime = request.POST.get('lifetime', None) # 아침형/저녁형
            # answer.. '아침형', '저녁형'
            if lifetime == '아침형':
                lifetime = 1
            elif lifetime == '저녁형':
                lifetime = 0

            religion = request.POST.get('religion', None) #종교
            # answer.. '네', '아니오'

            labtop = request.POST.get('labtop', None) # 노트북 유무 1: 유, 0: 무
            #labtop = int(request.POST.getlist('labtop')[0]) # ++ 0처리는 따로 추가적으로 해주어야함
            # answer.. '네', '아니오'
            if labtop == '네':
                labtop = 1
            elif labtop == '아니오':
                labtop = 0

            #room ,test
            room = request.POST.get('room', None) # 잠버릇종류
            
            print(room)
            
            sleepinghabit = request.POST.get('sleepinghabit', None) # 잠버릇종류
            # answer.. '네', '아니오'
            print(sleepinghabit)

            #default 상황
            police = 0 # 신고 유무 1: 유, 0: 무
            admin = 0 # 유저 권한 1: 관리자, 0: 사용자

            res_data = {}
            if not (name):
                res_data['error'] = '모든 값을 입력하세요!'
            #elif 학번 필터
            else:
                
                user = User(
                    username = signup_student_ID, 
                    password = make_password(password)
                )
                
                user.save()
                
                profile = Profile(
                    user = user,
                    name = name,
                    student_ID = student_Number,
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
                
                return redirect('/user/login')


            return render(request, '/user/signup_quest', res_data)
        else:
            question_keylist = list(question_list.keys())

            print(question_keylist[0])

            return render(request, 'Question/signup_quest.html', {'question_keylist': question_keylist, 'question_list': question_list, 'question_keylist_value':len(question_keylist)})
    else:
        #알람 잘못된 접근입니다.
        return redirect('/main/home')
        

def signup(request):
    if request.method == "POST":
        #User 객체
        name = request.POST.get('name', None)
        student_ID = request.POST.get('student_ID', None)
        student_Number = request.POST.get('student_Number', None)
        major = request.POST.get('major', None)
        age = request.POST.get('age', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}
        if not (name and student_ID and password and student_Number):
            res_data['error'] = '모든 값을 입력하세요'

            return render(request, 'User/signup.html', res_data)

        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
            
            return render(request, 'User/signup.html', res_data)

        request.session['signup_name'] = name
        request.session['signup_student_ID'] = student_ID
        request.session['signup_major'] = major
        request.session['signup_student_Number'] = student_Number
        request.session['signup_password'] = password
        request.session['signup_age'] = age
        
        #return render(request, 'Question/signup_quest.html', res_data)
        return redirect('/user/signup_quest')
        #return render(request, 'Question/signup_quest.html', res_data)
        return redirect('/user/signup_quest')
        #return render(request, 'Question/signup_quest.html', res_data)
        return redirect('/user/signup_quest')
        #return render(request, 'Question/signup_quest.html', res_data)
        return redirect('/user/signup_quest')
    
    else:
        return render(request, 'User/signup.html')
