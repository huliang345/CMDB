from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import hashlib
import time

ck = 'huliang'
auth_list = []  # 这里要做认证记录


@csrf_exempt
def asset(request):
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    auth_key_time = request.META['HTTP_AUTHKEY']
    # print(auth_key_time)
    auth_key_client, client_time = auth_key_time.split('|')
    server_current_time=time.time()
    if (server_current_time-float(client_time)) > 10:
        return HttpResponse('太久了不通过')
    if auth_key_time in auth_list:
        return HttpResponse('已访问的记录不通过')

    auth_key_time_string = '%s|%s' % (ck, client_time)
    m = hashlib.md5()
    m.update(bytes(auth_key_time_string, encoding='utf-8'))
    auth_key_server = m.hexdigest()
    if auth_key_client != auth_key_server:
        return HttpResponse('授权失败')
    # <QueryDict: {'status': ['True'], 'data': ['status', 'host_name', 'data']}>
    # post可以传入字典数据但不支持字典的v是字典所以要自己定制,最后字典数据会在request.body里
    # post只能传简单的python数据结构，不能用太复杂的，太复杂就用json后台再解析就行，只不过在requet.body里面就是了
    auth_list.append(auth_key_time)
    if request.method == 'POST':
        host_info = json.loads(str(request.body, encoding='utf-8'))
        # 注意request.body只能用于post请求，否则会报错，所以要给个if判断
        print(host_info, type(host_info))
    return HttpResponse('ok')

