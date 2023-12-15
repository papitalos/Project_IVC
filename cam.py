import cv2
import segmentation
import findobjects
import tracking

camera_index = 0
cap = cv2.VideoCapture(camera_index)
tracker = tracking.CSRTTracker()
frame_count = 0
redetection_interval = 30
tracker_initialized = False


def get_cap():
    return cap


def start_camloop():
    global tracker_initialized, frame_count

    # Verifica se a câmera foi inicializada com sucesso
    if not cap.isOpened():
        cap.open(camera_index)

    while True:

        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o quadro.")
            break

        # Frame de cada metodo para evitar conflitos
        frame_segmentation = frame
        frame_findobjects = frame
        frame_tracking = frame

        #Variaveis
        image_hsv = cv2.cvtColor(frame_segmentation, cv2.COLOR_BGR2HSV)
        mask = segmentation.update_segmentation(image_hsv)
        frame_cvmat = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Centers
        center_seg = segmentation.segmentate_card_center(mask)

        # Segmentação de imagens
        # Desenhe um círculo vermelho no centro
        cv2.circle(frame_cvmat, center_seg, 5, (0, 0, 255), -1)

        cv2.imshow("Result Segmentation", frame_segmentation)
