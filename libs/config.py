import os


def get_env(variable, default=None):
    env_variable = os.getenv(variable)
    if not env_variable:
        return default
    return env_variable


def get_int_env(variable, default=None):
    env_variable = get_env(variable, default)
    if not env_variable:
        return default
    try:
        env_variable = int(env_variable)
        return env_variable
    except ValueError:
        print(f"Error: can not convert to int: {variable}")
        return default


def get_float_env(variable, default=None):
    env_variable = get_env(variable, default)
    if not env_variable:
        return default
    try:
        env_variable = float(env_variable)
        return env_variable
    except ValueError:
        print(f"Error: can not convert to float: {variable}")
        return default


def get_bool_env(variable, default=None):
    env_variable = get_env(variable, default)
    if not env_variable or env_variable not in ("True", "False"):
        return default
    if env_variable == "True":
        return True
    elif env_variable == "False":
        return False
