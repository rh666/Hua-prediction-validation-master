import sys as sys

def actualtodict(file,time):
    """
    function to the stock price in a certain hour in the actual file a dictionary

    :param file:
    :param time:
    :return:
    """

    a = file.readline().split('|')

    while a[0] != str(time):
        a = file.readline().split('|')
        if a == ['']:
            print 'the time is not reached yet'
            return

    actualdict = {}

    while a[0] == str(time):


        actualdict[a[1]] = float(a[2])

        #print a[1], actualdict[a[1]]

        a = file.readline().split('|')

    # print a[0]

    return actualdict, a


def printresult(errorsum, errornum, window, starttime, file):
    tobeprint = []
    if len(errorsum) >= window:


        tobeprint.append(str(starttime + 1 ))
        tobeprint.append(str(starttime + window))


        if sum(errornum[len(errornum) - window:len(errornum)]) == 0:
            tobeprint.append('ignore')
        else:
            printerror = sum(errorsum[len(errorsum) - window:len(errorsum)]) / sum(errornum[len(errornum) - window:len(errornum)])

            tobeprint.append(str(round(printerror, 2)))

        file.write('|'.join(tobeprint) + '\n')
        # print '|'.join(tobeprint)


def main():

    window = int(open(sys.argv[1]).read())
    actual = open(sys.argv[2], 'r')
    predicted = open(sys.argv[3],'r')


    comparison = open(sys.argv[4],'a')

    linepredicted = predicted.readline().split('|') ### current line in predicted

    timestart = int(linepredicted[0])  ### starting time in predicted.

    temptime = timestart ### current time. will be updated


    actualdict, nextinitial = actualtodict(actual, temptime)
    ####
    # actualdict: dictionary of the actual stock price in current hour
    # nextinitial: store the first line that is not in current hour

    errorsum = []   # errorsum: each element is the sum of errors in a certain hour
    errornum = []   # errornum: each elements is the number of stocks in predicted file in a certain hour

    while linepredicted !=  [''] and linepredicted !=  ['\n']:
    ##### read predicted file line by line until the end


        hourerror = []   ## hourerror: record all errors in current hour. will be updated hour by hour

        while linepredicted != [''] and linepredicted !=  ['\n'] and int(linepredicted[0]) == temptime:
        ### calculate error hour by hour


            temperror = abs(float(linepredicted[2]) - actualdict[linepredicted[1]])
            # error of the current stock in current hour

            hourerror.append(temperror)     # an array to store errors of all stock in current hour

            linepredicted = predicted.readline().split('|')     ## update current line after computation

        errorsum.append(sum(hourerror))     # update the sum of errors of all stock in current hour
        errornum.append(len(hourerror))     # update the number of stock in predicted file in current hour

        printresult(errorsum, errornum, window, temptime - window,comparison)

        ### print the newly arrived comparison


        if linepredicted !=  [''] and linepredicted !=  ['\n']:


            if int(linepredicted[0]) != temptime + 1:

                for zeronum in range(int(linepredicted[0]) - temptime - 1):
                    errorsum.append(0)
                    errornum.append(0)
            ######  if there is missing hours in predicted file (low confidence for all predicted stock price in the hour)
            ######  record 0 for sum of the error and 0 for number of the stock

                    printresult(errorsum, errornum, window, temptime - window + zeronum, comparison)

                    ### still compute and print the average error in the window for the missing hour

            tempinitial = nextinitial


            lasttime = temptime
            temptime = int(linepredicted[0])  # update the time into the next in predicted file



            actualdict, nextinitial = actualtodict(actual, temptime) # get the dictionary for actual data for the corresponding hour

            if  int(linepredicted[0]) == lasttime + 1:
                actualdict[tempinitial[1]] = float(tempinitial[2])

            ### if there is no missing hour, complete the dictionary with the first line of next hour in actual file


if __name__ == '__main__':
    main()





