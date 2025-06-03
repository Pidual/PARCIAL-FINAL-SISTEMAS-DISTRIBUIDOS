# Parcial Final - Arquitectura de Microservicios

## SECCIÓN 1: CONCEPTOS TEÓRICOS

### 1.1 RabbitMQ

#### ¿Qué es RabbitMQ y cuándo se debe utilizar una cola frente a un exchange tipo fanout?

RabbitMQ es un broker de mensajería de código abierto que implementa el protocolo AMQP (Advanced Message Queuing Protocol). Actúa como intermediario para la comunicación asíncrona entre diferentes servicios, permitiendo el desacoplamiento entre productores y consumidores de mensajes.

**Diferencia entre cola y exchange tipo fanout:**
- **Cola (Queue)**: Se debe utilizar cuando necesitamos un patrón de comunicación punto a punto, donde cada mensaje debe ser procesado por un único consumidor. Las colas garantizan que un mensaje será entregado a un solo consumidor, lo que es ideal para distribuir tareas entre workers y asegurar que cada tarea se procese una sola vez.

- **Exchange tipo fanout**: Se debe utilizar cuando necesitamos un patrón de comunicación de publicación/suscripción, donde cada mensaje debe ser enviado a múltiples consumidores. Un exchange fanout distribuye todos los mensajes que recibe a todas las colas que están enlazadas a él. Es ideal para notificaciones en tiempo real, actualizaciones de estado o cualquier escenario donde múltiples servicios necesiten recibir la misma información.

#### ¿Qué es una Dead Letter Queue (DLQ) y cómo se configura en RabbitMQ?

Una **Dead Letter Queue (DLQ)** es una cola especial donde se envían los mensajes que no pudieron ser procesados correctamente por los consumidores o que expiraron antes de ser consumidos. Esto permite capturar mensajes fallidos para su posterior análisis, reintento o notificación.

**Configuración en RabbitMQ:**

1. Crear un exchange para dead letters:
```python
channel.exchange_declare(exchange='dlx', exchange_type='direct')
```

## SECCIÓN 2: CONFIGURACIÓN DE TRAEFIK

### 2.1 Configuración Básica

Para exponer nuestros microservicios al exterior de manera segura y eficiente, utilizaremos Traefik como nuestro proxy inverso y balanceador de carga. A continuación se detalla la configuración básica de Traefik en un entorno Docker.

**Archivo `docker-compose.yml`:**
```yaml
services:
  traefik:
    image: traefik:v2.9
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - web
    command:
      - "--api.dashboard=true"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.localhost`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.entrypoints=web"
```