Capa de transporte se encarga de conexion entre los extremos y comunicacion de los extremos
Dos protocolos importantes:
- Udp: Solo se mandan los datagramas para la capa 3, no importa la comunicación y la conexio entre 
- TCP: Si importa la conexión, es una comunicación entre extremos muy civilisados.

Taller: Implementar TCP usando sockets y solo UDP.

- Hacer dos extremos en localhost que se pueden comunicar.
- Primer paso un emisor que se le pasa un texto por entrada estandar y se le manda a un receptor por udp y lo imprima en pantalla.
- usar tc qdisc add dev lo root netem loss 20% delay 0.5s para añadir delay o perdida a las conexiones de 20 porciento y delay de 0.5 segundos
- podemos cambiarlo con tc qdisc change dev lo root netem loss 20% delay 5s para tener delay de 5s

TCP usa tres packetes de handshake para usar comunicacion a dos vias en ambos sentidos. Para cerrar la conexion el emisor pone un paquete FIN y pasa a un estado FIN_WAIT_1, luego el receptor entrega un paquete ACK y pasa a un estado CLOSE_WAIT, espera y luego manda un paquete FIN. El emisor recive el AKC y espera un ultimo paquete FIN para luego mandar un ultimo paquete ACK al receptor. Este al recibir el paquete ACK cierra su conexion y 

El stop and wait del TCP es para enviar cualquier tipo de paquetes siguiendo el mismo modelo de transmision. Cada paquete debe tener una secuencia (ordenadamente) y el recepto debe transmitir un paquete con la misma sequencia pero con flag ACK activada. Esto le indica al emisor que no hubo perdida de informacion entremedio. Para detectar perdida, el emisor espera un tiempo para recibir el paquete ACK, en caso de no ser recibido envia nuevamente el paquete de la sequencia asumiendo que hubo perdida de la informacion.



Recomendaciones:
    - Generar el stop and wait de envio de paquetes primero
    - Generar el handshake despues usando el stop and wait
    - Generar el fin de comunicacion