# coding: utf-8
__author__ = "HanQian"

class PageInfo(object):
    def __init__(self,current_page,per_page_num,all_count,base_url,page_range=11, filter=None):
        """
        :param current_page:  当前页码；type: int
        :param per_page_num:  每页显示数据条数
        :param all_count:  数据库总条数
        :param base_url:  页码标签的前缀
        :param page_range:  页面最多显示的页码个数
        """
        try:
            # 请求的参数不是数字就返回第一页
            current_page = int(current_page)
        except Exception as e:
            current_page = int(1)
        self.per_page_num = per_page_num
        self.all_count = all_count

        # 判断需要的页码数
        a, b = divmod(self.all_count,per_page_num)
        if b == 0:
            self.all_page = a
        else:
            self.all_page = a + 1
        # 请求的页码大于总页码返回第一页
        if current_page > self.all_page:
            self.current_page = 1
        else:
            self.current_page = current_page
        self.base_url = base_url
        self.page_range = page_range
        # 通过切片获取当前页要显示的数据，[0:10] [10:20] [20:30]
        self.start = (self.current_page - 1) * self.per_page_num
        self.end = self.current_page * self.per_page_num
        self.filter = ''
        for k,v in filter.items():
            self.filter += '&%s=%s'%(k,v)

        print("过滤URL==",self.filter)

    def page_str(self):
        """ 在HTML页面中显示页码信息 """
        page_list = []
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            prev = '<li><a href="%s?page=%s%s">上一页</a></li>' % (self.base_url, self.current_page - 1,self.filter,)
        page_list.append(prev)
        # page_range 默认11
        # 总页数小于11时
        if self.all_page <= self.page_range:
            start = 1
            end = self.all_page + 1
        else:
            # 总页数大于11时
            if self.current_page > int(self.page_range / 2):
                # 尾部页码处理： ....96,97,98,99,100
                # 当前页+5大于总页码时
                if (self.current_page + int(self.page_range / 2)) > self.all_page:
                    start = self.all_page - self.page_range + 1
                    end = self.all_page + 1
                else:
                    start = self.current_page - int(self.page_range / 2)
                    end = self.current_page + int(self.page_range / 2) + 1
            else:
                # 前边页码处理：1,2,3,4,5.....
                # 当前页码小于5时,防止出现：-4,-3,-2,-1,0,1,2,3,4,5,6
                start = 1
                end = self.page_range + 1

        for i in range(start, end):
            if self.current_page == i:
                temp = '<li class="active"><a href="%s?page=%s%s">%s</a></li>' % (self.base_url, i,self.filter, i,)
            else:
                temp = '<li><a href="%s?page=%s%s">%s</a></li>' % (self.base_url, i,self.filter, i,)
            page_list.append(temp)
        if self.current_page >= self.all_page:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            nex = '<li><a href="%s?page=%s%s">下一页</a></li>' % (self.base_url, self.current_page + 1,self.filter)
        page_list.append(nex)
        print("分页",page_list)
        return ''.join(page_list)