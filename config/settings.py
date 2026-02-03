SERVER_IP = "0.0.0.0"         # Écoute sur toutes les interfaces
SERVER_PORT = 5000

# === RÉSOLUTION & QUALITÉ (optimisées pour la fluidité) ===
# Résolution adaptée au réseau : plus basse = plus fluide
# Option 1 (TRÈS FLUIDE - réseau lent)  : 800x600
# Option 2 (FLUIDE - réseau moyen)      : 1024x768
# Option 3 (BON ÉQUILIBRE)              : 1280x720  <- RECOMMANDÉ
# Option 4 (QUALITÉ - réseau rapide)    : 1920x1080
WIDTH = 1024
HEIGHT = 768

# FPS : 20 = bon équilibre, 30 = meilleur, 15 = très fluide (réseau lent)
FPS = 20

# Qualité JPEG (1-100) : 
# 40-50 = très comprimé (fluide, moins de détails)
# 60-70 = bon équilibre
# 80+ = haute qualité (plus lent)
JPEG_QUALITY = 45