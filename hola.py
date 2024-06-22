import cv2
import time

# Reemplaza 'rtsp://username:password@ip_address:port/path' con tu URL RTSP
rtsp_url = 'rtsp://admin:Camara1202@192.168.0.101:554/Streaming/Channels/101'

def open_rtsp_stream(url):
    print("Intentando abrir el stream RTSP...")
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error al abrir el stream RTSP")
    else:
        print("Stream RTSP abierto exitosamente")
    return cap

def close_rtsp_stream(cap):
    if cap is not None and cap.isOpened():
        cap.release()

cap = open_rtsp_stream(rtsp_url)
frame_count = 0
max_retries = 5
retries = 0
retry_delay = 0.1  # Tiempo de espera entre reintentos en segundos
show_frame_interval = 2  # Mostrar cada N frames

try:
    while True:
        ret, frame = cap.read()
        frame_count += 1

        if not ret:
            print(f"Error al recibir el frame del stream en el frame {frame_count}")
            retries += 1
            if retries > max_retries:
                print("Máximo número de reintentos alcanzado, saliendo...")
                break
            else:
                print(f"Reintentando abrir el stream (intento {retries}/{max_retries})...")
                close_rtsp_stream(cap)
                time.sleep(retry_delay)  # Espera antes de intentar reabrir el stream
                cap = open_rtsp_stream(rtsp_url)
                continue

        retries = 0  # Resetear el contador de reintentos después de un frame exitoso

        # Mostrar el frame en una ventana cada cierto intervalo de frames
        if frame_count % show_frame_interval == 0:
            cv2.imshow('RTSP Stream', frame)
            print(f"Mostrando frame {frame_count}")

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Saliendo...")
            break

except KeyboardInterrupt:
    print("Interrupción por teclado recibida, saliendo...")

except cv2.error as e:
    print(f"Error de OpenCV: {e}")

except Exception as e:
    print(f"Error inesperado: {str(e)}")

finally:
    # Asegurarse de liberar el video y cerrar las ventanas
    close_rtsp_stream(cap)
    cv2.destroyAllWindows()
    print("Recursos liberados y ventanas cerradas")
