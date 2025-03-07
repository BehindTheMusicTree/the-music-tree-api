from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from bodzify_api.utils import data_transformer


class CamelToSnakeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Convert POST/PUT/PATCH data
        if hasattr(request, 'data'):
            request.data = data_transformer.form_data_to_snake_case(request.data)

        # Convert multipart form data
        content_type = request.headers.get('Content-Type', '')
        if content_type.startswith('multipart/form-data'):
            # Access request.POST first to ensure proper parsing of multipart data
            original_post = request.POST

            # Convert the data using the proper form data transformer
            snake_case_data = data_transformer.form_data_to_snake_case(original_post)

            # Create a new QueryDict and update it with the transformed data
            request.POST = QueryDict(mutable=True)
            for key, value in snake_case_data.items():
                if isinstance(value, list):
                    request.POST.setlist(key, value)
                else:
                    request.POST[key] = value

            # Handle files by creating new MultiValueDict with converted keys
            if request.FILES:
                original_files = request.FILES
                request._files = MultiValueDict()
                for key, files in original_files.items():
                    if not isinstance(files, (list, tuple)):
                        files = [files]
                    for file in files:
                        request._files.appendlist(data_transformer.to_snake_case(key), file)

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
