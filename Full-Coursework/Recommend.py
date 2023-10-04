import os
import csv
import math
import numpy as np


def PositiveEntriesCalculation(root):
    allElementsInFileHistory = ReadFile(root)
    allElementsInFileHistory.pop(0)
    allHistoryNoSpaces = [i for i in allElementsInFileHistory if i != []]
    removeDuplicatesHistory = list(set(tuple(sub) for sub in allHistoryNoSpaces))
    return len(removeDuplicatesHistory), removeDuplicatesHistory


def ShoppingCartCalculator(root):
    allElementsInFileQueries = ReadFile(root)
    allQueriesNoSpaces = [i for i in allElementsInFileQueries if i != []]
    return allQueriesNoSpaces


def AverageAngleCalculator(root,historyList):
    appendingList = []
    allElementsInFileHistory = ReadFile(root)
    appendingList.append(allElementsInFileHistory[0][0])
    historyList.insert(0,appendingList)
    number_cust = historyList[0][0].split(" ")[0]
    number_items = historyList[0][0].split(" ")[1]
    historyList.pop(0)
    emptyList = []
    number_zeros = int(number_cust) * int(number_items)
    for elements in range(0,number_zeros):
        emptyList.append(0)
    vectorList = [emptyList[i:i + int(number_items)] for i in range(0, len(emptyList), int(number_items))]
    for values in range(0,len(historyList)):
        list_num = list(historyList[values])[0].split(" ")[1]
        element_num = list(historyList[values])[0].split(" ")[0]
        vectorList[int(list_num)-1][int(element_num)-1] = 1

    averageAngleStatement = True
    averageAngle = AngleCalculator(vectorList,number_cust,number_items,None,None,averageAngleStatement)
    return round((sum(averageAngle)/len(averageAngle)),2)


def ItemMatchCalculator(root,historyList,queriesNum):
    appendingList = []
    allElementsInFileHistory = ReadFile(root)
    appendingList.append(allElementsInFileHistory[0][0])
    historyList.insert(0, appendingList)
    number_cust = historyList[0][0].split(" ")[0]
    number_items = historyList[0][0].split(" ")[1]
    historyList.pop(0)
    emptyList = []
    number_zeros = int(number_cust) * int(number_items)
    for elements in range(0, number_zeros):
        emptyList.append(0)
    vectorList = [emptyList[i:i + int(number_items)] for i in range(0, len(emptyList), int(number_items))]
    for values in range(0, len(historyList)):
        list_num = list(historyList[values])[0].split(" ")[1]
        element_num = list(historyList[values])[0].split(" ")[0]
        vectorList[int(list_num) - 1][int(element_num) - 1] = 1

    averageAngleStatement = False
    finalAnglesList = []
    for angleValues in range(0,len(list(x for x in queriesNum[0].split(" ")))):
        allElementsInteger = [eval(i) for i in queriesNum[0].split(" ")]
        finalAllElementsIntegers = [x for x in allElementsInteger if x == allElementsInteger[angleValues]]
        angleAndQuery = AngleCalculator(vectorList,number_cust,number_items,allElementsInteger,finalAllElementsIntegers[0],averageAngleStatement)
        finalAngleAndQuery = [angleAndQuery[0],angleAndQuery[1],angleAndQuery[2]]
        finalAnglesList.append(finalAngleAndQuery)

    return finalAnglesList


