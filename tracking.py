import cv2
import numpy as np


class CSRTTracker:
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.initialized = False
        self.msg_control = 0

    def initialize(self, frame, bbox):
        self.tracker.init(frame, bbox)
        self.initialized = True

    def update(self, frame):
        if not self.initialized:
            return None

        success, bbox = self.tracker.update(frame)
        if success:
            return bbox
        else:
            return None

    def detect_and_initialize(self, frame):

        # Converter para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir intervalos para a cor verde fluorescente
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        # Criar uma máscara para a cor verde
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # Encontrar contornos
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Defina os limites mínimos e máximos para a área do cartão
            min_area = 200
            max_area = 200000

            # Verifique se o contorno está dentro dos limites
            if min_area < w * h < max_area:
                self.msg_control = 0
                print(f"Inicializando tracker com ROI: {x}, {y}, {w}, {h}")
                self.initialize(frame, (x, y, w, h))
            else:
                if self.msg_control == 0:
                    self.msg_control = 1
                    print("Contorno encontrado não corresponde ao tamanho esperado do cartão.")
                return
        else:
            if self.msg_control == 0:
                self.msg_control = 1
                print("Nenhum contorno verde detectado.")
            return
