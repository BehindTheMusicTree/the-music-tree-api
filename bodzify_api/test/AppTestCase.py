import inspect
import os
from pathlib import Path


from django.core.management import call_command
from django.test import TestCase

from bodzify_api.model.user.User import User
from bodzify_api.test.utils.model_fixture_factory import ModelFixtureFactory


class AppTestCase(TestCase):
    SAMPLE_DIR_NAME = "sample"
    DEFAULT_SAMPLE_FILENAME = "default.mp3"
    LIB_SAMPLE_DIR_NAME = "library"
    INPUT_SAMPLE_DIR_NAME = "input"
    GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR = Path("utils/generic_file_sample")

    def _set_up_test_directories_and_variables(self):
        specific_test_dir_abs_path = Path(os.path.dirname(inspect.getfile(self.__class__)))
        specific_test_sample_dir_abs_path = specific_test_dir_abs_path / self.SAMPLE_DIR_NAME
        self.lib_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.LIB_SAMPLE_DIR_NAME
        self.specific_sample_dir_abs_path = specific_test_sample_dir_abs_path / self.INPUT_SAMPLE_DIR_NAME
        self.generic_sample_dir_abs_path = Path(os.path.dirname(os.path.abspath(__file__))) \
            / self.GENERIC_FILE_SAMPLE_PATH_RELATIVE_TO_TEST_DIR

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        call_command('loaddata', 'app')
        self.test_admin_user = User.objects.create_superuser(username='test_admin',
                                                             password='test_admin',
                                                             email='test_admin@example.com',
                                                             is_test_user=True)

        self.test_user1 = User.objects.create_instance(username='pytest_user1',
                                                       password='pytest_user1',
                                                       email='pytest@user1.com',
                                                       is_test_user=True)

        self.test_user2 = User.objects.create_instance(username='pytest_user2',
                                                       password='pytest_user2',
                                                       email='pytest@user2.com',
                                                       is_test_user=True)

        self._set_up_test_directories_and_variables()
        generic_sample_path = self.generic_sample_dir_abs_path / self.DEFAULT_SAMPLE_FILENAME
        self.model_fixture_factory = ModelFixtureFactory(default_test_user=self.test_user1,
                                                         lib_samples_dir=self.lib_sample_dir_abs_path,
                                                         generic_sample_path=generic_sample_path)

        super().setUp()

        if methods_names_to_implement:
            for method_name in methods_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")
