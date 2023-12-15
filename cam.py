import cv2
import segmentation
import findobjects
import tracking

camera_index = 0
cap = cv2.VideoCapture(camera_index)

initialize_doonly = 0
doonly = 0
showFindObjects = False
showSegmentation = False
showTracking = False


def drawcircle_tracking(frame, center):
    # Desenhe um círculo vermelho no centro
    frame_tracking = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.circle(frame_tracking, center, 5, (0, 0, 255), -1)
    cv2.imshow("Result Tracking", frame_tracking)


def drawcircle_findobject(frame, center):
    # Desenhe um círculo vermelho no centro
    frame_findobject = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.circle(frame_findobject, center, 5, (0, 0, 255), -1)
    cv2.imshow("Result Find Objects", frame_findobject)


def drawcircle_segmentation(frame, center, mask):
    # Desenhe um círculo vermelho no centro
    frame_segmentation = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.circle(frame_segmentation, center, 5, (0, 0, 255), -1)
    cv2.imshow("Result Segmentation", frame_segmentation)


def get_cap():
    return cap




def start_camloop(metodo):
    global doonly, initialize_doonly, showFindObjects, showSegmentation, showTracking

    # Verifica se a câmera foi inicializada com sucesso
    if not cap.isOpened():
        cap.open(camera_index)

    while True:

        ret, frame_og = cap.read()
        if not ret:
            print("Erro ao capturar o quadro.")
            break

        frame = cv2.flip(frame_og, 1)


        if initialize_doonly == 0:
            segmentation.create_trackbar()
            initialize_doonly = 1

        # Frame de cada metodo para evitar conflitos
        frame_segmentation = frame
        frame_findobjects = frame
        frame_tracking = frame
        print(metodo)

        # Variaveis
        gradient = findobjects.process_frame(frame_findobjects, showFindObjects)
        frame_result, bbox = tracking.execute_tracking(frame_tracking, showTracking)
        image_hsv = cv2.cvtColor(frame_segmentation, cv2.COLOR_BGR2HSV)
        mask = segmentation.update_segmentation(image_hsv, showSegmentation)

        if metodo == 1:
            doonly = 0

            showTracking = True
            showFindObjects = False
            showSegmentation = False

            center_tracking = tracking.calculate_center(bbox)
            if center_tracking is not None:
                center_card_x = center_tracking[0]
                drawcircle_tracking(frame, center_tracking)
                return center_card_x
            else:
                return 0
        elif metodo == 2:
            doonly = 0

            showFindObjects = True
            showSegmentation = False
            showTracking = False

            center_findobject = findobjects.find_card_center(gradient)
            if center_findobject is not None:
                center_card_x = center_findobject[0]
                drawcircle_findobject(frame, center_findobject)
                return center_card_x
            else:
                return 0
        elif metodo == 3:
            if doonly == 0:
                segmentation.create_trackbar()
                doonly = 1

            showSegmentation = True
            showFindObjects = False
            showTracking = False

            center_segmentation = segmentation.segmentate_card_center(mask)
            if center_segmentation is not None:
                center_card_x = center_segmentation[0]
                drawcircle_segmentation(frame, center_segmentation, mask)
                return center_card_x
            else:
                return 0
        elif metodo == 4:
            doonly = 0

            showFindObjects = True
            showSegmentation = True
            showTracking = True

            # Calcula os centros
            center_findobject = findobjects.find_card_center(gradient)
            center_segmentation = segmentation.segmentate_card_center(mask)
            center_tracking = tracking.calculate_center(bbox)

            # Mostra todos e calcula a media de todos os centros caso existam
            if center_segmentation and center_tracking and center_findobject is not None:
                center_card_x = (center_segmentation[0] + center_findobject[0] + center_tracking[0]) / 3
                drawcircle_tracking(frame, center_tracking)
                drawcircle_findobject(frame, center_findobject)
                drawcircle_segmentation(frame, center_segmentation, mask)
                # Foca em todas as visoes ao mesmo tempo porem calcula uma media dos 3 centros
                return center_card_x
            else:
                return 0
        else:
            print("Método não encontrado")

            center_card_x = 0
            return center_card_x
