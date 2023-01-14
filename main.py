import cv2
import sys
from streamlit import cli as stcli
import streamlit as st
import numpy as np
from PIL import Image


def cartoonization(img, cartoon):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if cartoon == "铅笔素描":
        value = st.sidebar.slider('调整草图的亮度（值越高，草图越亮）',
                                  0.0, 300.0, 250.0)
        kernel = st.sidebar.slider(
            '调整草图边缘的粗体（值越高，边缘越粗）', 1, 99, 25,
            step=2)

        gray_blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)

        cartoon = cv2.divide(gray, gray_blur, scale=value)

    if cartoon == "细节增强":
        smooth = st.sidebar.slider(
            '调整图像的平滑度级别（值越高，图像越平滑）', 3, 99, 5, step=2)
        kernel = st.sidebar.slider('调整图像的清晰度（值越低，越清晰）', 1, 21, 3,
                                   step=2)
        edge_preserve = st.sidebar.slider(
            '调整颜色平均效果（低：仅平滑相似的颜色，高：平滑不同的颜色）',
            0.0, 1.0, 0.5)

        gray = cv2.medianBlur(gray, kernel)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        color = cv2.detailEnhance(img, sigma_s=smooth, sigma_r=edge_preserve)
        cartoon = cv2.bitwise_and(color, color, mask=edges)

    if cartoon == "铅笔边缘":
        kernel = st.sidebar.slider('调整草图的清晰度（值越低，越锐利）', 1, 99,
                                   25, step=2)
        laplacian_filter = st.sidebar.slider(
            '调整边缘检测功率（值越高，功能越强大）', 3, 9, 3, step=2)
        noise_reduction = st.sidebar.slider(
            '调整草图的噪点效果（值越高，噪声越大）', 10, 255, 150)

        gray = cv2.medianBlur(gray, kernel)
        edges = cv2.Laplacian(gray, -1, ksize=laplacian_filter)

        edges_inv = 255 - edges

        dummy, cartoon = cv2.threshold(edges_inv, noise_reduction, 255, cv2.THRESH_BINARY)


    #这里有问题 删除
    # if cartoon == "Bilateral Filter":
    #     smooth = st.sidebar.slider(
    #         'Tune the smoothness level of the image (the higher the value, the smoother the image)', 3, 99, 5, step=2)
    #     kernel = st.sidebar.slider('Tune the sharpness of the image (the lower the value, the sharper it is)', 1, 21, 3,
    #                                step=2)
    #     edge_preserve = st.sidebar.slider(
    #         'Tune the color averaging effects (low: only similar colors will be smoothed, high: dissimilar color will be smoothed)',
    #         1, 100, 50)
    #
    #     gray = cv2.medianBlur(gray, kernel)
    #     edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #                                   cv2.THRESH_BINARY, 9, 9)
    #
    #     color = cv2.bilateralFilter(img, smooth, edge_preserve, smooth)
    #     cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


###############################################################################
def main():
    st.write("""
              # 将你的图像卡通化!

              """
             )

    file = st.sidebar.file_uploader("请从本地上传一张图片", type=["jpg", "png"])

    if file is None:
        st.text("你还没有上传图片")
    else:
        image = Image.open(file)
        img = np.array(image)

        option = st.sidebar.selectbox(
            '你想使用哪种卡通滤镜',
            ('铅笔素描', '细节增强', '铅笔边缘'))

        st.text("你的原始图片")
        st.image(image, use_column_width=True)

        st.text("你的卡通化图片")
        cartoon = cartoonization(img, option)

        st.image(cartoon, use_column_width=True)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())