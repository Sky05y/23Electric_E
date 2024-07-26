import cv2
import numpy as np

def find_red_green(m_img , test_area):
        "查找红绿点的坐标"
        img = m_img.copy()
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 创建一个与输入图像大小相同的空白掩膜
        mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)

        # 将 test_area 的四个点坐标转换为 numpy 数组
        points = np.array(test_area, dtype=np.int32)

        # 在掩膜上绘制多边形区域并填充
        cv2.fillPoly(mask, [points], 255)

        # 将掩膜应用于 HSV 图像
        roi = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

        # 定义红色和绿色的HSV颜色范围
        lower_red = np.array([130, 35, 120])
        upper_red = np.array([255, 255, 255])
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])

         # 创建红色和绿色的掩码
        mask_red = cv2.inRange(roi, lower_red, upper_red)
        mask_green = cv2.inRange(roi, lower_green, upper_green)

        # 进行形态学操作以去除噪点
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)

        # 查找红色和绿色点的轮廓
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        def find_largest_contour(contours):
            if not contours:
                return None, None
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] == 0:  # 防止分母为零
                return None, None
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return largest_contour, (cx, cy)

        p_red, p_green = -1, -1
        #cv2.imshow("2",mask_red)
        # 找到最大红色点的轮廓并绘制和获取坐标
        largest_contour_red, red_center = find_largest_contour(contours_red)
        if red_center:
            cv2.drawContours(img, [largest_contour_red], -1, (0, 0, 255), 2)
            p_red = red_center
            print("红色点坐标:{}".format(p_red))
        else:
            print("未找到红色点")


         # 找到最大绿色点的轮廓并绘制和获取坐标
        largest_contour_green, green_center = find_largest_contour(contours_green)
        if green_center:
            cv2.drawContours(img, [largest_contour_green], -1, (0, 255, 0), 2)
            p_green = green_center
            print("绿色点坐标:{}".format(p_green))
        else:
            print("未找到绿色点")
        
        return p_red,p_green   