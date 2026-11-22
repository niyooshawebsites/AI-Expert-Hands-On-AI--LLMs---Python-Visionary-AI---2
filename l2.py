import cv2
import numpy as np

def apply_filters(image, ftype):
    """Apply a filter to the image based on the filter type"""
    img = image.copy()

    # img[height, width, color_channel]
    # img[:, :, 0]  # Blue channel
    # img[:, :, 1]  # Green channel
    # img[:, :, 2]  # Red channel

    if ftype == 'red_tint':
        # BGR
        # turning the blue(0) and green(1) channels to 0. Keeping only the Red(2) channel
        img[:,:, 1] = img[:,:,0] = 0
    elif ftype == 'blue_tint':
        img[:,:, 1] = img[:,:,2] = 0
    elif ftype == 'green_tint':
        img[:,:,0] = img[:,:,2] = 0
    elif ftype == 'sobel':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = 3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize = 3)
        sob = cv2.bitwise_or(sx.astype('uint8'), sy.astype('uint8'))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)
    elif ftype == 'canny':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, (100, 200))
        img = cv2.cvColor(can, cv2.COLOR_GRAY2BGR)
    elif ftype == 'cartoon':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)

    return img

def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print('Error: Camera is not assessible!')
        exit()

    ftype = 'original'
    print("Keys: r=Red, g=Green, b=Blue, s=Sobel, c=Canny, t=Cartoon, q=quit")

    while True:
        success, frame = camera.read()

        if not success:
            print('Can not capture video')
            exit()

        frame = cv2.flip(frame, 1)
        out = apply_filters(frame, ftype)
        cv2.imshow("Filter", out)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            ftype = 'red_tint'
        elif key == ord('b'):
            ftype = 'blue_tint'
        elif key == ord('g'):
            ftype = 'green_tint'
        elif key == ord('s'):
            ftype = 'sobel'
        elif key == ord('c'):
            ftype = 'canny'
        elif key == ord('t'):
            ftype = 'cartoon'
        elif key == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()