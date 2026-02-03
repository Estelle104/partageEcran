# Processus de Prise de Contrôle

## Flux de demande de contrôle par le client

### 1️⃣ Client appuie sur "p"
```
display.py: show_frame()
    └─ Détecte la touche 'p'
       └─ Appelle send_control_request(sock)
```

### 2️⃣ Envoi de la demande au serveur
```
control.py: send_control_request(sock)
    └─ Envoie struct.pack(">B", MSG_CONTROL_REQUEST)
       └─ Message de 1 byte: [0x02]
```

### 3️⃣ Le serveur traite la demande
```
server.py: handle_client()
    └─ Reçoit MSG_CONTROL_REQUEST
       └─ Demande à l'utilisateur: "Autoriser X.X.X.X à contrôler ? (y/n)"
          ├─ Si OUI:
          │  ├─ controller = sock (marque ce client comme contrôleur)
          │  ├─ Envoie: [MSG_CONTROL_RESPONSE][CONTROL_ACCEPTED]
          │  └─ Lance handle_input_from_controller() en thread séparé
          │
          └─ Si NON:
             ├─ Envoie: [MSG_CONTROL_RESPONSE][CONTROL_REFUSED]
             └─ Continue à servir le flux vidéo
```

### 4️⃣ Client reçoit la réponse
```
client.py: main()
    └─ Après avoir appelé send_control_request()
       └─ Appelle wait_control_response(sock)
          ├─ Reçoit [MSG_CONTROL_RESPONSE][status]
          │
          ├─ Si status == CONTROL_ACCEPTED:
          │  ├─ Affiche "[CLIENT] Contrôle accordé!"
          │  └─ Appelle start_control_mode(sock)
          │
          └─ Si status == CONTROL_REFUSED:
             └─ Affiche "[CLIENT] Contrôle refusé"
```

### 5️⃣ Mode contrôle activé
```
control.py: start_control_mode(sock)
    └─ Lance InputCapture(sock).start()
       ├─ Écoute les mouvements de souris
       ├─ Écoute les clics
       ├─ Écoute les scrolls
       ├─ Écoute les touches clavier
       │
       └─ À chaque événement:
          └─ input_capture.py: send()
             └─ Envoie: [size:>I][MSG_INPUT][json_data]
                │
                ├─ Exemple mouvement souris:
                │  {"type": "mouse_move", "x": 100, "y": 200}
                │
                └─ Exemple clic:
                   {"type": "mouse_click", "x": 100, "y": 200, 
                    "button": "left", "pressed": true}
```

### 6️⃣ Le serveur applique les entrées
```
server.py: handle_input_from_controller()
    └─ Boucle tandis que controller == sock
       └─ Reçoit: [size:>I][MSG_INPUT][json_data]
          │
          ├─ Parse les données JSON
          └─ Appelle input_apply.handle(input_data)
             │
             └─ input_apply.py: handle()
                ├─ Si mouse_move: mouse.position = (x, y)
                ├─ Si mouse_click: mouse.press/release(button)
                ├─ Si mouse_scroll: mouse.scroll(dx, dy)
                ├─ Si key_press: keyboard.press(key)
                └─ Si key_release: keyboard.release(key)
```

### 7️⃣ Client libère le contrôle (Ctrl+C)
```
control.py: start_control_mode()
    └─ Catch KeyboardInterrupt
       └─ Appelle release_control(sock)
          └─ Envoie: [size:>I][MSG_RELEASE_CONTROL]
             │
             └─ server.py reçoit MSG_RELEASE_CONTROL
                └─ controller = None (libère le contrôle)
```

## Format des messages

### MSG_CONTROL_REQUEST (Client → Serveur)
- **Taille**: 1 byte
- **Format**: `[0x02]`
- **Signification**: Le client demande le contrôle

### MSG_CONTROL_RESPONSE (Serveur → Client)
- **Taille**: 2 bytes
- **Format**: `[0x03][status]`
- **Status**: 
  - `0x01` = CONTROL_ACCEPTED
  - `0x00` = CONTROL_REFUSED

### MSG_INPUT (Client → Serveur)
- **Taille**: variable
- **Format**: `[size:4bytes][0x04][json_data]`
- **Exemple**: `[0x00000045][0x04]{"type":"mouse_move","x":100,"y":200}`

### MSG_RELEASE_CONTROL (Client → Serveur)
- **Taille**: variable (généralement 5 bytes)
- **Format**: `[size:4bytes][0x05]`
- **Signification**: Le client libère le contrôle

## États possibles

```
┌─────────────────────────────────────────────────┐
│         Client connecté au serveur              │
│         (reçoit flux vidéo)                     │
└─────────────────┬───────────────────────────────┘
                  │
                  │ Appuie sur 'p'
                  ↓
┌─────────────────────────────────────────────────┐
│    Demande de contrôle envoyée                  │
│    (attend réponse du serveur)                  │
└─────────────────┬───────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
    ACCEPTÉ           REFUSÉ
         │                 │
         ↓                 ↓
    ┌─────────┐      ┌──────────┐
    │EN CONTRÔLE    │VIZUALISATION
    │(souris/clavier)│(lecture seule)
    └────┬────┘      └──────────┘
         │
    Ctrl+C ou déconnexion
         │
         ↓
    ┌─────────────────────────────────────────────────┐
    │         Contrôle libéré                         │
    │    (retour lecture seule)                       │
    └─────────────────────────────────────────────────┘
```

## Permissions

- **Un seul client** peut contrôler à la fois
- **L'utilisateur du serveur** valide chaque demande (y/n)
- Si un client contrôle déjà, les autres demandes sont **automatiquement refusées**
- La déconnexion du client libère automatiquement le contrôle
