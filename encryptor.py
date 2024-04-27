# -*- coding:gbk -*-
import numpy as np
import cv2


def encrypt_image_by_key(image, key):
    """按照密匙对图像进行加密

    Args:
        image (str or ndarray): 图片矩阵或路径
        key (str): 密匙

    Returns:
        ndarray: 加密后的图像
    """
    if isinstance(image, str):
        image = cv2.imread(image)
    assert isinstance(image, np.ndarray)
    x0 = gene_x0(key)
    return encrypt(image, x0, 3.999)


def gene_x0(key):
    """按照密匙生成混沌序列的初值

    Args:
        key (str): 密匙

    Returns:
        int: 混沌序列的初值
    """
    x0 = 0
    for i, c in enumerate(key):
        x0 += (i+1)*ord(c)
    while(x0 > 1):
        x0 /= 10
    return x0


def gene_logistic_list(x0, u, l):
    """生成混沌序列

    Args:
        x0 (float): 初值，0 < x0 < 1
        u (float): 系数，3.57 < u < 4
        l (int): 长度

    Returns:
        list: 混沌序列
    """
    assert 0 < x0 < 1 and 3.57 < u < 4 and isinstance(l, int)
    logistic_list = []
    for i in range(l):
        logistic_list.append(x0)
        x0 = u*x0*(1-x0)
    return logistic_list


def encrypt(image, x0, u):
    """使用混沌序列对图像加密，混沌序列：x(k+1)= u*x(k)*(1-x(k))

    Args:
        x0 (float): 初值，0 < x0 < 1
        u (float): 系数，3.57 < u < 4
    Returns:
        ndarray: 加密后的图像
    """
    logistic_list = gene_logistic_list(
        x0, u, image.shape[0]*image.shape[1]*3)
    logistic_image = np.array(logistic_list)
    logistic_image = np.uint8(logistic_image*256)
    logistic_image = np.reshape(logistic_image, image.shape)
    return cv2.bitwise_xor(image, logistic_image)


def decrypt(image, x0, u):
    """使用混沌序列对图像解密，混沌序列：x(k+1)= u*x(k)*(1-x(k))

    Args:
        x0 (float): 初值，0 < x0 < 1
        u (float): 系数，3.57 < u < 4
    Returns:
        ndarray: 解密后的图像
    """
    return encrypt(image, x0, u)


if __name__ == "__main__":
    x0 = gene_x0("我爱你")
    print("x0 =", x0)
    source_image = cv2.imread(r"img\girl.jpg")
    cv2.imshow("source image", source_image)

    encoded_image = encrypt(source_image, x0, 3.999)
    cv2.imshow("encoded image", encoded_image)

    decoded_image = decrypt(encoded_image, x0, 3.999)
    cv2.imshow("decoded image", decoded_image)

    cv2.waitKey(0)
