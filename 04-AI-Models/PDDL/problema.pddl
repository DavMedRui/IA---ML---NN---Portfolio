(define (problem robot-camarero-habitacion)
  (:domain robot-camarero)

  (:objects
    r - robot
    hab1 hab2 aseo pasillo recibidor salon cocina - habitacion
  )

  (:init
    ;; situamos al robot en una habitación, por ejemplo en el recibidor
    (en r hab1)

    ;; conexiones con el pasillo
    (conectadas pasillo hab1)
    (conectadas hab1 pasillo)
    (conectadas pasillo hab2)
    (conectadas hab2 pasillo)
    (conectadas pasillo aseo)
    (conectadas aseo pasillo)
    (conectadas pasillo recibidor)
    (conectadas recibidor pasillo)
    (conectadas pasillo salon)
    (conectadas salon pasillo)
    (conectadas pasillo cocina)
    (conectadas cocina pasillo)

    ;; conexiones entre habitaciones
    (conectadas recibidor salon)
    (conectadas salon recibidor)
    (conectadas salon cocina)
    (conectadas cocina salon)
  )

  (:goal
    (en r cocina)
  )
)
