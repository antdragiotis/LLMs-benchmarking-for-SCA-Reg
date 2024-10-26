import importlib
from typing import Optional

from evals.api import CompletionFn, CompletionResult

import faiss

from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.llms.openai import OpenAI

class LangChainLLMCompletionResult(CompletionResult):
    def __init__(self, response) -> None:
        self.response = response

    def get_completions(self) -> list[str]:
        return [self.response.strip()]

class SCA_CompletionFn(CompletionFn):
    def __init__(self, llm: str, llm_kwargs: Optional[dict] = None, **kwargs) -> None:

        # Initialize LLM model 
        llm = OpenAI(model=llm_kwargs['model_name'], temperature=0.7)   
        
        # Read vectorized data
        FAISS_directory = "./FAISS storage/"
        vector_store = FaissVectorStore.from_persist_dir(FAISS_directory)
        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=FAISS_directory)
        index = load_index_from_storage(storage_context=storage_context)

        # Initialize query engine
        self.query_engine = index.as_query_engine(llm=llm)
        
    def __call__(self, prompt, **kwargs) -> LangChainLLMCompletionResult:
        response = self.query_engine.query(str(prompt))
        return LangChainLLMCompletionResult(response.response)