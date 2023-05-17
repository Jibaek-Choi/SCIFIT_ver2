import cv2


class CamProcess:

    def __init__(self, capture, direction):
        self.capture = cv2.VideoCapture(0)
        """
        화면 방향 전환
        0 - 정상
        1 - 90도 회전
        2 - 180도 회전
        3 - 270도 회전
        """
        self.direction_flag = 0

        if self.direction_flag == 0:
            pass
        elif self.direction_flag == 1:
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        elif self.direction_flag == 2:
            self.image = cv2.rotate(self.image, cv2.ROTATE_180)
        elif self.direction_flag == 3:
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)