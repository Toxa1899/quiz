from django.core.paginator import Paginator


class PaginationObject:
    def __init__(self, objects, page=1, numbers_in_page=10, user=None, serializer=None,
                 number_of_objects_title='number_of_objects',
                 number_of_pages_title='number_of_pages', result_title='result',
                 **kwargs):
        self.all_objects = objects
        self.page = page
        self.numbers_in_page = numbers_in_page
        self.current_page_objects_data = None
        self.number_of_pages = None
        self.user = user
        self.serializer = serializer
        self.objects_pagination()
        self.number_of_objects_title = number_of_objects_title
        self.number_of_pages_title = number_of_pages_title
        self.result_title = result_title
        self.kwargs = kwargs

    def objects_pagination(self):
        if self.numbers_in_page == -1:
            p = Paginator(self.all_objects, len(self.all_objects) if len(self.all_objects) > 0 else 1)
            self.number_of_pages = 1
        else:
            p = Paginator(self.all_objects, self.numbers_in_page)
            self.number_of_pages = p.num_pages
        if self.page > p.num_pages:
            self.current_page_objects_data = []
        else:
            self.current_page_objects_data = self.serializer(instance=p.page(self.page), many=True,
                                                             context={'user': self.user}).data

    def serializer_data(self):
        return {self.number_of_objects_title: len(self.all_objects), self.number_of_pages_title: self.number_of_pages,
                self.result_title: self.current_page_objects_data, **self.kwargs}
