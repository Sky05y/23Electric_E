import cv2

class RectDetector(object):
    """
    矩形识别器
    """
    def __init__(self) -> None:
        self.maxval = 255
        self.minval = 0

    def createTrackbar(self):
        cv2.namedWindow('trackbar')
        cv2.createTrackbar('maxval', 'trackbar', self.maxval, 255, self.callback_maxval)
        cv2.createTrackbar('minval', 'trackbar', self.minval, 255, self.callback_minval)

    # region 回调函数
    def callback_maxval(self, x):
        self.maxval = x

    def callback_minval(self, x):
        self.minval = x
    # endregion
        
    def detect(self, _img):
        lst = []
        img = _img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, self.minval, self.maxval)  # 使用Canny算子提取边缘

        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 找到边缘

        for cnt in contours:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)  # 近似轮廓

            if len(approx) == 4:  # 如果近似后的轮廓有四个顶点，那么它可能是一个矩形
                lst.append(approx)
                cv2.drawContours(_img, [approx], -1, (0, 255, 0), 2)  # 在原始图像上画出矩形
        return _img, lst

        
if __name__ == '__main__':
    # img = cv2.imread('1.jpg')
    detector = RectDetector()
    # detector.createTrackbar()
    img = cv2.imread('1.jpg')
    img, p_lst = detector.detect(img)
    print(p_lst)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()        
            break
