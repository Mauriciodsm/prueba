import av
import cv2
container = av.open('rtsp://admin:Camara1202@192.168.0.101:554/Streaming/Channels/101')

for frame in container.decode(video=0):
    img = frame.to_image()  # Convertir frame a imagen (PIL)
    
    # Procesar 'img' con OpenCV para realizar inferencias con YOLOv8, por ejemplo
    # faces = tu_funcion_deteccion_yolov8(img)
    
    # Mostrar la imagen procesada
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break