import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Erro: não foi possível acessar a câmera.")
    exit()

print("✅ Câmera aberta com sucesso. Pressione ESC para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Erro ao capturar frame.")
        break

    cv2.imshow("Teste da Câmera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
