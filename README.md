# 🛠️ Sistema de notificação corporativa

Esse projeto é um sistema de notificações corporativas que utiliza o **RabbitMQ** para facilitar a comunicação entre diferentes departamentos de uma empresa (RH e TI). As mensagens enviadas são roteadas com base em **keys de tópicos**, permitindo que consumidores recebam notificações específicas. Além disso, há um **backend de auditoria** que registra todas as mensagens enviadas.

## 📋 Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados:

- Python 3.x
- Java 8 ou superior
- Biblioteca `pika` (para Python)
- Biblioteca `amqp-client` (para Java)

### 🔧 Dependências Python
Instale as dependências do Python para o produtor e backend de auditoria:

```
pip install pika
```

### 🐇 Configurações do RabbitMQ

Estamos utilizando uma instância do CloudAMQP (RabbitMQ hospedado na nuvem). As configurações de conexão são as seguintes:

```
spring.rabbitmq.host=prawn-01.rmq.cloudamqp.com
spring.rabbitmq.password=w1V5VdNdygWzDwsY5pi5C7p3pguzAwh0
spring.rabbitmq.virtual-host=btykjupb
spring.rabbitmq.username=btykjupb
spring.rabbitmq.addresses=amqps://btykjupb:w1V5VdNdygWzDwsY5pi5C7p3pguzAwh0@prawn.rmq.cloudamqp.com/btykjupb
```

### 🚀 Como executar o projeto

1 - Rodar o arquivo `auditoria.py`
```
python auditoria.py
```

2 - Rodar o arquivo `ClasseConsumidor.java`
```
javac classeConsumidor.java
```

3 - Rodar o arquivo `prod.py`
```
python prod.py
```

**⚠️ A sequência pode variar de acordo com o cenário que vai ser testado. ⚠️**

https://www.youtube.com/watch?v=pPQHttPxOts
