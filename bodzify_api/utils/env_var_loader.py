import os
import subprocess
from pathlib import Path
import dotenv

from bodzify_api.utils.utils import print_django


def load_required_str_env_var(var_name: str, must_print_value: bool = True) -> str:
    var_value = os.getenv(var_name)
    if var_value is None:
        raise EnvironmentError(f"The {var_name} environment variable must be set")
    if must_print_value:
        print_django(f"{var_name}: {var_value}")
    else:
        print_django(f"{var_name} is set.")
    return var_value


def load_required_bool_env_var(var_name: str) -> bool:
    var_value = load_required_str_env_var(var_name).lower()
    if var_value not in ['true', 'false']:
        raise EnvironmentError(f"The {var_name} environment variable must be 'true' or 'false', got '{var_value}'")
    return var_value == 'true'


def load_required_int_env_var(var_name: str) -> int:
    var_value = load_required_str_env_var(var_name)
    try:
        return int(var_value)
    except ValueError as e:
        raise EnvironmentError(f"The {var_name} environment variable must be an integer, got '{var_value}'") from e


def load_required_path_env_var(var_name: str, must_print_value: bool = True) -> Path:
    path = Path(load_required_str_env_var(var_name))
    if not path.exists():
        raise EnvironmentError(f"The path {path} does not exist")
    print_django(f"The path {path} exists on the system.")
    return path


def load_calculated_env_paths(base_dir: Path):
    CALCULATED_PATHS_ENV_FILE = base_dir / 'env/calculated_paths/.env'
    generate_calculated_paths_env_file_script_path = base_dir / 'scripts/generate-calculated-paths-env-file.sh'
    try:
        subprocess.run(['bash', str(generate_calculated_paths_env_file_script_path)],
                       check=True,
                       stderr=subprocess.PIPE,
                       text=True,
                       env=os.environ.copy())
    except subprocess.CalledProcessError as e:
        print_django(f"Error while generating the paths env file: {e.stderr}")  # type: ignore
        raise EnvironmentError("Error while generating the paths env file: {e}") from e

    dotenv.load_dotenv(CALCULATED_PATHS_ENV_FILE)


def load_env_vars_from_file_if_exists(env_file_path: Path):
    if not env_file_path.exists():
        print_django(f"No env file at {env_file_path}")
    else:
        print_django(f"Env file provided at {env_file_path} . Loading...")
        dotenv.load_dotenv(env_file_path)
        print_django("Env file loaded.")


def load_required_secret_env_var(var_name: str) -> str:
    var_value = load_required_str_env_var(var_name=var_name, must_print_value=False)
    if var_value.startswith('"') and var_value.endswith('"'):
        return var_value[1:-1]
    return var_value
