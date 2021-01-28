from django.shortcuts import render,redirect
from django.template.defaulttags import register
from user.models import Profile
import operator

# Create your views here.

# 질문의 종류 배열로
'''
질문
1. 룸메이트가 흡연하는 분이어도 괜찮나요?
2. 외향적인 사람과 내향적인 사람 중에 어떤 사람이 편하신가요?
3. 아침과 저녁 중에 언제 활동 하는 사람을 생각하시나요?
4. 학교를 언제 들어온 사람이 더 편한가요?
5. 학과는 같은 사람? 아니면 다른 학과?
6. 나이는 어떤 사람이 룸메로써 좋은가요?
7. 종교를 가진 사람 어때요?
8. 노트북을 가지고 있는 사람 어때요?
9. 어떤 기숙사 방을 신청하실 건가요?
10. 잠버릇이 있는 사람 괜찮아요?
'''
question_list = {
    '룸메이트가 흡연하는 분이어도 괜찮나요?': dict(enumerate(['흡연', '비흡연'])),
    '외향적인 사람과 내향적인 사람 중에 어떤 사람이 편하신가요?': dict(enumerate(['외향적', '내향적'])),
    '아침과 저녁 중에 언제 활동하는 사람을 생각하시나요?': dict(enumerate(['아침형', '저녁형'])),
    '학교를 언제 들어온 사람이 더 편한가요?': dict(enumerate(['고학번', '저학번', '상관없음'])),
    '학과는 같은 사람? 아니면 다른 학과?': dict(enumerate(['같은학과', '다른학과', '상관없음'])),
    '나이는 어떤 사람이 룸메로써 좋은가요?': dict(enumerate(['연상', '연하', '상관없음'])),
    '종교를 가진 사람 어때요?': dict(enumerate(['좋아요', '별로에요'])),
    '노트북을 가지고 있는 사람 어때요?': dict(enumerate(['좋아요', '글쎄요'])),
    '어떤 기숙사 방을 신청하실 건가요?': dict(enumerate(['일반동 2인실(578)', '신축동 숲전망(M) 2인실(1,234)', '신축동 캠퍼스전망(A) 2인실(1,282)', '신축동 캠퍼스전망(S) 2인실(1,330)'])),
    '잠버릇이 있는 사람 괜찮아요?': dict(enumerate(['괜찮아요', '싫어요']))
}
'''
답변
1. 1) 흡연, 2) 비흡연
2. 1) 외향적, 2) 내향적
3. 1) 아침형, 2) 저녁형
4. 1) 고학번, 2) 저학번, 3) 동기
5. 1) 같은학과, 2) 다른학과, 3) 상관없음
6. 1) 연상, 2) 연하, 3) 동갑
7. 1) 좋아요, 2) 별로에요
8. 1) 좋아요, 2) 글쎄요
9. 1) 일반동 2인실(578), 2) 일반동 1인실(781), 3) 신축동 숲전망(M) 2인실(1,234), 4) 신축동 캠퍼스전망(A) 2인실(1,282), 5) 신축동 캠퍼스전망(S) 2인실(1,330), 6) 신축동 숲전망(M) 1인실(1,556), 7) 신축동 캠퍼스전망(A) 1인실(1,556), 8) 신축동 캠퍼스전망(S) 1인실(1,610)
10. 1) 괜찮아요, 2) 싫어요
'''

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def question_df(request):
    if 'signup_name' in request.session and 'signup_student_ID' in request.session and 'signup_student_Number' in request.session and 'signup_password' in request.session and 'signup_major' in request.session and 'signup_age' in request.session:
        if request.method == "POST":
            user_pk = request.session.get('user')
            
            user = Profile.objects.filter(user= user_pk)
            
            # 알고리즘
            # 임시로 보관될 룸메리스트
            roommate_list = {}
            
            #같은 성별 리스트 추출
            gender_filter = Profile.objects.filter(gender=user[0].gender)
            
            for key, dic in enumerate(gender_filter):
                roommate_list.update({key: [dic, 0]})
            print(roommate_list)
            
            #Question 객체
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

            lifetime = request.POST.get('lifetime', None) #아침형 / 저녁형
            # answer.. '아침형', '저녁형'
            if lifetime == '아침형':
                lifetime = 1
            elif lifetime == '저녁형':
                lifetime = 0

            student_Number = request.POST.get('student_Number', None) #고학번/저학번/동기
            # answer.. '고학번', '저학번', '동기'
            
            major = request.POST.get('major', None) # 전공
            # answer.. '같은학과', '다른학과', '상관없음'

            age = request.POST.get('age', None) #나이
            # answer.. '연상', '연하', '동갑'

            religion = request.POST.get('religion', None) #종교
            # answer.. '좋아요', '별로에요'
            if religion == '좋아요':
                religion = '네'
            elif religion == '별로에요':
                religion = '아니오'

            labtop = request.POST.get('labtop', None) # 노트북 유무 1: 유, 0: 무        
            # answer.. '좋아요', '글쎄요'
            if labtop == '좋아요':
                labtop = 1
            elif labtop == '글쎄요':
                labtop = 0

            room = request.POST.get('room', None) # room

            sleepinghabit = request.POST.get('sleepinghabit', None) # 잠버릇종류
            # answer.. '괜찮아요', '싫어요'
            if sleepinghabit == '괜찮아요':
                sleepinghabit = 1
            elif sleepinghabit == '싫어요':
                sleepinghabit = 0
            print('-----------------------')
            print(smoke) #흡연 0
            print(lifetime) #아침형/저녁형 1
            print(student_Number) #학번 
            print(type(tendency)) #외향형/내향형 0
            print(type(major)) #전공 상관없음
            print(age) #나이 상관없음
            print(religion) #종교 1
            print(labtop) #노트북 0
            print(sleepinghabit) #잠버릇 1
            print('-----------------------')


            
            for index in range(len(roommate_list)):
                print(roommate_list[index][0].name)
                print('------------------')
                print(type(roommate_list[index][0].smoke))
                print(smoke == roommate_list[index][0].smoke)
                print(lifetime)
                print(type(lifetime))
                print(roommate_list[index][0].lifetime)
                print(type(roommate_list[index][0].lifetime))
                print(lifetime == roommate_list[index][0].lifetime)
                print(user[0].student_ID == roommate_list[index][0].student_ID)
                print(tendency)
                print(roommate_list[index][0].tendency)
                print(tendency == roommate_list[index][0].tendency)
                print(user[0].major == roommate_list[index][0].major)
                print(user[0].age == roommate_list[index][0].age)
                print(type(roommate_list[index][0].religion))
                print(religion == roommate_list[index][0].religion)
                print(labtop == roommate_list[index][0].labtop)
                print(sleepinghabit)
                print(roommate_list[index][0].sleepinghabit)
                print(sleepinghabit == roommate_list[index][0].sleepinghabit)
                print('------------------')
                # 흡연 / 비흡연
                print('--흡연/비흡연--')
                if smoke == roommate_list[index][0].smoke:
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('smoke ok')
                    
                # 아침형 / 저녁형
                print('--아침형/저녁형--')
                if lifetime == int(roommate_list[index][0].lifetime):
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('lifetime ok')
                    
                # 고학번 / 저학번 / 상관없음, 함수
                print('--고학번/저학번/상관없음--')
                if student_Number == '고학번':
                    print('--고학번--')
                    if user[0].student_ID > roommate_list[index][0].student_ID:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('고학번 ok')
                elif student_Number == '저학번':
                    print('--저학번--')
                    if user[0].student_ID < roommate_list[index][0].student_ID:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('저학번 ok')
                elif student_Number == '상관없음':
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('학번 상관없음 Ok')

                # 외향적 / 내향적  
                print('--외향적/내향적--')
                if tendency == int(roommate_list[index][0].tendency):
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('성향 ok')
                    
                # 같은학과 / 다른학과 / 상관없음
                print('--같은학과/다른학과/상관없음--')
                if major == '같은학과':
                    print('--같은학과--')
                    if roommate_list[index][0].major in user[0].major:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('같은학과 Ok')
                elif major == '다른학과':
                    print('--다른학과--')
                    if roommate_list[index][0].major not in user[0].major:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('다른학과 Ok')

                elif major == '상관없음':
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('학과 상관없음 Ok')

                # 연상 / 연하 / 상관없음
                print('--연상/연하/상관없음--')
                if age == '연상':
                    print('--연상--')
                    if user[0].age < roommate_list[index][0].age:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('연상 ok')

                elif age == '연하':
                    print('--연하--')
                    if user[0].age > roommate_list[index][0].age:
                        roommate_list[index][1] = roommate_list[index][1] + 1
                        print('연하 ok')

                elif age == '상관없음':
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('나이 상관없음 ok')

                # 종교 유무
                print('--종교--')
                if religion == roommate_list[index][0].religion:
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('종교 ok')
                    
                # 노트북 유무
                print('--노트북--')
                if labtop == roommate_list[index][0].labtop:
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('노트북 ok')
                    
                #if room == roommate_list[index][0].room:
                #    roommate_list[index][1] = roommate_list[index][1] + 1
                
                # 잠버릇 유무
                print('--잠버릇--')
                if sleepinghabit == int(roommate_list[index][0].sleepinghabit):
                    roommate_list[index][1] = roommate_list[index][1] + 1
                    print('잠버릇 ok')

                print('---------------')
            v = list(roommate_list.values())
            
            t = sorted(v, key=operator.itemgetter(1), reverse=True)
            print(t)

            data = t[:5]
            data_list = []
            data_countlist = []

            for i in range(5):
                data_list.append(data[i][0])
                data_countlist.append(data[i][1])

            data = {
                'data_list': data_list,
                'data_countlist': data_countlist
            }
            
            return render(request, 'Question/result.html', data)
        else:
            question_keylist = list(question_list.keys())
            
            
            return render(request, 'Question/user_quest.html', {'question_keylist': question_keylist, 'question_list': question_list, 'question_keylist_value': len(question_keylist)})
    else:
        #알람 접근권한이없다
        return redirect('/main/home')
# result 임의설정
def questionResult(request):
    return render(request, 'Question/result.html')