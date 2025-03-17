import cv2 as cv
import time

def apply_filters(frame, contrast=1.0, brightness=0, flip=False):
    contrast = max(0.5, min(3.0, contrast))  # 대비 범위: 0.5 ~ 3.0
    brightness = max(-100, min(100, brightness))  # 밝기 범위: -100 ~ 100
    frame = cv.convertScaleAbs(frame, alpha=contrast, beta=brightness)
    
    if flip:
        frame = cv.flip(frame, 1)

    return frame

def video_recorder(camera_source=0, output_file="output.avi"):
    video = cv.VideoCapture(camera_source)
    
    if not video.isOpened():
        print("에러: 카메라를 열 수 없습니다.")
        return

    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv.CAP_PROP_FPS)) or 20  # 기본 20 FPS

    if frame_width == 0 or frame_height == 0:
        print("에러: 프레임 사이즈 검색에 실패했습니다.")
        video.release()
        return

    fourcc = cv.VideoWriter_fourcc(*'MJPG')  
    out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    is_recording = False
    contrast = 1.0
    brightness = 0
    flip = False

    print("Space로 녹화 시작/중지, ESC로 종료.")
    print("C/V 로 Contrast +/-, B/N 으로 Brightness +/-, F로 Flip.")

    timeout_limit = 30
    last_frame_time = time.time()

    while True:
        ret, frame = video.read()
        
        if not ret:
            print("Warning: Frame read failed. Checking timeout...")
            if time.time() - last_frame_time > timeout_limit:
                print("Error: RTSP stream timeout. Exiting...")
                break
            continue

        last_frame_time = time.time()  

        frame = apply_filters(frame, contrast, brightness, flip)

        if is_recording:
            out.write(frame)
            cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)  

        cv.imshow('Camera Feed', frame)

        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 32:  
            is_recording = not is_recording
        elif key == ord('c'): 
            contrast += 0.1
        elif key == ord('v'): 
            contrast -= 0.1
        elif key == ord('b'): 
            brightness += 5
        elif key == ord('n'):
            brightness -= 5
        elif key == ord('f'):
            flip = not flip

    video.release()
    out.release()
    cv.destroyAllWindows()
    print("비디오 녹화 종료.")

video_recorder("rtmp://210.99.70.120/live/cctv001.stream")