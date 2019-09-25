from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.views import View
from repository import models
import json
from utils.pagination import Pagination
from django.http.request import QueryDict


class AssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset.html')


class AssetJsonView(View):
    # get方法处理以get方式发来的ajax请求：获取数据
    def get(self, request, *args, **kwargs):
        table_config = [
            # 我们的数据表配置文件：
            # 规则：text中的@+字段就解析成数据库对应值，没有就保留
            {
                'theme': None,
                'title': '选项',
                'display': True,
                'text': {'content': '<input type="checkbox"/>', 'kwargs': {}},
                'attrs': {},
            },
            {
                'theme': 'id',
                'title': 'ID',
                'display': False,
                'text': {},
                'attrs': {},
            },
            {
                'theme': 'device_type_id',
                'title': '资产类型',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@@device_type_choices'}},  # 怎么辨别他有choices得有个规则
                'attrs': {'original-id': '@device_type_id', 'edit-enable': 'false', 'edit-type': 'select',
                          'global-name': 'device_type_choices'},
            },
            {
                'theme': 'device_status_id',
                'title': '资产状态',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@@device_status_choices'}},  # 怎么辨别他有choices得有个规则
                'attrs': {'field': 'device_status_id', 'original-id': '@device_status_id', 'edit-enable': 'true',
                          'edit-type': 'select',
                          'global-name': 'device_status_choices'},
            },
            {
                'theme': 'idc_id',
                'title': 'idc_id',
                'display': False,
                'text': {},  # 怎么辨别他有choices得有个规则
                'attrs': {},
            },
            {
                'theme': 'idc__name',
                'title': 'idc',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@idc__name'}},  # 怎么辨别他有choices得有个规则
                'attrs': {'field': 'idc_id', 'original-id': '@idc_id', 'edit-enable': 'true', 'edit-type': 'select',
                          'global-name': 'idc_choices'},
            },
            {
                'theme': 'cabinet_order',
                'title': '机柜位置',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@cabinet_order'}},
                'attrs': {'field': 'cabinet_order', 'original-id': '@cabinet_order', 'edit-enable': 'true',
                          'edit-type': 'input'},
            },
            {
                'theme': 'cabinet_num',
                'title': '机柜号',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@cabinet_num'}},
                'attrs': {'edit-enable': 'false', 'edit-type': 'input'},
            },
            {
                'theme': None,
                'title': '操作',
                'display': True,
                'text': {'content': "<a href='/assetdetail-{m}.html'>{n}</a>", 'kwargs': {'n': '查看详细', 'm': '@id'}},
                'attrs': {},
            },
        ]
        theme_list = []
        for i in table_config:
            if i['theme']:
                theme_list.append(i['theme'])

        # 分页组件：# ++++++++++++++++
        current_page = request.GET.get('pager')
        if not current_page:
            current_page = 1
        data_count = models.Asset.objects.values(*theme_list).count()
        obj = Pagination(current_page, data_count)

        table_data_list = list(models.Asset.objects.values(*theme_list)[obj.start:obj.end])
        # [{'id': 1, 'cabinet_order': '1', 'cabinet_num': '12B'},
        # {'id': 2, 'cabinet_order': '2', 'cabinet_num': '2B'}]
        result = {
            'table_config': table_config,
            'table_data_list': table_data_list,
            'global_dict': {
                'device_type_choices': models.Asset.device_type_choices,  # 怎么辨别他有choices得有个规则
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choices': list(models.IDC.objects.values_list('id', 'name')),
            },
            # ++++++++++++++++
            # 'pager':"""<li><a>1</a></li><li><a>2</a></li><li><a>3</a></li><li><a>4</a></li><li><a>5</a></li>""",
            'pager': obj.page_str("javascript:void(0);"),
        }
        return HttpResponse(json.dumps(result))

    # put方法处理以gput方式发来的ajax请求：修改数据
    def put(self, request, *args, **kwargs):
        ret = {
            'status': True,
        }
        # 没有request.put故put数据在request.body里面
        content = request.body
        v = QueryDict(content, encoding='utf-8')  # 用来存储请求中的数据，是为了解决一个key对应多个值的情况
        print('+++++++++++++++++++++++++++++', v)
        postlist = json.loads(v.get('postlist'))
        print('+++++++++++++++++++++++++++++', postlist, type(postlist))
        for row_dict in postlist:
            id = row_dict.pop('id')
            try:
                models.Asset.objects.filter(id=id).update(**row_dict)
            except Exception as e:
                ret['status'] = False
                ret['error'] = str(e)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        return HttpResponse(json.dumps(ret))


