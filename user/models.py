from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 20) #사용자의 이름
    student_ID = models.CharField(max_length=45, unique = True) #학번
    User_PW = models.CharField(max_length=256) #사용자의 패스워드
    smoke = models.IntegerField() #흡연 유무 1: 유, 0: 무
    gender = models.CharField(max_length=5) #남/여
    tendency = models.CharField(max_length=15) #성향
    lifetime = models.CharField(max_length=20) #아침형/저녁형
    major = models.CharField(max_length=45) #전공
    age = models.IntegerField() #나이
    religion = models.CharField(max_length=45) #종교
    labtop = models.IntegerField() #노트북 유무 1: 유, 0: 무
    police = models.IntegerField() #신고 유무 1: 유, 0: 무
    admin = models.IntegerField() #유저 권환 1: 관리자, 0: 사용자
    sleepinghabit = models.CharField(max_length=20) #잠버릇종류