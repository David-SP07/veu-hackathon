import cv2
import numpy as np

# Cargar imagen
imagen = cv2.imread('images.jpeg')

# Redimensionar la imagen para procesamiento más rápido (opcional)
imagen = cv2.resize(imagen, (800, 600))

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar desenfoque para reducir ruido
desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)

# Detección de bordes
bordes = cv2.Canny(desenfoque, 50, 150)

# Encontrar contornos
contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos que sean "posibles baches" (áreas entre 500 y 5000 píxeles por ejemplo)
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if 500 < area < 5000:
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Rectángulo rojo
        cv2.putText(imagen, "Bache?", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Mostrar resultados
cv2.imshow('Baches Detectados', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()