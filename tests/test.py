import os
import subprocess
import numpy as np
import shutil
import sys
import cv2
from time import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tqdm import tqdm
if __name__ == '__main__':
    inputs_p = os.path.join(os.path.dirname(os.getcwd()),r'./tests/input/')
    outputs_p = os.path.join(os.path.dirname(os.getcwd()),r'./tests/output/')
    outputs_test_p = os.path.join(os.path.dirname(os.getcwd()),r'./tests/output_test/')
    main = os.path.join(os.path.dirname(os.getcwd()),r'./main.py')
    # Create outputs test empty
    os.path.exists(outputs_test_p) or os.makedirs(outputs_test_p)

    # Prepare the various arguments for the test
    inputs = sorted([f for f in os.listdir(inputs_p) if 'input' in f], key=lambda x: x.split('_')[1].split('.jpg')[0])
    masks = sorted([f for f in os.listdir(inputs_p) if 'mask' in f], key=lambda x: x.split('_')[1].split('.jpg')[0])
    size_of_test = len([a for a in os.listdir(inputs_p) if 'mask' in a])
    assert(len(inputs)==len(masks))
    times_1 = []
    times_2 = []
    # Iterate over different inputs
    distances1 = []
    distances2 = []
    for i in tqdm(np.random.permutation(min(size_of_test,10))):

        # arguments
        input = os.path.join(inputs_p,inputs[i])
        mask = os.path.join(inputs_p,masks[i])
        output_test = os.path.join(outputs_test_p,inputs[i].replace('input','output'))
        z = str(np.random.randint(1,6)/2)
        epsilon = str(np.random.random()/1000)
        connectivity = bool(np.random.randint(0,2))

        # module call
        input_im = cv2.imread(input)
        cmd = [
                  sys.executable, main,
                            '--input_path', input,\
                            '--mask_path', mask,\
                            '--output_path', output_test,\
                            '--z', z,\
                            '--epsilon', epsilon
                ] + \
              (['--is_8_connectivity'] if connectivity else [])
        result1 = subprocess.run(cmd,capture_output=True, text=True).stdout
        times_1.append(float(result1))

        # Reading and plotting images
        output_test_im_1 = cv2.imread(output_test)
        # im = np.concatenate([output_test_im, input_im], axis=1)
        # plt.imshow(im)
        # plt.show()
        distances1.append((((output_test_im_1-input_im)**2).sum()**0.5)/input_im.size)
        print(' mse error (classic): ', distances1[-1])

        result2 = subprocess.run(cmd+['--KNN'], capture_output=True, text=True).stdout
        times_2.append(float(result2))

        # Reading and plotting images
        output_test_im_2 = cv2.imread(output_test)
        distances2.append((((output_test_im_2-input_im)**2).sum()**0.5)/input_im.size)
        # im = np.concatenate([output_test_im, input_im], axis=1)
        # plt.imshow(im)
        # plt.show()
        print(' mse error (KNN): ', distances2[-1])
    print('Total error :',np.mean(distances1),'std: ',np.std(distances1))
    print('Total error :',np.mean(distances2),'std: ',np.std(distances2))
    plt.figure(1)
    plt.plot(times_1,label='classic')
    plt.plot(times_2,label='KNN')
    plt.legend()
    plt.show()
    plt.figure(2)
    plt.plot(distances1,label='classic')
    plt.plot(distances2,label='KNN')
    plt.legend()
    plt.show()
    print('The results might be found in "./tests/output_tests directory')
    # removing recirsevly the 'output_test' folder
    # shutil.rmtree(outputs_test_p)