from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import LLMEvaluationPrompt
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import secret

AI_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.75, 
    max_tokens = 1024,
    openai_api_key = secret.openai_api_key
)


def get_LLM_evaluation_score(context, question, answer):
    
    formatted_messages = LLMEvaluationPrompt.make_LLM_evaluation_prompt(context, question, answer)

    response = AI_model.invoke(formatted_messages)
        
    parser = StrOutputParser()
    LLM_evaluation_score = parser.parse(response)
    
    return LLM_evaluation_score.content

