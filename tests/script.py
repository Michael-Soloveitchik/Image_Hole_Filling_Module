import numpy as np
import cv2
import os
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
pp=r'/mnt/c/Users/Michael Soloveitchik/PycharmProjects/Job/tests/input - Copy/'
p=r'/mnt/c/Users/Michael Soloveitchik/PycharmProjects/Job/tests/input/'
o=r'/mnt/c/Users/Michael Soloveitchik/PycharmProjects/Job/tests/output/'
masks=r'/mnt/c/Users/Michael Soloveitchik/PycharmProjects/Job/tests/masks/'
i = 0
for f in os.listdir(p):
    im = os.rename(os.path.join(p, f), os.path.join(p, f'image_{i}.jpg'))
    i+=1

j = 0
for f in os.listdir(pp):
    im = cv2.imread(os.path.join(pp, f))
    for m in os.listdir(masks):
        h, w, _ = im.shape
        r1, r2 = np.random.random(2)
        dh = h / 3 * r1
        dw = w / 3 * r2
        im_new = im[int(dh // 2):h - int(dh // 2), int(dw // 2):w - int(dw // 2)]
        h, w, _ = im_new.shape
        ma =cv2.imread(os.path.join(masks, m))
        h_m,w_m,_ = ma.shape
        d = 1.
        ma_resized = cv2.resize(ma, (int(h_m//d),int(w_m//d)), interpolation = cv2.INTER_LINEAR_EXACT)
        ma_resized[(0 <ma_resized) & (ma_resized < 230.)]=0.
        ma_resized[(230 <ma_resized) & (ma_resized < 255.)]=255.
        h_m, w_m, _ = ma_resized.shape
        h_r, w_r = h-h_m//2-4, w-w_m//2-4
        c_y, c_x = np.random.randint([h_m//2+2, w_m//2+2], [h_r, w_r], (2))
        im_mask = im_new * 0. + 255.
        im_mask[c_y-int(h_m//2):c_y+int(h_m-(h_m//2)),c_x-int(w_m//2):c_x+int(w_m-(w_m//2))] = ma_resized
        cv2.imwrite(os.path.join(p, f'mask_{j}.png'), cv2.cvtColor(im_mask.astype('uint8'), cv2.COLOR_RGB2GRAY))
        cv2.imwrite(os.path.join(p, f'input_{j}.png'), cv2.cvtColor(im_new.astype('uint8'), cv2.COLOR_RGB2GRAY))
        cv2.imwrite(os.path.join(o, f'output_{j}.png'), cv2.cvtColor(im_new.astype('uint8'), cv2.COLOR_RGB2GRAY))
        j+=1
