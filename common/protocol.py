# Types de messages
MSG_FRAME = 1
MSG_CONTROL_REQUEST = 2
MSG_CONTROL_RESPONSE = 3
MSG_INPUT = 4  # Données d'entrée (souris/clavier) du client
MSG_RELEASE_CONTROL = 5  # Client libère le contrôle

# Réponses possibles pour la demande de contrôle
CONTROL_ACCEPTED = 1
CONTROL_REFUSED = 0

# Type d'entrées (utilisé dans MSG_INPUT)
INPUT_MOUSE = 10
INPUT_KEYBOARD = 11
