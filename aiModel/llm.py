from langchain_openai import ChatOpenAI
import secret

AI_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.75, 
    max_tokens = 1024,
    openai_api_key = secret.openai_api_key
)
