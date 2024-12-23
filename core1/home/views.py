from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from home.models import Person
from home.serializers import PeopleSerializers,LoginSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator


class LoginAPI(APIView):
    def post(self,request):
        data= request.data
        serializer=LoginSerializer(data=data)
        if  not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors

            },status.HTTP_400_BAD_REQUEST)
        user = authenticate(username= serializer.data['username'],password=serializer.data['password'])
        if not user:
             return Response({
                'status':False,
                'message':'invalid credential'

            },status.HTTP_400_BAD_REQUEST)

        token,_=Token.objects.get_or_create(user=user)
        return Response({'status':True,'message':'user login','token':str(token)},status.HTTP_201_CREATED)



class RegisterAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if  not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors

            },status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'status':True,'message':'user created'},status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def index(request):
    if request.method == "GET":
       json_response={
            'name':'python',
            'course':['c++','python'],
            'method':'GET'
        }
    else:
        data = request.data 
        print(data)
        json_response={
            'name':'python',
            'course':['c++','python'],
            'method':'GET'
        }
    
    return Response(json_response)

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message ':'success'})
    return Response(serializer.errors)

class PersonAPI(APIView): # APIview class 
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    def get(self,request):
        try:
            objs = Person.objects.all()
            page = request.GET.get('page',1)
            page_size = 3
            paginator=Paginator(objs,page_size)
            serializer=PeopleSerializers(paginator.page(page), many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status':False,
                'message':'invalid page'
            })
        
        
    def post(self,request):
        data= request.data
        serializer=PeopleSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def put(self,request):
        data = request.data
        serializer=PeopleSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)
    def patch(self,request):
        data= request.data
        objs=Person.objects.get(id=data['id'])
        serializer=PeopleSerializers(objs,data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request):
        data= request.data
        objs= Person.objects.get(id = data['id'])
        objs.delete()


@api_view(['GET','POST','PUT','PATCH','DELETE']) #decorator
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()

        serializer=PeopleSerializers(objs, many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        data= request.data
        serializer=PeopleSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        serializer=PeopleSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        data= request.data
        objs=Person.objects.get(id=data['id'])
        serializer=PeopleSerializers(objs,data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data= request.data
        objs= Person.objects.get(id = data['id'])
        objs.delete()
        return Response({'message ':'person deleted'})



class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializers
    queryset = Person.objects.all()
    http_method_names=['get','post'] #to restrict other method


    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search: 
            queryset= queryset.filter(name__startswith = search)
        
        serializer=PeopleSerializers(queryset,many = True)

        return Response({'data':serializer.data},status=status.HTTP_204_NO_CONTENT) 

    @action(detail=True,methods=['GET'])
    def send_mail_to_person(self,request,pk):
        objs=Person.objects.get(pk=pk)
        serializer = PeopleSerializers(objs)
        return Response({
                'status':True,
                'message':'email sent succesfully',
                'data':serializer.data
            })
        