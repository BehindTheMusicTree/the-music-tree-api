
import json
from json.decoder import JSONDecodeError

from bodzify_api.utils import data_transformer


class CamelToSnakeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_type = request.headers.get('Content-Type', '')

        if content_type.startswith('application/json'):
            try:
                if request.body:
                    json_data = json.loads(request.body)
                    request.data = data_transformer.form_data_to_snake_case(json_data)
                else:
                    request.data = {}
            except JSONDecodeError:
                request.data = {}

        if content_type.startswith('multipart/form-data'):
            request.POST = data_transformer.form_data_to_snake_case(request.POST)

            if request.FILES:
                original_files = request.FILES
                request._files = dict()
                for key, files in original_files.items():
                    request._files[data_transformer.to_snake_case(key)] = files

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
