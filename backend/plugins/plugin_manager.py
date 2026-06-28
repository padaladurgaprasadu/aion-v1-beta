import os
import importlib.util
from typing import List, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class PluginManager:
    """
    Enterprise Phase 3 Feature: Plugin Marketplace & Extensions.
    Dynamically loads Python scripts from the 'plugins/' directory, allowing
    enterprise users to extend AiON with custom LangChain Tools (e.g., Jira, AWS).
    """
    def __init__(self, plugin_dir: str = None):
        if not plugin_dir:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.plugin_dir = os.path.join(base_dir, "plugins")
        else:
            self.plugin_dir = plugin_dir
            
        os.makedirs(self.plugin_dir, exist_ok=True)
        self.loaded_tools = []
        self._load_plugins()

    def _load_plugins(self):
        """Scans the plugins directory and imports custom tools."""
        logger.info(f"[PluginManager] Scanning for enterprise plugins in {self.plugin_dir}...")
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                self._import_plugin(filename)

    def _import_plugin(self, filename: str):
        filepath = os.path.join(self.plugin_dir, filename)
        module_name = filename[:-3]
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for a register_tools function in the plugin
            if hasattr(module, "register_tools"):
                tools = module.register_tools()
                if isinstance(tools, list):
                    self.loaded_tools.extend(tools)
                    logger.info(f"   -> [PluginManager] Successfully loaded {len(tools)} tools from {filename}")
        except Exception as e:
            logger.error(f"   -> [PluginManager] Failed to load plugin {filename}: {e}")

    def get_all_tools(self) -> List[Any]:
        """Returns all dynamically loaded LangChain tools."""
        return self.loaded_tools
