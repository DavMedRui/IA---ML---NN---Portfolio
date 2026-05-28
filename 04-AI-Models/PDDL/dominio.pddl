(define (domain robot-camarero)
  (:requirements :typing)

  (:types habitacion robot)

  (:predicates
    (en ?r - robot ?h - habitacion)
    (conectadas ?h1 - habitacion ?h2 - habitacion)
  )

  (:action mover
    :parameters (?r - robot ?desde - habitacion ?hacia - habitacion)
    :precondition (and
        (en ?r ?desde)
        (conectadas ?desde ?hacia)
    )
    :effect (and
        (not (en ?r ?desde))
        (en ?r ?hacia)
    )
  )
)
