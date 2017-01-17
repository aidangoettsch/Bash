import importlib.util

spec = importlib.util.spec_from_file_location("module.name", str("src/client/main.py"))
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)
