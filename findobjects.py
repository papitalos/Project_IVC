import cv2
import numpy as np


def process_frame(frame, showFindObjects):
    # Converter para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Isolar a faixa de cor do cartão verde
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    green_frame = cv2.bitwise_and(hsv_frame, hsv_frame, mask=green_mask)

    # Converte a imagem filtrada para escala de cinza
    image_gray = cv2.cvtColor(green_frame, cv2.COLOR_BGR2GRAY)
    image_gray = image_gray / 255.0

    # Kernels de Prewitt
    Mx_Prewitt = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float64)
    My_Prewitt = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float64)

    # Aplica filtros de Prewitt
    dx_Prewitt = cv2.filter2D(src=image_gray, ddepth=-1, kernel=Mx_Prewitt)
    dy_Prewitt = cv2.filter2D(src=image_gray, ddepth=-1, kernel=My_Prewitt)

    # Calcula gradientes
    gradient_Prewitt = np.sqrt(dx_Prewitt ** 2 + dy_Prewitt ** 2)

    # Define um limiar para identificar pontos de interesse
    threshold = 1.1

    # Identifica pontos de interesse
    points_of_interest = np.where(gradient_Prewitt > threshold)

    # Copia o frame original para desenhar os pontos de interesse
    frame_with_points = frame.copy()

    for y, x in zip(*points_of_interest):
        # Desenha um 'X' vermelho
        cv2.drawMarker(frame_with_points, (x, y), (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS)

    if showFindObjects:
        cv2.imshow('Pontos de Interesse Find Objects', frame_with_points)
    elif cv2.getWindowProperty('Pontos de Interesse Find Objects', cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyWindow('Pontos de Interesse Find Objects')


    return gradient_Prewitt


def find_card_center(image):
    # Aplica limiar para identificar contornos
    ret, thresh = cv2.threshold(image, 0.5, 1.0, cv2.THRESH_BINARY)

    # Encontra contornos
    contours, _ = cv2.findContours((thresh * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Encontrar o maior contorno+-
        max_contour = max(contours, key=cv2.contourArea)

        # Calcula o centro do contorno
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
        else:
            return None
    else:
        return None
