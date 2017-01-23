tableData = [['apples', 'oranges', 'cherries', 'banana'],
['Alice', 'Bob', 'Carol', 'David'],
['dogs', 'cats', 'moose', 'goose']]


def printTable(tableData):
    colWidths = [0] * len(tableData)
    index = 0
    for line in tableData:
        maxlength = 0
        for word in line:
            if len(word) > maxlength:
                maxlength = len(word)
        colWidths[index] = maxlength
        index+=1

    print(colWidths)

    for i in range(len(tableData[0])):
        for j in range(len(tableData)):
            print(tableData[j][i].ljust(colWidths[j]+1), end='')
        print('')

printTable(tableData)