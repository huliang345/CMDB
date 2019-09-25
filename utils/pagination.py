#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'huliang'
from django.utils.safestring import mark_safe


class Pagination(object):  # 继承不继承都可以，python3默认继承 继承的是新式类，不继承的是经典类或旧式类
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):  # 初始化参数
        try:
            v = int(current_page)
            if v <= 0:
                self.current_page = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property  # 将调用去掉（）
    def start(self):  # 确定当前页开始的数据
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):  # 确定当前页结束的数据
        return self.current_page * self.per_page_count

    @property
    def total_page(self):  # 计算总页数
        a, b = divmod(self.data_count, self.per_page_count)
        if b:
            a += 1
        return a

    def page_str(self, base_url):
        page_list = []

        # 极值情况的考虑：
        if self.total_page < self.pager_num:
            start_index = 1  # 页码开始切片
            end_index = self.total_page + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_page:
                    start_index = self.total_page - self.pager_num + 1
                    end_index = self.total_page + 1

        if self.current_page == 1:
            prev = '<li><a class="page" href="javascript:void(0);">上一页</a></li>'
        else:
            prev = '<li><a class="page" href="%s?p=%s">上一页</a></li>' % (base_url, self.current_page - 1,)
        page_list.append(prev)

        for i in range(start_index,end_index):
            if i == self.current_page:
                temp='<li class="active"><a class="page active" href="%s?p=%s">%s</a></li>'%(base_url,i,i,)
            else:
                temp = '<li><a class="page" href="%s?p=%s">%s</a></li>' % (base_url, i, i,)
            page_list.append(temp)

        if self.current_page == self.total_page:
            nex = '<li><a class="page" href="javascript:void(0);">下一页</a></li>'
        else:
            nex = '<li><a class="page" href="%s?p=%s">下一页</a></li>' % (base_url, self.current_page + 1,)
        page_list.append(nex)

        page_str = mark_safe(' '.join(page_list))
        return page_str
