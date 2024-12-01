import os
from langchain_core.output_parsers import StrOutputParser
from aiModel import llm
from prompts import recommend_prompt
from services import context


def recommend(user_id, message): # 유저 아이디 필요! 어케?
    history = context.get_user_memory(user_id)
    
    formatted_messages = recommend_prompt.make_recommend_prompt(message, history)
    response = llm.AI_model.invoke(formatted_messages)
        
    parser = StrOutputParser()
    parsed_output = parser.parse(response)

    context.add_message(user_id, message, parsed_output.content)
    
    return parsed_output.content
