import pika
import datetime
import ssl

def main():
    # Configurações de conexão
    url = 'amqps://xliciseh:8kV_rlN6kX0t9LcC-9Juz4bdVqU8jzuj@prawn.rmq.cloudamqp.com/xliciseh'

    parameters = pika.URLParameters(url)
    parameters.ssl_options = pika.SSLOptions(ssl.create_default_context())

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declaração do exchange
    channel.exchange_declare(exchange='notificacoes_corporativas', exchange_type='topic')

    # Criação de uma fila temporária
    result = channel.queue_declare(queue='auditoria', auto_delete=False)
    queue_name = result.method.queue

    # Associação da fila ao exchange com a binding key '#'
    channel.queue_bind(exchange='notificacoes_corporativas', queue=queue_name, routing_key='rh.#')

    print("Backend de Auditoria iniciando... Todas as mensagens serão gravadas em 'auditoria_log.txt'.")

    # Função callback para processar as mensagens recebidas
    def callback(ch, method, properties, body):
        mensagem = body.decode('utf-8')
        routing_key = method.routing_key
        log_entry = f"[{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}] Routing Key: '{routing_key}' - Mensagem: {mensagem}\n"
        print(f"Mensagem recebida e gravada: {mensagem}")

        # Abrindo o arquivo em modo de adição
        f = open('auditoria_log.txt', 'a')
        try:
            # Escrevendo a entrada de log no arquivo
            f.write(log_entry)
        finally:
            # Fechando o arquivo manualmente
            f.close()
            
    # Início do consumo
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Backend de Auditoria aguardando mensagens. Pressione CTRL+C para sair.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
        print('Backend de Auditoria encerrado.')

if __name__ == "__main__":
    main()
