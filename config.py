import yaml
import os

def load_config():
    config_path = os.path.join(
        os.path.dirname(__file__),
        "config/gateway_config.yaml"
    )
    with open(config_path) as f:
        return yaml.safe_load(f)

CONFIG = load_config()