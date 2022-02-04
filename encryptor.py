# -*- coding:gbk -*-
import numpy as np
import cv2


def encrypt_image_by_key(image, key):
    """�����ܳ׶�ͼ����м���

    Args:
        image (str or ndarray): ͼƬ�����·��
        key (str): �ܳ�

    Returns:
        ndarray: ���ܺ��ͼ��
    """
    if isinstance(image, str):
        image = cv2.imread(image)
    assert isinstance(image, np.ndarray)
    x0 = gene_x0(key)
    return encrypt(image, x0, 3.999)


def gene_x0(key):
    """�����ܳ����ɻ������еĳ�ֵ

    Args:
        key (str): �ܳ�

    Returns:
        int: �������еĳ�ֵ
    """
    x0 = 0
    for i, c in enumerate(key):
        x0 += (i+1)*ord(c)
    while(x0 > 1):
        x0 /= 10
    return x0


def gene_logistic_list(x0, u, l):
    """���ɻ�������

    Args:
        x0 (float): ��ֵ��0 < x0 < 1
        u (float): ϵ����3.57 < u < 4
        l (int): ����

    Returns:
        list: ��������
    """
    assert 0 < x0 < 1 and 3.57 < u < 4 and isinstance(l, int)
    logistic_list = []
    for i in range(l):
        logistic_list.append(x0)
        x0 = u*x0*(1-x0)
    return logistic_list


def encrypt(image, x0, u):
    """ʹ�û������ж�ͼ����ܣ��������У�x(k+1)= u*x(k)*(1-x(k))

    Args:
        x0 (float): ��ֵ��0 < x0 < 1
        u (float): ϵ����3.57 < u < 4
    Returns:
        ndarray: ���ܺ��ͼ��
    """
    logistic_list = gene_logistic_list(
        x0, u, image.shape[0]*image.shape[1]*3)
    logistic_image = np.array(logistic_list)
    logistic_image = np.uint8(logistic_image*256)
    logistic_image = np.reshape(logistic_image, image.shape)
    return cv2.bitwise_xor(image, logistic_image)


def decrypt(image, x0, u):
    """ʹ�û������ж�ͼ����ܣ��������У�x(k+1)= u*x(k)*(1-x(k))

    Args:
        x0 (float): ��ֵ��0 < x0 < 1
        u (float): ϵ����3.57 < u < 4
    Returns:
        ndarray: ���ܺ��ͼ��
    """
    return encrypt(image, x0, u)


if __name__ == "__main__":
    x0 = gene_x0("�Ұ���")
    print("x0 =", x0)
    source_image = cv2.imread(r"img\girl.jpg")
    cv2.imshow("source image", source_image)

    encoded_image = encrypt(source_image, x0, 3.999)
    cv2.imshow("encoded image", encoded_image)

    decoded_image = decrypt(encoded_image, x0, 3.999)
    cv2.imshow("decoded image", decoded_image)

    cv2.waitKey(0)
