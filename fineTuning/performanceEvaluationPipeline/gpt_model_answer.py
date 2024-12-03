from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import LLMEvaluationPrompt
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import secret

AI_model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1, 
    max_tokens = 1024,
    openai_api_key = secret.openai_api_key
)


def get_gpt_model_answer(context, question):
    
    formatted_messages = "'"+ context+"' 의 상황에서 '" + question + "' 뒤에 올 말을 한 줄로 말하세요."
    response = AI_model.invoke(formatted_messages)
        
    parser = StrOutputParser()
    gpt_model_answer = parser.parse(response)
    
    return gpt_model_answer.content

