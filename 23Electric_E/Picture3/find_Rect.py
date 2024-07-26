import cv2
import numpy as np

class RectDetector(object):
    """
    矩形识别器
    """
    def __init__(self) -> None:
        self.maxval = 255   #经调试，图像1在(152,255)时识别抗干扰能力最强
        self.minval = 152 
        self.min_area_threshold = 2000  # 最小面积阈值
    def createTrackbar(self):           #回调器
        cv2.namedWindow('trackbar')
        cv2.createTrackbar('maxval', 'trackbar', self.maxval, 255, self.callback_maxval)
        cv2.createTrackbar('minval', 'trackbar', self.minval, 255, self.callback_minval)

    # region 回调函数
    def callback_maxval(self, x):
        self.maxval = x

    def callback_minval(self, x):
        self.minval = x
    # endregion

    def detect(self, _img):         #矩形检测器
        lst = []
        areas = []
        img = _img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 高斯模糊
        blurred = cv2.GaussianBlur(gray, (1, 1), 0)
        # 使用Canny算子提取边缘
        edges = cv2.Canny(blurred, self.minval, self.maxval)  
        #cv2.imshow("2",edges)
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 找到边缘
        min_area = float('inf')
        min_rect_center = None
        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)  # 近似轮廓

            if len(approx) == 4 and cv2.contourArea(approx) > self.min_area_threshold:  # 如果近似后的轮廓有四个顶点，那么它可能是一个矩形
                areas.append(cv2.contourArea(approx))  # 将面积存储
                lst.append(approx)  # 将矩形存储
                cv2.drawContours(_img, [approx], -1, (0, 0, 255), 2)  # 在原始图像上画出矩形
                
                # 计算矩形的面积
                area = cv2.contourArea(approx)
                if area < min_area:
                    min_area = area
                    min_rect_center = self.get_intersection(approx[0][0], approx[2][0], approx[1][0], approx[3][0])

                # 画对角线
                cv2.line(_img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 1)  # 对角线1
                cv2.line(_img, tuple(approx[1][0]), tuple(approx[3][0]), (0, 255, 0), 1)  # 对角线2

                # 计算对角线交点
                intersection = self.get_intersection(approx[0][0], approx[2][0], approx[1][0], approx[3][0])
                cv2.circle(_img, intersection, 5, (0, 255, 255), -1)
                cv2.putText(_img, '({}, {})'.format(intersection[0], intersection[1]), 
                            (intersection[0] + 10, intersection[1]), 
                            cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 255), 1)
        
        # 按面积排序，找出第二大矩形
        if len(areas) > 1:
            sorted_indices = np.argsort(areas)
            second_largest_index = sorted_indices[-3]  #获取第二大的矩形的索引
            second_largest_rect = lst[second_largest_index]
            print("细线四角坐标：")
            for point in second_largest_rect:
                print(point[0])
        return _img, lst ,min_rect_center ,second_largest_rect
        
    def get_intersection(self, p1, p2, p3, p4):
        """计算两条对角线的交点"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denom == 0:
            return None  # 平行或重合
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
        intersection_x = int(x1 + ua * (x2 - x1))
        intersection_y = int(y1 + ua * (y2 - y1))
        return (intersection_x, intersection_y)  