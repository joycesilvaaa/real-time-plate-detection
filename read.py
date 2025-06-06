import cv2
import easyocr
import csv

reader = easyocr.Reader(['pt','en'])

def detectar_placa(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray)
    for (bbox, texto, confianca) in results: 
        if len(texto) >= 6 and any(char.isdigit() for char in texto):
            print(f"Possível placa: {texto} - Confiança: {confianca:.2f}")
            salvar_placa(texto)
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 2)
            cv2.putText(frame, texto, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    return frame
            

def salvar_placa(texto):
    with open('placas_detectadas.csv', mode="a", newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow([texto])