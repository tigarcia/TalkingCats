import contextlib
import glob
import json
import os
import wave


def getDuration(fname):
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


if __name__ == '__main__':
    vocab = dict()
    with open('C:/Dev/Temp/lsdc-train.jsonl', 'wb') as f:
        for sound in glob.glob('C:/Dev/MathData/NROC_Questions_NoDuplicates_wav/*.wav'):
            print(sound)
            txtfile = sound[sound.rfind('\\') + 1:sound.find('_', sound.rfind('\\'))]
            if not os.path.isfile('C:/Dev/MathData/NROC_Questions_NoDuplicates_xml/' + txtfile + '.xml'):
                continue
            with open('C:/Dev/MathData/NROC_Questions_NoDuplicates_xml/' + txtfile + '.xml', 'r') as f2:
                annotation = f2.read()
            annotation = annotation.lower().replace('"', '').replace('\n', '').replace(' ', '').replace('\\', '\\\\')
            if 'apply' in annotation:
                continue
            item_list = []
            while annotation:
                if annotation.startswith('<mo>'):
                    item_list.append(annotation[:annotation.find('</mo>') + 5])
                    annotation = annotation[annotation.find('</mo>') + 5:]
                elif annotation.startswith('<'):
                    item_list.append(annotation[:annotation.find('>') + 1])
                    annotation = annotation[annotation.find('>') + 1:]
                else:
                    item_list.append(annotation[:1])
                    annotation = annotation[1:]
            if item_list[0]=='<mrow>':
                item_list = item_list[1:-1]
            for i in item_list:
                if i not in vocab:
                    vocab[i] = 0
                vocab[i] += 1
            f.write(('{"text": ' + json.dumps(item_list) + ', "duration_s": ' + str(
                getDuration(sound)) + ', "uuid": "' + sound[sound.rfind('\\') + 1:-4] + '"}\n').encode('utf-8'))

    vocablist = list(vocab.keys())
    vocablist.sort()
    with open('C:/dev/Temp/vocab.json', 'w') as f:
        f.write(json.dumps(vocablist))

    with open('C:/dev/Temp/lsdc-test.jsonl', 'wb') as f:
        for sound in glob.glob('C:/dev/Temp/audio/*.wav'):
            print(sound)
            txtfile = sound[sound.rfind('\\') + 1:sound.find('_', sound.rfind('\\'))]
            if not os.path.isfile('C:/Dev/MathData/col10614_1.3_MathML_NoDuplicates_xml/' + txtfile + '.xml'):
                continue
            with open('C:/Dev/MathData/col10614_1.3_MathML_NoDuplicates_xml/' + txtfile + '.xml', 'r') as f2:
                annotation = f2.read()
            annotation = annotation.lower().replace('"', '').replace('\n', '').replace(' ', '').replace('\\', '\\\\')
            if 'apply' in annotation:
                continue
            item_list = []
            while annotation:
                if annotation.startswith('<mo>'):
                    item_list.append(annotation[:annotation.find('</mo>') + 5])
                    annotation = annotation[annotation.find('</mo>') + 5:]
                elif annotation.startswith('<'):
                    item_list.append(annotation[:annotation.find('>') + 1])
                    annotation = annotation[annotation.find('>') + 1:]
                else:
                    item_list.append(annotation[:1])
                    annotation = annotation[1:]
            if item_list[0]=='<mrow>':
                item_list = item_list[1:-1]
            f.write(('{"text": ' + json.dumps(item_list) + ', "duration_s": ' + str(
                getDuration(sound)) + ', "uuid": "' + sound[sound.rfind('\\') + 1:-4] + '"}\n').encode('utf-8'))
    print(vocab)
