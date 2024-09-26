package com.example.Consumidor;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

public class ClasseConsumidor {

    private static final String EXCHANGE_NAME = "notificacoes_corporativas";

    public static void main(String[] args) throws IOException, TimeoutException, KeyManagementException, NoSuchAlgorithmException, URISyntaxException {
        System.out.println("==== Sistema de Notificação Corporativa ====");
        System.out.println("Selecione o consumidor:");
        System.out.println("1. Consumidor de RH");
        System.out.println("2. Consumidor de TI");
        System.out.print("Opção: ");
        Scanner scanner = new Scanner(System.in);
        String choice = scanner.nextLine();

        String bindingKey;
        String consumerName;

        switch (choice) {
            case "1":
                consumerName = "Consumidor de RH";
                bindingKey = "rh.*";
                break;
            case "2":
                consumerName = "Consumidor de TI";
                bindingKey = "ti.*";
                break;
            default:
                System.out.println("Opção inválida.");
                scanner.close();
                return;
        }

        System.out.println("\nIniciando " + consumerName + "...");

        // Configuração da conexão
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUri("amqps://btykjupb:w1V5VdNdygWzDwsY5pi5C7p3pguzAwh0@prawn.rmq.cloudamqp.com/btykjupb");
        factory.useSslProtocol(); // Habilitar SSL/TLS

        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // Declaração do exchange
        channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.TOPIC);

        // Criação de uma fila temporária
        String queueName = channel.queueDeclare().getQueue();

        // Associação da fila ao exchange com a routing key apropriada
        channel.queueBind(queueName, EXCHANGE_NAME, bindingKey);

        System.out.println(consumerName + " aguardando mensagens...");

        // Callback para recebimento de mensagens
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String mensagem = new String(delivery.getBody(), StandardCharsets.UTF_8);
            String routingKeyReceived = delivery.getEnvelope().getRoutingKey();
            System.out.println("\n[" + consumerName + "] Recebido: '" + mensagem + "' com a chave de roteamento '" + routingKeyReceived + "'");
        };

        // Início do consumo
        channel.basicConsume(queueName, true, deliverCallback, consumerTag -> { });

        // Manter o aplicativo em execução
        System.out.println("Pressione ENTER para sair.");
        scanner.nextLine();

        // Fechamento dos recursos
        channel.close();
        connection.close();
        scanner.close();
    }
}
