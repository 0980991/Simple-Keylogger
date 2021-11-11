def datetimeList2String(datetimelist):
    output = ''
    for datetime in datetimelist:
        output += str(datetime)[:-7].replace(' ', '-').replace(':', '') + ' '
    return output

def addEmailSubject2Message(subject, message):
    return f'Subject: {readableDateTime(subject)} \n{message}'

def readableDateTime(datetimelist):
    output = 'From: '
    for datetime in datetimelist:
        datetime = str(datetime)
        datetime = datetime[:-7]
        output += datetime + ' | Until: '
    return output[:-10]

