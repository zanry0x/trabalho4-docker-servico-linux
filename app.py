from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import signal
import time

PORT = int(os.getenv("PORT", "8080"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def registrar(mensagem):
    agora = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{agora} [{LOG_LEVEL}] {mensagem}", flush=True)


class ServicoHandler(BaseHTTPRequestHandler):
    def responder_json(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        registrar(f"Requisição recebida: {self.path}")

        if self.path == "/":
            self.responder_json(200, {
                "mensagem": "Serviço do Trabalho 4 está em execução",
                "pid": os.getpid(),
                "uid": os.getuid(),
                "porta": PORT
            })

        elif self.path == "/health":
            self.responder_json(200, {"status": "ok"})

        elif self.path == "/fail":
            registrar("Falha controlada solicitada. Encerrando processo com código 1.")
            self.responder_json(500, {"erro": "Falha controlada acionada"})
            os._exit(1)

        else:
            self.responder_json(404, {"erro": "Rota não encontrada"})

    def log_message(self, formato, *args):
        return


def encerrar_graciosamente(sinal, quadro):
    registrar("SIGTERM recebido. Encerrando o serviço normalmente.")
    raise SystemExit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, encerrar_graciosamente)
    registrar(f"Serviço iniciado na porta {PORT}, com UID {os.getuid()}")
    servidor = ThreadingHTTPServer(("0.0.0.0", PORT), ServicoHandler)
    servidor.serve_forever()