class BusinessUnitView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'business_unit.html')


class BusinessUnitJsonView(View):
    # get方法处理以get方式发来的ajax请求：获取数据
    def get(self, request, *args, **kwargs):
        table_config = [
            # 我们的数据表配置文件：
            # 规则：text中的@+字段就解析成数据库对应值，没有就保留
            {
                'theme': None,
                'title': '选项',
                'display': True,
                'text': {'content': '<input type="checkbox"/>', 'kwargs': {}},
                'attrs': {},
            },
            {
                'theme': 'id',
                'title': 'ID',
                'display': False,
                'text': {},
                'attrs': {},
            },
            {
                'theme': 'name',
                'title': '业务线名称',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@name'}},  # 怎么辨别他有choices得有个规则
                'attrs': {'field': 'name','original-id': '@name', 'edit-enable': 'true', 'edit-type': 'input',
                          },
            },
            {
                'theme': 'contact_id',
                'title': '联系人组id',
                'display': False,
                'text': {},  # 怎么辨别他有choices得有个规则
                'attrs': {},
            },
            {
                'theme': 'contact__name',
                'title': '联系人组',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@contact__name'}},  # 怎么辨别他有choices得有个规则
                'attrs': {'field': 'contact_id','original-id': '@contact_id', 'edit-enable': 'true', 'edit-type': 'select',
                          'global-name': 'contact_choices'},
            },
            {
                'theme': 'manager__name',
                'title': '管理员组',
                'display': True,
                'text': {'content': '{n}', 'kwargs': {'n': '@manager__name'}},  # 怎么辨别他有choices得有个规则
                'attrs': {},
            },
            {
                'theme': None,
                'title': '操作',
                'display': True,
                'text': {'content': "<a href='/assetdetail-{m}.html'>{n}</a>", 'kwargs': {'n': '查看详细', 'm': '@id'}},
                'attrs': {},
            },
        ]
        theme_list = []
        for i in table_config:
            if i['theme']:
                theme_list.append(i['theme'])
        # 分页组件：# ++++++++++++++++
        current_page = request.GET.get('pager')
        if not current_page:
            current_page = 1
        data_count = models.BusinessUnit.objects.values(*theme_list).count()
        obj = Pagination(current_page, data_count)
        table_data_list = list(models.BusinessUnit.objects.values(*theme_list)[obj.start:obj.end])
        print(table_data_list)
        # [{'id': 1, 'cabinet_order': '1', 'cabinet_num': '12B'},
        # {'id': 2, 'cabinet_order': '2', 'cabinet_num': '2B'}]
        result = {
            'table_config': table_config,
            'table_data_list': table_data_list,
            'global_dict': {
                'contact_choices': list(models.UserGroup.objects.values_list('id', 'name')),
                # 'device_type_choices': models.Asset.device_type_choices,  # 怎么辨别他有choices得有个规则
                # 'device_status_choices': models.Asset.device_status_choices,
                # 'idc_choices': list(models.IDC.objects.values_list('id', 'name')),
            },
            # ++++++++++++++++
            'pager': obj.page_str("javascript:void(0);"),
        }
        return HttpResponse(json.dumps(result))

    # put方法处理以gput方式发来的ajax请求：修改数据
    def put(self, request, *args, **kwargs):
        # 没有request.put故put数据在request.body里面
        content = request.body
        ret = {
            'status': True,
        }
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        v = QueryDict(content, encoding='utf-8')  # 用来存储请求中的数据，是为了解决一个key对应多个值的情况
        print('+++++++++++++++++++++++++++++', v)
        postlist = json.loads(v.get('postlist'))
        print('+++++++++++++++++++++++++++++', postlist, type(postlist))
        for row_dict in postlist:
            id = row_dict.pop('id')
            try:
                models.BusinessUnit.objects.filter(id=id).update(**row_dict)
            except Exception as e:
                ret['status'] = False
                ret['error'] = str(e)
        return HttpResponse(json.dumps(ret))
