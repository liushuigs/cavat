class HttpStatusMiddleWare(object):
    def process_response(self, request, response, spider):
        return response