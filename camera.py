import cv2


def show_webcam(mirror=False):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Webcam Life2Coding', cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, frame = cap.read()

        if mirror:
            frame = cv2.flip(frame, 1)

        cv2.imshow('Webcam Life2Coding', frame)

        if cv2.waitKey(1) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()
