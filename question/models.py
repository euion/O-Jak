from django.db import models
from user.models import Profile

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100) #기숙사 방이름    
    
class Quest(models.Model):
    User_id  = models.ForeignKey(Profile, on_delete=models.CASCADE) #사용자 번호
    smoke = models.IntegerField() #흡연 유무 1:유 0:무
    tendency = models.CharField(max_length=15) #성향
    lifetime = models.CharField(max_length=20) #아침형/저녁형
    student_ID = models.CharField(max_length=45) #고학번/저학번/동기
    major = models.CharField(max_length=45) #전공/타전공
    age = models.IntegerField() #연상/연하/상관없음
    religion = models.IntegerField() #종교 유무 1: 유, 0: 무
    labtop = models.IntegerField() #노트북 유무 1: 유, 0: 무
    room = models.OneToOneField(Room, on_delete=models.CASCADE) #room 번호
    sleepinghabit = models.IntegerField() #잠버릇 유무 1: 유, 0: 무

