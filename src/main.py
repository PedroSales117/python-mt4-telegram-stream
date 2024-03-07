from flask import Flask, request, jsonify
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TELEGRAM_TOKEN)

# Lista dinâmica de rotas
@app.route('/', methods=['GET'])
def home():
    routes = [str(rule) for rule in app.url_map.iter_rules() if rule.endpoint != 'static']
    return jsonify(rotas_disponiveis=routes)

@app.route('/api/sinal', methods=['POST'])
def receber_sinal():
    try:
        acao = request.form.get('acao')
        preco = request.form.get('preco')
        simbolo = request.form.get('simbolo')
        direcao = request.form.get('direcao')
        
        if not all([acao, preco, simbolo, direcao]):
            status=400
            return jsonify(message="Faltam dados na solicitação", status=status), status
        
        mensagem = f"🏆 SINAL {simbolo} {direcao}\n🕐 ENTRADA {preco}\n📊 COM 1G SE NECESSÁRIO\n⏳ Expiração de 1 minuto"
        bot.send_message(chat_id=CHAT_ID, text=mensagem)
        
        status=200
        return jsonify(message="Sinal enviado para o Telegram", status=status), status
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
