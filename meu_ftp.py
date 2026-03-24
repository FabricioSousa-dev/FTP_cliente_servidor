import ftplib
from pathlib import Path

try:
    from tqdm import tqdm

    TEM_TQDM = True
except ImportError:
    TEM_TQDM = False


class ClienteFTPAvancado:
    def __init__(self, conexao_segura: bool = False):
        self.ftp = ftplib.FTP_TLS() if conexao_segura else ftplib.FTP()
        self.conectado = False
        self.seguro = conexao_segura

    def conectar(self, host: str, usuario: str, senha: str):
        try:
            protocolo = "FTPS" if self.seguro else "FTP"
            print(f"[*] Conectando a {host} via {protocolo}...")

            self.ftp.connect(host)
            self.ftp.login(usuario, senha)

            if self.seguro:
                self.ftp.prot_p()

            self.conectado = True
            print("[+] Conexão e autenticação realizadas com sucesso!")
        except Exception as e:
            print(f"[-] Erro ao conectar: {e}")

    def listar_arquivos(self):
        if not self.conectado:
            print("[-] Conecte-se primeiro.")
            return

        try:
            print("\n" + "=" * 40)
            self.ftp.retrlines('LIST')
            print("=" * 40 + "\n")
        except Exception as e:
            print(f"[-] Erro ao listar arquivos: {e}")

    def baixar_arquivo(self, nome_remoto: str, pasta_destino: str = "."):
        if not self.conectado:
            print("[-] Conecte-se primeiro.")
            return

        caminho_local = Path(pasta_destino) / nome_remoto

        try:
            tamanho = self.ftp.size(nome_remoto)
            print(f"[*] Baixando '{nome_remoto}'...")

            with open(caminho_local, 'wb') as arquivo:
                if TEM_TQDM and tamanho:
                    with tqdm(total=tamanho, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                        def callback_progresso(dados):
                            arquivo.write(dados)
                            pbar.update(len(dados))

                        self.ftp.retrbinary(f"RETR {nome_remoto}", callback_progresso)
                else:
                    self.ftp.retrbinary(f"RETR {nome_remoto}", arquivo.write)

            print(f"[+] Download concluído! Salvo em: {caminho_local.absolute()}")

        except Exception as e:
            print(f"[-] Erro ao baixar arquivo: {e}")

    def enviar_arquivo(self, caminho_local: str, nome_remoto: str = None):
        if not self.conectado:
            print("[-] Conecte-se primeiro.")
            return

        arquivo_local = Path(caminho_local)

        if not arquivo_local.is_file():
            print(f"[-] Erro: O arquivo '{arquivo_local}' não existe.")
            return

        if not nome_remoto:
            nome_remoto = arquivo_local.name

        try:
            tamanho = arquivo_local.stat().st_size
            print(f"[*] Enviando '{arquivo_local.name}'...")

            with open(arquivo_local, 'rb') as arquivo:
                if TEM_TQDM:
                    with tqdm(total=tamanho, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                        def callback_progresso(dados):
                            pbar.update(len(dados))

                        self.ftp.storbinary(f"STOR {nome_remoto}", arquivo, callback=callback_progresso)
                else:
                    self.ftp.storbinary(f"STOR {nome_remoto}", arquivo)

            print("[+] Upload concluído com sucesso!")

        except Exception as e:
            print(f"[-] Erro ao enviar arquivo: {e}")

    def desconectar(self):
        if self.conectado:
            try:
                self.ftp.quit()
            except:
                self.ftp.close()
            finally:
                self.conectado = False
                print("[*] Desconectado.")


def menu():
    print("=======================================")
    print("      CLIENTE FTP/FTPS AVANÇADO        ")
    print("=======================================")

    usar_seguranca = input("Usar conexão segura FTPS? (s/n): ").strip().lower() == 's'
    cliente = ClienteFTPAvancado(conexao_segura=usar_seguranca)

    host = input("Endereço do Servidor: ")
    user = input("Usuário: ")
    senha = input("Senha: ")

    cliente.conectar(host, user, senha)
    if not cliente.conectado: return

    while True:
        print("\n[1] Listar  [2] Baixar  [3] Enviar  [4] Sair")
        opcao = input("Opção: ").strip()

        if opcao == '1':
            cliente.listar_arquivos()
        elif opcao == '2':
            remoto = input("Nome do arquivo no servidor: ")
            cliente.baixar_arquivo(remoto)
        elif opcao == '3':
            local = input("Caminho do arquivo no PC: ")
            cliente.enviar_arquivo(local)
        elif opcao == '4':
            cliente.desconectar()
            break
        else:
            print("[-] Opção inválida.")


if __name__ == "__main__":
    menu()