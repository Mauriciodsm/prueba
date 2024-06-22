import cv2
import ffmpeg
import numpy as np 


input_stream = 'rtsp://tu_url_de_rtsp'
probe = ffmpeg.probe(input_stream)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

process = (
    ffmpeg
    .input(input_stream)
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
    .run_async(pipe_stdout=True)
)

while True:
    in_bytes = process.stdout.read(video_info['height'] * video_info['width'] * 3)
    if not in_bytes:
        break
    frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([video_info['height'], video_info['width'], 3])
    )

    # Procesar 'frame' con OpenCV para inferencias con YOLOv8, etc.

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()