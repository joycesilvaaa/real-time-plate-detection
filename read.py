import cv2
import easyocr
import re

reader = easyocr.Reader(['pt','en'], gpu=False)

regex_placa = re.compile(r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$')

def detectar_placa(frame, retornar_resultados=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray)
    anotacoes = []

    for (bbox, texto, confianca) in results:
        texto_limpo = texto.upper().replace(" ", "").replace("-", "")
        if len(texto_limpo) >= 6 and any(char.isdigit() for char in texto_limpo):
            if regex_placa.match(texto_limpo):
                print(f"✅ Possível placa: {texto_limpo} - Confiança: {confianca:.2f}")
                anotacoes.append((bbox, texto_limpo, confianca))
            else:
                print(f"🔶 Texto não corresponde à placa: {texto_limpo}")
        else:
            print(f"🔸 Ignorado: {texto}")
    return anotacoes if retornar_resultados else frame