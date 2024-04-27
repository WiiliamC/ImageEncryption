import cv2

def percent_func_gen(a, b, time, n, mode):
    """
    高次多项式计算函数生成器
    :param a: 起始百分比（如：0.25）
    :param b: 结束百分比
    :param time: 动画持续时间
    :param n: 多项式次数
    :param mode: faster（越来越快）、slower（越来越慢）
    :return: 每个时刻到达百分比的计算函数
    """
    if mode == "slower":
        a, b = b, a
    delta = abs(a - b)
    sgn = 1 if b - a > 0 else (-1 if b - a < 0 else 0)

    def percent_calc(ti):
        if mode == "slower":
            ti = time - ti
        return sgn * delta / (time ** n) * (ti ** n) + a

    return percent_calc


if __name__ == '__main__':
    '''读入图像'''
    img1 = cv2.imread(r"img\love.bmp")
    img2 = cv2.imread(r"img\love.jpg")
    rows, cols = img1.shape[:2]

    '''特效展示'''
    load_f = 20
    tim = 0.5
    percent_func1 = percent_func_gen(a=1, b=0, time=tim, n=1, mode="null")
    percent_func2 = percent_func_gen(a=0, b=1, time=tim, n=1, mode="null")
    for t in range(int(tim * 1000) // load_f + 1):
        percent = percent_func1(t * load_f / 1000)
        img_show = cv2.multiply(img1, (1, 1, 1, 1), scale=percent)
        cv2.imshow("show", img_show)
        cv2.waitKey(load_f)
    for t in range(int(tim * 1000) // load_f + 1):
        percent = percent_func2(t * load_f / 1000)
        img_show = cv2.multiply(img2, (1, 1, 1, 1), scale=percent)
        cv2.imshow("show", img_show)
        cv2.waitKey(load_f)

    '''关闭窗口'''
    cv2.waitKey(1500)
    cv2.destroyAllWindows()
