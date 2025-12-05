import pytest

from bodzify_api.serializer.AppSerializer import AppSerializer


class TestAppSerializer:

    @pytest.mark.parametrize('input_data,expected_output', [
        # Single value list should be extracted
        ({'archived': ['true']}, {'archived': 'true'}),
        ({'title': ['My Title']}, {'title': 'My Title'}),
        ({'count': [5]}, {'count': 5}),

        # List fields (with [] suffix) should remain as lists
        ({'artists_names[]': ['Artist1', 'Artist2']}, {'artists_names[]': ['Artist1', 'Artist2']}),
        ({'artists_names[]': ['Single']}, {'artists_names[]': ['Single']}),

        # Empty list should become None
        ({'archived': []}, {'archived': None}),
        ({'title': []}, {'title': None}),

        # Multiple values for non-list field - normalization handles gracefully
        # (can happen if user submits multiple inputs with same name; field validation will reject)
        ({'archived': ['true', 'false']}, {'archived': ['true', 'false']}),

        # Non-list values should remain unchanged
        ({'archived': True}, {'archived': True}),
        ({'title': 'My Title'}, {'title': 'My Title'}),
        ({'count': 5}, {'count': 5}),

        # Mixed scenarios
        (
            {
                'archived': ['true'],
                'title': 'My Title',
                'artists_names[]': ['Artist1', 'Artist2'],
                'count': [5],
                'empty': []
            },
            {
                'archived': 'true',
                'title': 'My Title',
                'artists_names[]': ['Artist1', 'Artist2'],
                'count': 5,
                'empty': None
            }
        ),
    ])
    def test_normalize_multipart_data_then_returns_expected_output(self, input_data, expected_output):
        serializer = AppSerializer()
        normalized = serializer._normalize_multipart_data(input_data)
        assert normalized == expected_output
