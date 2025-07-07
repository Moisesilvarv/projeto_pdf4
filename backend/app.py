from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv(override=True)


app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = 'harmoisah@gmail.com'
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # pega a senha do .env
print("Senha carregada:", EMAIL_PASSWORD)



@app.route('/enviar-pdf', methods=['POST'])
def enviar_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'Nenhum arquivo PDF recebido'}), 400

    pdf_file = request.files['pdf']
    nome_aluno = request.form.get('nome', 'Aluno')

    msg = EmailMessage()
    msg['Subject'] = 'Ficha de Treinamento'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'tutosan5@gmail.com'  # Email do professor

    msg.set_content(f'''
Prezado Professor,

Segue anexo o arquivo PDF com a Ficha de Avaliação Física do aluno {nome_aluno}, contendo os dados e objetivos referentes à sua avaliação.

Ficamos à disposição para quaisquer esclarecimentos ou discussões sobre o conteúdo apresentado.

Atenciosamente,
Moises Da Silva Pimenta.
''')

    pdf_bytes = pdf_file.read()
    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='avaliacao.pdf')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({'success': 'Email enviado com sucesso!'})
    except Exception as e:
        return jsonify({'error': f'Falha ao enviar email: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
