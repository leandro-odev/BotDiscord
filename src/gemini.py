import json
import google.generativeai as genai

with open("D:\programacao\Gemini-Discord-Bot\src\config.json", "r") as file:
    config = json.load(file)

gemini_token = config["gemini_api_key"]

genai.configure(api_key=gemini_token)

# Configurações do modelo
generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 4000,
    "response_mime_type": "text/plain",
}

# Criação do modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Função para gerar a mensagem
def generate_message(message, historico):
    formatted_history = []
    
    # Adiciona o histórico de mensagens no formato de dicionário certo
    for user_msg, bot_msg in historico:
        formatted_history.append({
            "role": "user",
            "parts": [user_msg]
        })
        formatted_history.append({
            "role": "model",
            "parts": [bot_msg]
        })

    # Adiciona a nova mensagem do usuário
    formatted_history.append({
        "role": "user",
        "parts": [message]
    })
    
    
    chat_session = model.start_chat(history=formatted_history)


    # Incluindo personalidades
    with open("D:\programacao\Gemini-Discord-Bot\src\prompts.json", "r") as file:
        prompts = json.load(file)


    prompt = prompts["default"]

    if "Ele" in message or "ele" in message or "morreu" in message or "morto" in message or "morte" in message or "Gojo" in message or "gojo" in message:
        prompt = prompts["gojo"]

    message_with_prompt = prompt + message

    response = chat_session.send_message(message_with_prompt)

    # Extrair o texto da resposta
    if hasattr(response, 'candidates') and response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "Desculpe, não recebi uma resposta válida da API."


# historico_inicial = [
#     ("Apartir de agora você é vascaino", "E aí, vascaíno! ⚡️🖤🤍 A partir de agora, a torcida vai ser ainda mais forte! Me contem tudo sobre o Gigante da Colina: qual o seu ídolo, a sua maior conquista, o que te deixa mais feliz como vascaíno?  Estou pronto para vibrar com cada gol, cada vitória e cada momento épico do Vasco! 🏆 Vamos juntos rumo à glória! 👊")
# ]
# x = generate_message("que coisa boa. qual o maior jogador da historia do seu time", historico_inicial)

# print(x)