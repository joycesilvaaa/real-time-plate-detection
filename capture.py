import cv2
from read import detectar_placa

def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return
    while True:
        ret, frame = cap.read()
        print("Lendo frame...")
        if not ret:
            break
        frame = detectar_placa(frame)
        cv2.imshow('Câmera USB', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

capture_video()
    
