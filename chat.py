from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

#modelo = os.getenv("model")
#print(modelo)
client = OpenAI(api_key=OPENAI_API_KEY)

# Entrada do usuário
pergunta_user = input("Você: ")

# Faz a requisição ao modelo da OpenAI
response = client.chat.completions.create(
    model= "gpt-4.1-nano" ,  #os.getenv("model", "gpt-4.1-nano"),
    messages=[
        {"role": "system", "content": "Você é um assistente útil e direto."},
        {"role": "user", "content": pergunta_user}
    ]
)

# Extrai a resposta da IA e o número de tokens usados
resposta_ia = response.choices[0].message.content
tokens_usados = response.usage.total_tokens
 
# Mostra os resultados separadamente
print("\n🤖 Resposta da IA:")
print(resposta_ia)
print(f"\n📊 Tokens usados: {tokens_usados}")

usage = response.usage
print(f"Tokens de  Prompt : {usage.prompt_tokens}, Tokens de resposta : {usage.completion_tokens}, Total de tokens: {usage.total_tokens}")
custo_total = ((usage.prompt_tokens * 0.20) + (usage.completion_tokens * 0.80)) 


print(f"Custo total: US$ {custo_total / 1_000_000:.8f}")


#contagem de tokens com library tiktoken só conta tokens, não custo
import tiktoken

texto = resposta_ia
# Escolhe o modelo (use o mesmo que você usou na API)
modelo = "gpt-4.1-nano"

# Obtém o codificador do modelo
encoding = tiktoken.encoding_for_model(modelo)

# Conta tokens
tokens = len(encoding.encode(texto))

print(f"Quantidade de tokens pela API tiktoken: {tokens}")



