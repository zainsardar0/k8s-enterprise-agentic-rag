import sys
import types

# Compatibility shim for ragas internal imports of deprecated langchain_community modules
try:
    import langchain_google_vertexai
    if "langchain_community.chat_models.vertexai" not in sys.modules:
        m_chat = types.ModuleType("langchain_community.chat_models.vertexai")
        m_chat.ChatVertexAI = langchain_google_vertexai.ChatVertexAI
        sys.modules["langchain_community.chat_models.vertexai"] = m_chat
    if "langchain_community.llms.vertexai" not in sys.modules:
        m_llm = types.ModuleType("langchain_community.llms.vertexai")
        m_llm.VertexAI = langchain_google_vertexai.VertexAI
        sys.modules["langchain_community.llms.vertexai"] = m_llm
except ImportError:
    pass

from evals.guardrails_eval import compute_guardrails_metrics, run_guardrails_eval
from evals.metrics import run_all_metrics
from evals.pipeline import load_golden_dataset, run_pipeline