from urllib import response
from openai import OpenAI  
from dotenv import load_dotenv
import os

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializar o cliente OpenAI corretamente
client = OpenAI(api_key=OPENAI_API_KEY)

modelo = os.getenv("model", "gpt-4.1-mini")  # Valor padrão se não definido
temp = float(os.getenv("temperature", "0.7"))  # Converter para float com valor padrão
max_tokens = int(os.getenv("max_tokens", "150"))  # Converter para int com valor padrão
 
print(modelo)  
#print(client)
# Memoria
MAX_MEMORY = 6
memory = []

def limitar_memoria():
    global memory
    if len(memory) > MAX_MEMORY:
        memory = memory[-MAX_MEMORY:]
    
    
    
def pergunta(user_input: str):
    global memory

    # Adicionar a pergunta do usuário à memória
    memory.append({"role": "user", "content": user_input})
    limitar_memoria()
    
    try:
        # print(f"[DEBUG] Enviando para API - Modelo: {modelo}, Temp: {temp}, Max Tokens: {max_tokens}")
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é um assistente de IA Python especializado em desenvolvimento de agentes inteligentes."},
                *memory
            ],
            temperature=temp,
            max_tokens=max_tokens
        )

        assistant_reply = response.choices[0].message.content
        print(f"[DEBUG] Resposta da IA: {assistant_reply}")

        # Captura de tokens
        if response.usage:
            tokens = response.usage
            print(f"[DEBUG] Tokens usados -> prompt: {tokens.prompt_tokens}, completion: {tokens.completion_tokens}, total: {tokens.total_tokens}")

        # Adicionar resposta do assistente à memória
        memory.append({"role": "assistant", "content": assistant_reply})
        limitar_memoria()

        return assistant_reply
    
    except Exception as e:
        error_msg = f"Erro ao conectar com a API: {str(e)}"
        print(f"[ERRO] {error_msg}")
        return error_msg


# Exemplo de uso interativo
if __name__ == "__main__":
    print("🤖 Assistente de IA (com memória limitada a 6 interações)\n")
    print(f"[INFO] Modelo: {modelo}, Temperature: {temp}, Max Tokens: {max_tokens}\n")

    while True:
        user_message = input("Você: ")
        if user_message.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o assistente...")
            break

        reply = pergunta(user_message)
        print(f"\nAssistente: {reply}\n")
        
        print(memory)
        
        # Debug: mostrar o estado atual da memória
        print(f"[DEBUG] Memória atual ({len(memory)} itens)\n")
 #calcular custo dos tokens
 
#  PRECO_POR_1K_TOKENS = 0.01  # exemplo: 1 centavo por mil tokens
# custo = (tokens.total_tokens / 1000) * PRECO_POR_1K_TOKENS
# print(f"[INFO] Custo estimado desta requisição: ${custo:.4f}")
