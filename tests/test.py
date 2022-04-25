import os
import subprocess
import numpy as np
import shutil
import sys
import cv2
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
    outputs = sorted([f for f in os.listdir(outputs_p) if 'output' in f], key=lambda x: x.split('_')[1].split('.jpg')[0])
    size_of_test = len([a for a in os.listdir(inputs_p) if 'mask' in a])
    assert(len(inputs)==len(masks)==len(outputs))

    # Iterate over different inputs
    distances = []
    for i in tqdm(np.random.permutation(size_of_test)):

        # arguments
        input = os.path.join(inputs_p,inputs[i])
        mask = os.path.join(inputs_p,masks[i])
        output = os.path.join(outputs_p,outputs[i])
        output_test = os.path.join(outputs_test_p,inputs[i].replace('input','output'))
        z = str(np.random.randint(1,6)/2)
        epsilon = str(np.random.random()/1000)
        connectivity = bool(np.random.randint(0,2))

        # module call
        cmd = [
                  sys.executable, main,
                            '--input_path', input,\
                            '--mask_path', mask,\
                            '--output_path', output_test,\
                            '--z', z,\
                            '--epsilon', epsilon
                ] + \
              ([
                            '--is_8_connectivity'
                ] if connectivity else [])
        subprocess.run(cmd)
        # Reading and plotting images
        output_test_im = cv2.imread(output_test)
        output_im = cv2.imread(output)
        im = np.concatenate([output_test_im, output_im], axis=1)
        plt.imshow(im)
        distances.append((((output_test_im-output_im)**2).sum()**0.5)/output_im.size)
        print(' L2 distance: ',distances[-1])
    print('Total error :',np.mean(distances),'std: ',np.std(distances))
    # removing recirsevly the 'output_test' folder
    shutil.rmtree(outputs_test_p)