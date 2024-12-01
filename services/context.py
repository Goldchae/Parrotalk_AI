from langchain.memory import ConversationSummaryMemory
from aiModel import llm

memory_store = {}

def get_user_memory(user_id):

    if user_id not in memory_store:
        memory_store[user_id] = ConversationSummaryMemory(llm=llm.AI_model)
        return "nothing"
    return memory_store[user_id]


def add_message(user_id,input,output):
    memory_store[user_id].save_context({"inputs": input}, {"outputs": output})