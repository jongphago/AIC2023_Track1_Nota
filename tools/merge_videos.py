import cv2
import numpy as np

# 비디오 파일 경로
video_files = [
    "/Users/my/Documents/Project/opencv/sample/mapS001_rescaled.mp4",
    "/Users/my/Documents/Project/opencv/sample/S001c001.mp4",
    "/Users/my/Documents/Project/opencv/sample/S001c002.mp4",
    "/Users/my/Documents/Project/opencv/sample/S001c003.mp4",
    "/Users/my/Documents/Project/opencv/sample/S001c006.mp4",
    "/Users/my/Documents/Project/opencv/sample/S001c007.mp4",
]

# VideoCapture 객체를 생성합니다.
caps = [cv2.VideoCapture(file) for file in video_files]

# 모든 비디오의 첫 프레임을 읽어서 비디오의 해상도를 결정합니다.
frames = [cap.read()[1] for cap in caps]
height, width, _ = frames[0].shape

# 결과 비디오의 해상도를 결정합니다. (2x3 그리드)
out_height = height * 2
out_width = width * 3

# 출력 비디오 설정
fps = caps[-1].get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*"avc1")
out = cv2.VideoWriter("aihub_output.mp4", fourcc, fps, (out_width, out_height))

while True:
    # 각 비디오로부터 프레임을 읽습니다.
    rets, frames = zip(*[cap.read() for cap in caps])

    # 모든 비디오에서 프레임을 성공적으로 읽었는지 확인합니다.
    if not all(rets):
        break

    # 2x3 그리드로 프레임들을 합칩니다.
    grid = np.zeros((out_height, out_width, 3), dtype=np.uint8)
    grid[:height, :width] = frames[0]
    grid[:height, width : width * 2] = frames[1]
    grid[:height, width * 2 :] = frames[2]
    grid[height:, :width] = frames[3]
    grid[height:, width : width * 2] = frames[4]
    grid[height:, width * 2 :] = frames[5]

    # 결과 그리드 프레임을 출력 비디오에 작성합니다.
    out.write(grid)

# 모든 자원을 해제합니다.
out.release()
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
