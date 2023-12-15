import cv2
import numpy as np


def initialize_tracker(tracker, frame, bbox):
    tracker.init(frame, bbox)
    return tracker


def update_tracker(tracker, frame):
    if tracker is None:
        return None, None

    success, bbox = tracker.update(frame)
    return success, bbox


def detect_and_initialize(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        min_area = 200
        max_area = 200000
        if min_area < w * h < max_area:
            return x, y, w, h
        else:
            return None
    else:
        return None


def execute_tracking(frame, showTracking):
    tracker = cv2.TrackerCSRT_create()
    bbox = detect_and_initialize(frame)
    frame_copy = frame.copy()

    if bbox:
        tracker = initialize_tracker(tracker, frame, bbox)
    else:
        print("Não foi possível detectar uma ROI válida.")
        return frame, None

    success, bbox = update_tracker(tracker, frame)
    if success:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame_copy, p1, p2, (255, 0, 0), 2, 1)

        if showTracking:
            cv2.imshow("Tracking Line", frame_copy)
        elif cv2.getWindowProperty("Tracking Line", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Tracking Line")

        return frame_copy, bbox
    else:
        return frame, None


def calculate_center(bbox):
    if bbox is None:
        return None

    x, y, w, h = bbox
    centro_x = int(x + w / 2)
    centro_y = int(y + h / 2)
    return centro_x, centro_y
