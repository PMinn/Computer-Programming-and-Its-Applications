# coding=utf-8


def toCountTotal(data, column):
    labels = [schoolName for schoolName in data]
    barData = {}
    for i in range(len(column)):
        attribute = column[i]
        barData[attribute] = [sum([int(data[schoolName]['肇因'][index][attribute]) for index in data[schoolName]['肇因']]) for schoolName in data]
    return barData, labels


def toCauseData(data):
    sumCause = {}
    for schoolName in data:
        for index in data[schoolName]['肇因']:
            if data[schoolName]['肇因'][index]['肇事原因'] not in sumCause:
                sumCause[data[schoolName]['肇因'][index]['肇事原因']] = int(data[schoolName]['肇因'][index]['件數'])
            else:
                sumCause[data[schoolName]['肇因'][index]['肇事原因']] += int(data[schoolName]['肇因'][index]['件數'])
    topFiveCause = sorted(sumCause.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [cause[0] for cause in topFiveCause]
    causeData = {}
    for schoolName in data:
        causeData[schoolName] = []
        for cause in topFiveCause:
            indexes = [index for index in data[schoolName]['肇因'] if data[schoolName]['肇因'][index]['肇事原因']==cause[0]]
            if len(indexes) == 0:
                causeData[schoolName].append(0)
            else:
                causeData[schoolName].append(int(data[schoolName]['肇因'][indexes[0]]['件數']))
    return causeData, labels


def toAgeData(data):
    unknown = 0
    labels = ['18歲以下', '18歲-24歲', '25歲-44歲', '45歲-65歲', '65歲以上', '不明']
    ageRange = [[0, 17], [18, 24], [25, 44], [45, 65], [66, 100]]
    sumAgeData = {}
    for schoolName in data:
        sumAgeData[schoolName] = [0 for i in range(len(ageRange))]
        for index in data[schoolName]['年齡']:
            rangeOfAge = data[schoolName]['年齡'][index]['年齡層'].replace('歲', '').replace('以上', '').split('-')
            if len(rangeOfAge) == 2:
                for i in range(len(ageRange)):
                    if int(rangeOfAge[1]) >= ageRange[i][0] and int(rangeOfAge[1]) <= ageRange[i][1]:
                        sumAgeData[schoolName][i] += int(data[schoolName]['年齡'][index]['人數'])
            elif rangeOfAge[0] == '不明':
                unknown += int(data[schoolName]['年齡'][index]['人數'])
            else:
                for i in range(len(ageRange)):
                    if int(rangeOfAge[0]) >= ageRange[i][0] and int(rangeOfAge[0]) <= ageRange[i][1]:
                        sumAgeData[schoolName][i] += int(data[schoolName]['年齡'][index]['人數'])
        sumAgeData[schoolName].append(unknown)
    return sumAgeData, labels