def BuildRecommendationBundle():
    onlyTextFilesAndRoots = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".txt"):
                onlyTextFilesAndRoots.append(file)
                onlyTextFilesAndRoots.append(os.path.join(root, file))

    improvedTextFilesAndRoots = [i for i in onlyTextFilesAndRoots if "history" in i or "out" in i or "queries" in i]
    multipleCorrectTextFilesAndRoots = [improvedTextFilesAndRoots[i:i + 6] for i in range(0, len(improvedTextFilesAndRoots), 6)]

    for removingFiles in multipleCorrectTextFilesAndRoots:
        if len(removingFiles) != 6:
            multipleCorrectTextFilesAndRoots.pop()

    for textFiles in multipleCorrectTextFilesAndRoots:
        outFile = [i for i in textFiles if "out" in i and len(i) < 10]
        historyFileRoot = [i for i in textFiles if "history" in i and len(i) >= 15]
        queriesFileRoot = [i for i in textFiles if "queries" in i and len(i) >= 15]

        finalOutFile = str(outFile)[1:-1]
        finalHistoryFileRoot = str(historyFileRoot)[1:-1]
        finalQueriesFileRoot = str(queriesFileRoot)[1:-1]

        positiveEntriesResult = PositiveEntriesCalculation(finalHistoryFileRoot)
        averageAngleResult = AverageAngleCalculator(finalHistoryFileRoot,positiveEntriesResult[1])

        print(f"\n\nFile Name: {finalOutFile}\n\n")

        print(f"Positive entries: {positiveEntriesResult[0]}")
        print(f"Average angle: {averageAngleResult}")

        shoppingCartResult = ShoppingCartCalculator(finalQueriesFileRoot)
        for allItems in range(0,len(shoppingCartResult)):
            item_MatchResult = ItemMatchCalculator(finalHistoryFileRoot,positiveEntriesResult[1],shoppingCartResult[allItems])
            print(f"Shopping cart: {shoppingCartResult[allItems][0]}")
            finalItem_MatchList = []
            for finalItems in item_MatchResult:
                if finalItems[1] == "no match":
                    print(f"Item: {finalItems[0]} {finalItems[1]}")
                else:
                    print(f"Item: {finalItems[0]}; match: {finalItems[1]+1}; angle: {round(finalItems[2],2)}")
                    if finalItems[1] not in finalItem_MatchList:
                        finalItem_MatchList.append(finalItems[1])
            if item_MatchResult[0][1] == "no match" and len(item_MatchResult) == 1:
                print("Recommend: ")
            else:
                finalRecommendation = [x+1 for x in finalItem_MatchList]
                finalRecommendation = " ".join( repr(e) for e in finalRecommendation )
                print(f"Recommend: {finalRecommendation}")


def ReadFile(root):
    allLines = []
    finalroot = root.replace('\\\\','/')[1:][:-1]
    with open(finalroot, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            allLines.append(row)
    csvfile.close()
    return allLines


def AngleCalculator(v_list,n_cust,n_items,elements,queryNo,statement):
    if statement:
        angle_list = []
        angle_number_list = list(range(0,int(n_cust)))*int(n_items)
        vectorsCompleted = [0]
        skip_num = []
        for numbers in range(0,int(n_items)):
            skip_num.append(int(n_cust)*numbers)
        i = 0
        j = 0
        z = 0
        for A,B in enumerate(angle_number_list):
            if A in skip_num:
                i = skip_num[j] + j
                j += 1
                if A != skip_num[0]:
                    z += 1
                    vectorsCompleted.append(z)
            else:
                if A == i or B in vectorsCompleted:
                    pass
                else:
                    first_comparison_vector = np.array(v_list[z])
                    first_comparison_vector_magnitude = np.linalg.norm(first_comparison_vector)
                    second_comparison_vector = np.array(v_list[B])
                    second_comparison_vector_magnitude = np.linalg.norm(second_comparison_vector)

                    scalarproduct = sum(x * y for x, y in zip(first_comparison_vector, second_comparison_vector))
                    angle = math.degrees(math.acos(scalarproduct / (first_comparison_vector_magnitude * second_comparison_vector_magnitude)))
                    angle_list.append(angle)

        return angle_list

    else:
        item_angle_list = []
        just_angle_list = []
        item_angle_number_list = list(range(0,int(n_cust)))
        for itemValues in elements:
            item_angle_number_list.remove(int(itemValues)-1)
        for angleValues in item_angle_number_list:
            first_comparison_vector = np.array(v_list[int(queryNo)-1])
            first_comparison_vector_magnitude = np.linalg.norm(first_comparison_vector)
            second_comparison_vector = np.array(v_list[angleValues])
            second_comparison_vector_magnitude = np.linalg.norm(second_comparison_vector)

            scalarproduct = sum(x * y for x, y in zip(first_comparison_vector, second_comparison_vector))
            angle = math.degrees(math.acos(scalarproduct / (first_comparison_vector_magnitude * second_comparison_vector_magnitude)))
            item_angle_list.append(angleValues)
            item_angle_list.append(angle)
            just_angle_list.append(angle)

        smallestvalue = 100000000000000000000000000000000000
        for length,finalValues in enumerate(item_angle_list):
            if isinstance(finalValues, float) and length > 0 and finalValues < smallestvalue:
                smallestvalue = finalValues
            elif all(element == just_angle_list[0] for element in just_angle_list):
                return queryNo,"no match",None
        min_index = item_angle_list.index(smallestvalue)
        return queryNo,item_angle_list[min_index-1],item_angle_list[min_index]



BuildRecommendationBundle()