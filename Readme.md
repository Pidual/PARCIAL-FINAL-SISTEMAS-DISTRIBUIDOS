# Parcial Final - Arquitectura de Microservicios

## SECCIÓN 1: CONCEPTOS TEÓRICOS

RabbitMQ
● Explique qué es RabbitMQ y cuándo se debe utilizar una cola frente a un exchange tipo fanout
un fanout es cuando no nos importa a quien le llegue
un exchange tiene filtros para decidir a quien le va llegar el mensaje
● ¿Qué es una Dead Letter Queue (DLQ) y cómo se configura en RabbitMQ?
Es un sistema para hacer que mensajes que nunca fueron enviados sean procesados

Docker y Docker Compose
● Diferencia entre un volumen y un bind mount con ejemplos: un volumen es dentro de docker y un bind mount utiliza una carpeta por fuera de docker
● ¿Qué implica usar network_mode: host en un contenedor?. Que utiliza su propia red jjj

Traefik
● Función de Traefik en una arquitectura de microservicios. muy util para mandarle al microservicio que le corresponda, ademas hace load balancer y mucha mas magia pero prefiero no usarlo
● ¿Cómo se puede asegurar un endpoint usando certificados TLS automáticos
en Traefik?, usando un self singed certificate ni idea pero de alguna forma nos da HTTPS 


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
Esta configuración debe se la realizo claude jaja puso labels  dentro de docker-compose.yml.
Labels para el servicio de traefik 




5. Healt Checks
   ![image](https://github.com/user-attachments/assets/558f0fd8-490d-4ae3-b9f1-d2df7ada2c16)
por medio de helat checks podemos revisar en este caso esta configurado para 30 segundos 








