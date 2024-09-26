from typing import Any, Dict, List
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler

class AgentCallBackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str],**kwargs: Any) -> Any:
        """Run when llm starts running"""

        return super().on_llm_start(serialized, prompts, **kwargs)