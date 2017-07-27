#coding=utf-8
'''
Created on 2016-1-23

@author: kwsy
'''
import os
import hibiscusTools
from audioop import reverse
import sys
import csv


class Hibiscus():
    def analyseNovel(self, filename):
        if not os.path.exists(filename):
            pass
        with open(filename, 'r', encoding='gbk') as file:
            content = file.read()
        txtlist = hibiscusTools.getAllChineseCharacters(content)

        self.novelInfo = {}
        index = 0
        for txt in txtlist:
            itemlst = hibiscusTools.getLatentword(txt, index)
            index = index + len(txt)
            for item in itemlst:
                word = item['word']
                if not word in self.novelInfo:
                    self.novelInfo[word] = {
                        'leftLst': [],
                        'rightLst': [],
                        'wordindexLst': [],
                        'count': 0,
                        'word': word
                    }
                if not item['left'] == None:
                    self.novelInfo[word]['leftLst'].append(item['left'])
                if not item['right'] == None:
                    self.novelInfo[word]['rightLst'].append(item['right'])
                self.novelInfo[word]['wordindexLst'].append(item['wordindex'])
                self.novelInfo[word][
                    'count'] = self.novelInfo[word]['count'] + 1

        self.charCount = index
        self.calculte()

    def outExcel(self, filename):
        headers = ('word', 'count', 'solidification', 'freedom')
        lst = []
        for k, v in self.novelInfo.items():
            if v['count'] > 30 and len(
                    k) > 1 and v['solidification'] > 50 and v['freedom'] > 3:
                lst.append(v)

        lst = sorted(lst, key=lambda x: x['count'], reverse=True)

        with open(filename + '.csv', 'w', encoding='gbk') as f:
            f_csv = csv.DictWriter(f, headers, extrasaction='ignore')
            f_csv.writerow({
                'word': '单词',
                'count': '出现次数',
                'solidification': '凝结度',
                'freedom': '自由度'
            })
            f_csv.writerows(lst)

    def calculte(self):
        for word, info in self.novelInfo.items():
            self.novelInfo[word]['solidification'] = self.getSolidification(
                word)
            self.novelInfo[word]['freedom'] = self.getFreedom(
                self.novelInfo[word])

    def getFreedom(self, wordinfo):
        leftfreedom = hibiscusTools.calculateFreedom(wordinfo['leftLst'])
        rightfreedom = hibiscusTools.calculateFreedom(wordinfo['rightLst'])
        if leftfreedom < rightfreedom:
            return leftfreedom
        return rightfreedom

    def getSolidification(self, word):

        splitLst = hibiscusTools.splitWord(word)
        wordcount = self.novelInfo[word]['count']
        probability = float(wordcount) / float(self.charCount)
        min = 10000000
        for item in splitLst:
            left, right = item[0], item[1]
            leftcount, rightcount = self.novelInfo[left][
                'count'], self.novelInfo[right]['count']

            Togetherprobability = probability / (
                (float(rightcount) / float(self.charCount)) *
                (float(leftcount) / float(self.charCount)))
            if Togetherprobability < min:
                min = Togetherprobability
        return min


def excute(name):
    filename = sys.argv[1]
    hibi = Hibiscus()
    hibi.analyseNovel(filename)
    hibi.outExcel(filename)


if __name__ == '__main__':
    excute(sys.argv[1:])
