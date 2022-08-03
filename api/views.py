from django.test import RequestFactory
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Job_title, Employee
from .serializers import Job_title_Serializer, EmployeeSerializer, RecurseEmployeeSerializer
from django.db import models
import hashlib
import time

PARAMS = [ 
    'id',
    'first_name',
    'second_name',
    'middle_name',
    'job_title',
    'hired',
    'salary',
    'chief',
    'username'
]

TRUE_FALSE = [
    'False',
    'True'
]

@api_view(['POST'])
def login(request):
    try:
        tusername = request.data['username']
        tpassword = request.data['password']
        md5pass = hashlib.md5(tpassword.encode()).hexdigest()

        employer = Employee.objects.get(username=tusername, password=md5pass)
        employer.auth_token = hashlib.sha256(str(tusername+tpassword+str(time.time())).encode()).hexdigest()
        employer.save()
        return Response({'msg': 'success', 'token': employer.auth_token})
    except Employee.DoesNotExist:
        return Response({'msg': 'Wrong password or username!'})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})

@api_view(['POST'])
def logout(request):
    try:
        token = request.data['token']
        employer = Employee.objects.get(auth_token=token)
        employer.auth_token = ''
        employer.save()
        return Response({'msg': 'successfully logout!'})
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})

@api_view(['GET'])
def titles(request):
    try:
        token = request.data['token']
        Employee.objects.get(auth_token=token)

        titles = Job_title.objects.all().order_by('pk')
        serializer = Job_title_Serializer(titles, many=True)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})

@api_view(['GET'])
def abilities(request):
    try:
        token = request.data['token']
        Employee.objects.get(auth_token=token)      

        resp = {
            'msg': 'Functionality available to you',
            'params': {
                'search_by': PARAMS,
                'ordering_by': PARAMS,
                'reversed_ordering': TRUE_FALSE,
                'tree': TRUE_FALSE
            }                         
        }
        return Response(resp)
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000

@api_view(['GET'])
def getemployers(request):        
    try:
        token = request.data['token']
        Employee.objects.get(auth_token=token)      
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})
    
    ordering = 'id'
    try:
        if request.data['ordering_by'] in PARAMS:
            ordering = request.data['ordering_by'] 
    except:
        pass

    try:
        if request.data['reversed_ordering'] == 'True':
            ordering = '-'+ordering
    except:
        pass    

    tree = False
    try:
        if request.data['tree'] == 'True':
            tree = True
    except:
        pass

    try:
        paginator = StandardResultsSetPagination()
        param = request.data['search_by']['param']
        value = request.data['search_by']['value']

        if param in PARAMS:
            if tree == False:
                my_filter = {}
                my_filter[param] = value
                employers = Employee.objects.order_by(ordering).filter(**my_filter)
                result_page = paginator.paginate_queryset(employers, request)
                serializer = EmployeeSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                my_filter = {}
                my_filter[param] = value
                employers = Employee.objects.order_by(ordering).filter(**my_filter)                
                result_page = paginator.paginate_queryset(employers, request)
                serializer = RecurseEmployeeSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            return Response({'msg': 'Undefined param'})        
    except KeyError:
        if tree == False:
            employers = Employee.objects.all().order_by(ordering)            
            result_page = paginator.paginate_queryset(employers, request)
            serializer = EmployeeSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
            
        else:               
            employers = Employee.objects.order_by(ordering).filter(Job_title__pk=0)
            result_page = paginator.paginate_queryset(employers, request)
            serializer = RecurseEmployeeSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def changedata(request):
    try:
        token = request.data['token']
        mdict = request.data
        del mdict['token']
        Employee.objects.filter(auth_token=token).update(**mdict)
        return Response({'msg': 'success'})
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})
    
@api_view(['POST'])
def changepassword(request):
    try:
        token = request.data['token']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        old_password = hashlib.md5(old_password.encode()).hexdigest()
        new_password = hashlib.md5(new_password.encode()).hexdigest()
        employer = Employee.objects.get(auth_token=token, password=old_password)
        employer.password = new_password
        employer.save()
        return Response({'msg': 'password succesfully changed!'})
    except Employee.DoesNotExist:
        return Response({'msg': "Token doesn't exists or wrong old_password!"})
    except KeyError:
        return Response({'msg': 'Unexpected error!'})

