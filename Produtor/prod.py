import pika
import datetime
import ssl

def send_message(producer_name, routing_key):
    # Configurações de conexão
    url = 'amqps://xliciseh:8kV_rlN6kX0t9LcC-9Juz4bdVqU8jzuj@prawn.rmq.cloudamqp.com/xliciseh'

    # Parâmetros de conexão
    parameters = pika.URLParameters(url)
    parameters.ssl_options = pika.SSLOptions(ssl.create_default_context())

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declaração do exchange do tipo 'topic'
    channel.exchange_declare(exchange='notificacoes_corporativas', exchange_type='topic')

    while True:
        mensagem = input("Digite a mensagem (ou 'sair' para encerrar): ")
        if mensagem.lower() == 'sair':
            break
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")
        mensagem_formatada = f"[{timestamp}] {producer_name}: \"{mensagem}\""
        channel.basic_publish(exchange='notificacoes_corporativas',
                              routing_key=routing_key,
                              body=mensagem_formatada,
                              properties=pika.BasicProperties(
                                delivery_mode=2,  # Tornar a mensagem persistente
                              )
        )
        print(f"Enviada: {mensagem_formatada}")
    connection.close()

def main():
    print("==== Sistema de Notificação Corporativa ====")
    print("Selecione o produtor:")
    print("1. Produtor de RH")
    print("2. Produtor de TI")
    escolha = input("Opção: ")

    if escolha == '1':
        producer_name = 'RH'
        print("\nSelecione o tipo de mensagem:")
        print("1. Notificações Gerais")
        print("2. Ofertas de Benefícios Exclusivas")
        tipo_mensagem = input("Opção: ")
        if tipo_mensagem == '1':
            routing_key = 'rh.geral'
        elif tipo_mensagem == '2':
            routing_key = 'rh.beneficios'
        else:
            print("Opção inválida.")
            return
    elif escolha == '2':
        producer_name = 'TI'
        print("\nSelecione o tipo de mensagem:")
        print("1. Alertas Críticos e de Segurança")
        print("2. Manutenção")
        tipo_mensagem = input("Opção: ")
        if tipo_mensagem == '1':
            routing_key = 'ti.alerta'
        elif tipo_mensagem == '2':
            routing_key = 'ti.manutencao'
        else:
            print("Opção inválida.")
            return
    else:
        print("Opção inválida.")
        return

    print(f"\nIniciando {producer_name} produtor...")
    send_message(producer_name, routing_key)

if __name__ == "__main__":
    main()
