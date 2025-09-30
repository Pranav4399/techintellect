import os
from typing import Dict, Any

class ConfigLoader:     
    def __init__(self, config_file: str = "app.conf"):
        self.config_file = config_file
        self._config = {}
        self._load_config()
    
    def _load_config(self) -> None:
        try:
            if not os.path.exists(self.config_file):
                raise FileNotFoundError(f"Configuration file not found")
            
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self._config[key.strip()] = value.strip()
        
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def get_elasticsearch_config(self) -> Dict[str, str]:
        return {
            'host': self.get('ELASTICSEARCH_HOST', 'http://localhost:9200'),
            'index_name': self.get('INDEX_NAME', 'employee_data')
        }


config = ConfigLoader()
