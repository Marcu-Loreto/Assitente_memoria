from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)


client = OpenAI(api_key=OPENAI_API_KEY)
 #Prompt do sistema lido de um arquivo externo
with open("Prompt/prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()
#Base de conehcimento lido de arquivo externo

with open ("conhecimento/rag_01.txt", "r" , encoding = "utf-8" ) as file:
    rag = file.read()

# Entrada do usuário
MAX_MEMORY = 10
memory = []
def limitar_memoria():
    global memory
    if len(memory) > MAX_MEMORY:
        memory = memory[-MAX_MEMORY:]
    

if __name__ == "__main__":
    # Inicializa a memória com o prompt do sistema
    memory = [{"role": "system", "content": prompt}]
    
    while True:
        pergunta_user = input("Você: ")
        if pergunta_user.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o assistente...")
            break

        memory.append({"role": "user", "content": pergunta_user})
        limitar_memoria()

# Faz a requisição ao modelo da OpenAI
        response = client.chat.completions.create(
            model= "gpt-4.1-nano" ,  #os.getenv("model", "gpt-4.1-nano"),
            messages= memory
        )
         
        # Extrai a resposta da IA e o número de tokens usados
        resposta_ia = response.choices[0].message.content
        tokens_usados = response.usage.total_tokens
    
        memory.append({"role" : "assistente", "content" : resposta_ia}) # Adiciona a resposta da IA à memória
        limitar_memoria()
         
# Mostra os resultados separadamente
        print("\n🤖 Resposta da IA:")
        print(resposta_ia)
        print(f"\n📊 Tokens usados: {tokens_usados}")

        usage = response.usage
        print(f"Tokens de  Prompt : {usage.prompt_tokens}, Tokens de resposta : {usage.completion_tokens}, Total de tokens: {usage.total_tokens}")
        custo_total = ((usage.prompt_tokens * 0.20) + (usage.completion_tokens * 0.80)) 

        print(f"Custo total: US$ {custo_total / 1_000_000:.8f}")

        #print( memory)



