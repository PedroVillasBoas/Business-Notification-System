package com.example.Consumidor;

import org.springframework.stereotype.Component;

@Component
public class Reciever {

    // Método que será chamado quando uma mensagem for recebida
    public void receiveMessage(String message) {
        System.out.println(" [x] Recebido: '" + message + "'");
    }
}
