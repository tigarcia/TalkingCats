import glob
import os

import librosa
import numpy as np
import soundfile

import matplotlib.pyplot as plt


def wavToFtr(inputFile, outputFile):
    if not os.path.exists(outputFile[0:outputFile.rfind('\\')]):
        os.makedirs(outputFile[0:outputFile.rfind('\\')])

    data = soundfile.read(inputFile)
    features = librosa.feature.melspectrogram(data[0], sr=41100, hop_length=1024)
    np.save(outputFile, features)
    # librosa.display.specshow(librosa.logamplitude(features, ref_power=np.max), y_axis='mel', fmax=8000, x_axis='time')
    # plt.show()


def convertAll(inputDir, outputDir):
    for inputFile in glob.glob(inputDir + '/**/*.wav', recursive=True):
        print(inputFile)
        outputFile = inputFile.replace(inputDir, outputDir).replace('.wav', '.npy')
        if not os.path.isfile(outputFile):
            print('Generating output file: ' + outputFile)
            try:
                wavToFtr(inputFile, outputFile)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    convertAll('wavData', 'ftrData')
