import cv2
import segmentation
import findobjects


camera_index = 0

cap = cv2.VideoCapture(camera_index)


def get_cap():
    return cap


def start_camloop():
    # Inicializa a camera uma primeira vez
    if not cap.isOpened():
        cap.open(0)
        _, frame = cap.read()
        cv2.imshow("Frame", frame)

    # Verifica se a camera foi inicializada com sucesso
    if not cap.isOpened():
        cap.open(0)
    else:
        # Capture um quadro da câmera
        ret, frame = cap.read()
        # Verifica se a captura foi bem-sucedida
        if not ret:
            print("Erro ao capturar o quadro.")

        else:
            # Exibe o quadro em uma janela
            frame = frame[:, ::-1, :]

            cv2.imshow('Frame', frame)
            window_size = cv2.getWindowImageRect('Frame')
            print(window_size[2], window_size[3])

            image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


            # METODOS APLICADOS
            # Variaveis dos metodos
            mask = segmentation.update_segmentation(image_hsv)
            gradient = findobjects.process_frame(frame, mask)

            # Calcule o centro do cartão verde na detecção de objetos
            center_fb = findobjects.calculate_card_center(gradient)
            if center_fb is not None:
                center_x = center_fb[0]

                # Converta o quadro para o tipo cv::Mat
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Desenhe um círculo vermelho no centro
                cv2.circle(frame, center_fb, 5, (0, 0, 255), -1)
                cv2.imshow("Result FB", frame)
                return center_x


            # Calcule o centro do cartão verde na imagem segmentada
            center = segmentation.find_card_center(mask)
            if center is not None:
                center_x = center[0]  # Valor x do centro

                # Converta o quadro para o tipo cv::Mat
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Desenhe um círculo vermelho no centro
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                cv2.imshow("Result SEG", frame)
                return center_x
