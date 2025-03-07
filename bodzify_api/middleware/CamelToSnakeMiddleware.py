
from bodzify_api.utils import data_transformer


class CamelToSnakeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert POST/PUT/PATCH data
        if hasattr(request, 'data'):
            request.data = data_transformer.form_data_to_snake_case(request.data)

        # Convert multipart form data
        if request.POST:
            request.POST = request.POST.copy()
            request.POST = data_transformer.form_data_to_snake_case(request.POST)

        # Convert file upload field names
        if request.FILES:
            files_copy = request.FILES.copy()
            files_dict = data_transformer.dict_to_snake_case(dict(files_copy))
            request._files.clear()
            for key, value in files_dict.items():
                request._files[key] = value

        # Convert GET parameters
        if request.GET:
            request.GET = request.GET.copy()
            get_params = dict(request.GET.lists())
            converted = data_transformer.dict_to_snake_case(get_params)
            request.GET.clear()
            for key, value in converted.items():
                if isinstance(value, list):
                    request.GET.setlist(key, value)
                else:
                    request.GET[key] = value

        response = self.get_response(request)
        return response
