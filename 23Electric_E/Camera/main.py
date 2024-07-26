import cv2
import numpy as np
import find_circle
import find_Rect

def resize_picture(img_display , percent):
    # 获取图片的宽度和高度
        original_height, original_width = img_display.shape[:2]
        # 设定缩放比例，例如缩小到原来的50%
        scale_percent = percent
        new_width = int(original_width * scale_percent / 100)
        new_height = int(original_height * scale_percent / 100)
        dim = (new_width, new_height)
        # 缩放图片
        img_display = cv2.resize(img_display, dim, interpolation=cv2.INTER_AREA)
        return img_display

if __name__ == '__main__':
    detector = find_Rect.RectDetector()
    #detector.createTrackbar()  # 创建Trackbar
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        _img = frame.copy()
        img, p_lst ,min_center,Location_Rect = detector.detect(frame)
        try:
            if Location_Rect != -1:
                p_red,p_green = find_circle.find_red_green(_img,Location_Rect)

                if p_red != -1:
                    cv2.circle(img, p_red, 5, (0, 0, 255), -1)
                    cv2.putText(img, f"Red: {p_red}", (p_red[0] + 10, p_red[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                if p_green != -1:
                    cv2.circle(img, p_green, 5, (0, 255, 0), -1)
                    cv2.putText(img, f"Green: {p_green}", (p_green[0] + 10, p_green[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        except:
            continue
        print("矩形中心点坐标:", min_center)
        cv2.waitKey(10)

        img_display = img.copy()  
        for rect in p_lst:
            for i in range(4):
                x, y = rect[i][0]
                cv2.putText(img_display, '({}, {})'.format(x, y), 
                            (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
        img_display = resize_picture(img_display , 100) #设定缩放比例，默认缩小为原来的50%
        cv2.imshow('img', img_display)
        
        key = cv2.waitKey(1)
        # 按空格键退出
        if key == ord(' '):
            cap.release()
            cv2.destroyAllWindows()
            break
