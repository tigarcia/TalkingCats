import glob
import os

from comtypes.client import CreateObject


def txtToWav(inputFile, outputFile, voice=0):
    if not os.path.exists(outputFile[0:outputFile.rfind('\\')]):
        os.makedirs(outputFile[0:outputFile.rfind('\\')])

    engine = CreateObject("SAPI.SpVoice")
    engine.Voice = engine.GetVoices()[voice]
    stream = CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib

    stream.Open(outputFile, SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream = stream

    f = open(inputFile, 'r')
    text = f.read()
    f.close()

    engine.speak(text)
    stream.Close()


def convertAll(inputDir, outputDir):
    engine = CreateObject("SAPI.SpVoice")
    for i in range(len(engine.GetVoices())):

        for inputFile in glob.glob(inputDir + '/**/*.txt', recursive=True):
            print(inputFile)
            outputFile = inputFile.replace(inputDir, outputDir).replace('.txt', '') \
                         + '_voice' + str(i) + '.wav'
            if not os.path.isfile(outputFile):
                try:
                    txtToWav(inputFile, outputFile, i)
                except:
                    pass


if __name__ == '__main__':
    convertAll('txtData', 'wavData')
