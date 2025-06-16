import cv2
from read import detectar_placa
import threading
import time
import requests 
import re

quantidade_frames = 0
frame_global = None
lock = threading.Lock()
anotacoes_ocr = []
regex_placa = re.compile(r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$')

def ocr_loop():
    global frame_global, anotacoes_ocr
    while True:
        time.sleep(1.5) 
        with lock:
            if frame_global is not None:
                frame_copy = frame_global.copy()
            else:
                continue
        try:
            resultados = detectar_placa(frame_copy, retornar_resultados=True)
            with lock:
                for (bbox, texto, confianca) in resultados:
                        if regex_placa.match(texto):
                            try:
                                requests.post("http://localhost:8000/api/inserir", data={
                                    "placa": texto,
                                    "confianca": confianca
                                })
                            except Exception as e:
                                print("Erro ao enviar para API:", e)
        except Exception as e:
            print("Erro no OCR:", e)

def desenhar_anotacoes(frame, anotacoes):
    for (bbox, texto) in anotacoes:
        if len(bbox) == 4:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, texto, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return frame

def capture_video():
    global frame_global, anotacoes_ocr
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    threading.Thread(target=ocr_loop, daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_resized = cv2.resize(frame, (640, 480))
        with lock:
            frame_global = frame_resized.copy()
            anotacoes = list(anotacoes_ocr)

        frame_marcado = desenhar_anotacoes(frame_resized.copy(), anotacoes)
        cv2.imshow("Câmera USB", frame_marcado)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

capture_video()
    
