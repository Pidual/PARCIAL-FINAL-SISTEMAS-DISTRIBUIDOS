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






SECCION 2
Crear un archivo docker-compose.yml que incluya los servicios:
● api
● worker
● rabbitmq
● traefik

1 Como primer paso creamos el docker compose
![image](https://github.com/user-attachments/assets/eb3314d0-f0be-4da8-8bcf-626c73da59fe)

2 Paso implementar una API REST  POST /message que reciba un cuerpo JSON y lo publique en una cola RabbitMQ llamada messages. También debe asegurar el endpoint mediante autenticación básica. para esta API le dije a claude Sonnet thinking 3.7 que la programara 
![image](https://github.com/user-attachments/assets/8022b6b6-ebd3-40e5-8686-aa37c3f798dc)



3. Crear un worker que escuche la cola messages y escriba el contenido de los mensajes en un archivo local usando un volumen para persistencia.
FUe el mismo proceso anterior le pedi a claude que me ayudara con a implementacion por cierto en este programa podemos encontrar la creacion de canales de rabbitmq en la funcion main del script
![image](https://github.com/user-attachments/assets/afcbcafe-8c1c-4ad8-8791-c376d9a37e29)

4 Configurar Traefik para enrutar las siguientes rutas:
 /api hacia el servicio api.
 /monitor hacia la interfaz web de RabbitMQ.
Esta configuración debe se realizo con label dentro de docker-compose.yml.
Labels para el servicio de traefik 
![image](https://github.com/user-attachments/assets/efce6814-af4b-48ad-8897-5021674bde1f)











