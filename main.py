from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()
 
# Configurando CORS para permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para o domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para dados recebidos do frontend
class FormData(BaseModel):
    messageType: str
    recipientName: str
    amount: str = None
    dueDate: str
    paymentMethod: str = None

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/generate-message/")
def generate_message(data: FormData):
    # Variações de mensagens para o tipo 'payment'
    payment_messages = [
        f"Olá {data.recipientName},\nGostaríamos de lembrar que há um pagamento pendente no valor de {data.amount}, com vencimento em {data.dueDate}. Por favor, utilize {data.paymentMethod} para realizar o pagamento.",
        f"Prezado(a) {data.recipientName},\nEste é um lembrete sobre o pagamento no valor de {data.amount}, com vencimento em {data.dueDate}. Método de pagamento: {data.paymentMethod}.",
        f"Oi {data.recipientName},\nSeu pagamento no valor de {data.amount} vence em {data.dueDate}. Por favor, realize o pagamento utilizando {data.paymentMethod}.",
    ]

    # Variações de mensagens para o tipo 'formalInvite'
    formal_invite_messages = [
        f"Prezado(a) {data.recipientName},\nÉ com grande prazer que convidamos você para participar do nosso evento especial. Por favor, confirme sua presença até {data.dueDate}. Será uma honra tê-lo(a) conosco.",
        f"Olá {data.recipientName},\nGostaríamos de convidá-lo(a) para um evento especial. Confirme sua presença até {data.dueDate}. Sua participação é muito importante para nós!",
        f"Prezado(a) {data.recipientName},\nEstamos organizando um evento especial e seria uma honra contar com sua presença. Por favor, confirme até {data.dueDate}.",
    ]

    # Escolher a mensagem com base no tipo de mensagem
    if data.messageType == "payment":
        message = random.choice(payment_messages)
    elif data.messageType == "formalInvite":
        message = random.choice(formal_invite_messages)
    else:
        message = "Por favor, escolha um tipo de mensagem válido."

    return {"generatedMessage": message}
