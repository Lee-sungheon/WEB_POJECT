from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserFollowSerializer
from django.contrib.auth import get_user_model
from .models import User

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus
import random

@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    username = request.data.get('username')
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        return Response({'error': '중복되는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        pass
    print(request.data)
    baseUrl = 'http://random.cat/view/'
    plusUrl = str(random.randint(1, 1500))
    url = baseUrl + plusUrl
    html = urlopen(url)
    soup = bs(html, "html.parser")
    img = soup.find_all(id='cat')
    profileurl = img[0]['src']
    request.data['profileurl'] = profileurl
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    serializer = UserFollowSerializer(person)
    print(serializer.data)
    return Response(serializer.data)




@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    user = request.user
    if person != user:
        if person.followers.filter(username=user.username).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': '본인을 팔로우 할 수 없습니다.'})

    