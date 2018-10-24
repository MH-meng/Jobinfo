

class Pagination(object):
    def __init__(self,totleCount,currentPage,perPageItemNum=20,maxPageNum=11):
        self.totle_count = totleCount  #数据总个数
        try:
            v = int(currentPage) # 当前页
            if v <=0:
                v=1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        self.per_page__item_num = perPageItemNum # 每页显示条数
        self.max_page_num = maxPageNum # 最对显示页数

    def start(self):
        return (self.current_page-1)*self.per_page__item_num


    def end(self):
        return self.current_page * self.per_page__item_num

    @property  # 将num_pages()--> num_pages
    def num_pages(self):
        """总页数"""
        a,b = divmod(self.totle_count,self.per_page__item_num)
        if b == 0:
            return a
        return a+1

    def page_num_range(self):
        # num_pages:总页数
        if self.num_pages < self.max_page_num:  # 数据少于最多显示页码数
            return range(1,self.num_pages+1)
        # 总页数特别多
        part = int(self.max_page_num / 2)
        if self.current_page <= part:
            return range(1,self.max_page_num+1)

        if (self.current_page+part > self.num_pages):
            return range(self.num_pages-self.max_page_num+1,self.num_pages+1)

        return range(self.current_page-part,self.current_page+part+1)


    def page_str(self):

        page_list= []
        first = "<li><a href='/index2.html?p=1'>首页</a></li>"
        page_list.append(first)

        if self.current_page <= 1:
            prev="<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/index2.html?p=%s'>上一页</a></li>" %(self.current_page-1)
        page_list.append(prev)

        for i in self.page_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/index2.html?p=%s'>%s</a></li>" % (i,i)
            else:
                temp = "<li><a href='/index2.html?p=%s'>%s</a></li>" % (i, i)
            page_list.append(temp)

        if self.current_page >= self.num_pages:
            nex="<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/index2.html?p=%s'>下一页</a></li>" %(self.current_page+1)
        page_list.append(nex)

        final = "<li><a href='/index2.html?p=%s'>尾页</a></li>" % (self.num_pages)
        page_list.append(final)

        return ''.join(page_list)



# views视图
#     from app.pager import Pagination
#
#     def index2(request):
#         current_page = request.GET.get('p')
#         page_obj = Pagination(999, current_page)
#
#         data_list = USER_LIST[page_obj.start():page_obj.end()]
#
#         return render(request, 'index2.html', {'data': data_list, 'page_obj': page_obj})


# templates
#     < link rel = "stylesheet" href = "/static/inseat/bootstrap/css/bootstrap.css" type = "text/css" >
#     < ul class ="pagination pagination-sm" >
#         {{page_obj.page_str | safe}}
#     < / ul >
