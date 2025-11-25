from flask import Flask, jsonify, request
import anthropic
import os

app = Flask(__name__)

# Configurar cliente de Anthropic (usando variable de entorno)
# En producción, esto debería estar en variables de entorno del contenedor
client = None

@app.route('/')
def hello():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CI/CD - David Cocha</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .feature {
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .badge {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 12px;
                margin: 5px 5px 5px 0;
            }
            .chat-section {
                margin-top: 30px;
                padding-top: 30px;
                border-top: 2px solid #eee;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 14px;
                resize: vertical;
                box-sizing: border-box;
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
                margin-top: 10px;
                transition: background 0.3s;
            }
            button:hover {
                background: #5568d3;
            }
            #response {
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 CI/CD Pipeline - Examen Final</h1>
            <p class="subtitle">Proyecto automatizado con GitHub Actions + Docker Swarm</p>
            
            <div class="feature">
                <strong>✅ Características implementadas:</strong><br>
                <span class="badge">GitHub Actions</span>
                <span class="badge">Docker</span>
                <span class="badge">GHCR</span>
                <span class="badge">Traefik</span>
                <span class="badge">Tests automatizados</span>
                <span class="badge">IA con Claude</span>
            </div>
            
            <div class="feature">
                <strong>📦 Versión de imagen:</strong> cocha:1.0.5<br>
                <strong>🌐 Subdominio:</strong> pgcocha.byronrm.com<br>
                <strong>👨‍💻 Estudiante:</strong> David Cocha
            </div>

            <div class="chat-section">
                <h3 style="color: #667eea;">💬 Pregúntale a Claude</h3>
                <textarea id="userInput" rows="4" placeholder="Escribe tu pregunta aquí..."></textarea>
                <button onclick="askClaude()">Enviar pregunta</button>
                <div id="response"></div>
            </div>
        </div>

        <script>
            async function askClaude() {
                const input = document.getElementById('userInput').value;
                const responseDiv = document.getElementById('response');
                
                if (!input.trim()) {
                    alert('Por favor escribe una pregunta');
                    return;
                }
                
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = '⏳ Pensando...';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: input })
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        responseDiv.innerHTML = `<strong style="color: #e74c3c;">❌ Error:</strong> ${data.error}`;
                    } else {
                        responseDiv.innerHTML = `<strong style="color: #667eea;">🤖 Claude responde:</strong><br><br>${data.response}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `<strong style="color: #e74c3c;">❌ Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/ask', methods=['POST'])
def ask():
    """Endpoint para interactuar con Claude AI"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No se proporcionó una pregunta'}), 400
        
        # Verificar si hay API key configurada
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({
                'response': 'ℹ️ La integración con IA está configurada pero requiere una API key de Anthropic. '
                           'Para este demo, puedo confirmar que la aplicación funciona correctamente con Flask, '
                           'está desplegada via CI/CD y tiene pruebas automatizadas. '
                           f'Tu pregunta fue: "{question}"'
            })
        
        # Si hay API key, usar Claude
        global client
        if client is None:
            client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        
        return jsonify({'response': message.content[0].text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Endpoint para health checks"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.5',
        'student': 'David Cocha',
        'project': 'CI/CD Pipeline Exam'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)