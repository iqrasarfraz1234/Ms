

# import pandas as pd
# df2 = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadith py/Name Extraction Work/comparison/NewNERandExactNames/NamesAndLengthComparison_NewNER_andExactNamesFrom480Hadith.xlsx", engine='openpyxl')
#
# df2 = df2.dropna()
# finalNarratorsNameList = df2.new_NERNames[3]

import mysql.connector
myDb = mysql.connector.connect(host='localhost', user='root', passwd='cnic1330251711906', database='scholar_database')

myCursor = myDb.cursor()


# finalNarratorsNameList=[['عبد الله بن مسلمة', 'مالك', 'زيد بن أسلم', 'عطاء بن يسار', 'ابن عباس', 'محمد صلی اللہ علیہ وآلہ وسلم']]
# hadithtext="حدثنا عبد الله بن مسلمة، عن مالك، عن زيد بن أسلم، عن عطاء بن يسار، عن ابن عباس، قال قال النبي صلى الله عليه وسلم " أريت النار فإذا أكثر أهلها النساء يكفرن ". قيل أيكفرن بالله قال " يكفرن العشير، ويكفرن الإحسان، لو أحسنت إلى إحداهن الدهر ثم رأت منك شيئا قالت ما رأيت منك خيرا قط ".   "
# finalNarratorsNameList=[['محمد بن سنان', 'فليح'], ['إبراهيم بن المنذر', 'محمد بن فليح', 'أبي', 'هلال بن علي', 'عطاء بن يسار', 'أبي هريرة', 'محمد صلی اللہ علیہ وآلہ وسلم']]
finalNarratorsNameList=[['أحمد بن يونس وموسى بن إسماعيل', 'إبراهيم بن سعد', 'ابن شهاب', 'سعيد بن المسيب', 'أبي هريرة', 'محمد صلی اللہ علیہ وآلہ وسلم']]
# finalNarratorsNameList=[['عبد الله بن مسلمة', 'مالك', 'زيد بن أسلم', 'عطاء بن يسار', 'ابن عباس', 'محمد صلی اللہ علیہ وآلہ وسلم'],['أحمد بن يونس وموسى بن إسماعيل', 'إبراهيم بن سعد', 'ابن شهاب', 'سعيد بن المسيب', 'أبي هريرة', 'محمد صلی اللہ علیہ وآلہ وسلم']]
# finalNarratorsNameList=[[['محمد بن سنان', 'فليح'], ['إبراهيم بن المنذر', 'محمد بن فليح', 'أبي', 'هلال بن علي', 'عطاء بن يسار', 'أبي هريرة', 'محمد صلی اللہ علیہ وآلہ وسلم']],['أحمد بن يونس وموسى بن إسماعيل', 'إبراهيم بن سعد', 'ابن شهاب', 'سعيد بن المسيب', 'أبي هريرة', 'محمد صلی اللہ علیہ وآلہ وسلم']]

rulebasedList=[]
finalMatchList=[]
finalInfoList_Narrators = []
# Cross Check of Narrators_Names with Database
for i in range(len(finalNarratorsNameList)):
    if(len(finalNarratorsNameList[i])==0):
        continue
    index = finalNarratorsNameList[i][0]
    #print(finalNarratorsNameList[i],end="\n"
    matchList=[]
    if(type(index)==str):
        for j in range(len(finalNarratorsNameList[i])):
            # Query for checking Narrator's Info in scholars table
            query = '''select * from scholars where name like "''' + finalNarratorsNameList[i][j] + '''";'''
            myCursor.execute(query)
            result = myCursor.fetchall()
            # Check if Narrator's Info found in scholars table
            if (len(result) != 0):
                finalInfoList_Narrators.append(result[0])
            # Check if Narrator's Info not found in scholars table
            if (len(result) == 0):
                # Query for checking Narrator's Info in scholar_other_names table
                query = '''select * from scholar_other_names where name like "''' + finalNarratorsNameList[i][j]  + '''";'''
                myCursor.execute(query)
                result = myCursor.fetchall()
                # Check if Narrator's Info found in scholar_other_names table
                if (len(result) != 0):
                    finalInfoList_Narrators.append(result[0])
        # print(finalInfoList_Narrators)
        # List of all Narrator's Ids of given hadith that are present in our DataBase
        finalIdList_Narrators = []
        counter_Musnad = 0
        # Code for Extracting all Narrator's Ids of Given Hadith and storing in finalIdList_Narrators List
        for j in range(len(finalInfoList_Narrators)):
            # Check if Narrator's Info is found from scholars table
            if (len(finalInfoList_Narrators[j]) == 8):
                finalIdList_Narrators.append(finalInfoList_Narrators[j][0])
                continue
            # Check if Narrator's Info is found from scholar_other_names table
            if (len(finalInfoList_Narrators[j]) == 3):
                finalIdList_Narrators.append(finalInfoList_Narrators[j][1])
                continue

        # print(finalIdList_Narrators)
        reason_Musnad = ""
        reason_Sahih = ""
        reason_Zaeef = ""
        reason_Munqate = ""
        reason_Muedal = ""
        reason_Muallaq = ""
        reason_Mursal = ""

        counter_Musnad = 0
        for i in range(len(finalIdList_Narrators)):
            if (i <= len(finalIdList_Narrators) - 2):
                query = "select teacher_id from teachers where scholar_id = " + str(finalIdList_Narrators[i]) + ";"

                myCursor.execute(query)

                result = myCursor.fetchall()

                teacher_ids = []
                for j in range(len(result)):
                    teacher_ids.append(result[j][0])
                # print(teacher_ids)
                if (finalIdList_Narrators[i + 1] in teacher_ids):
                    counter_Musnad += 1
                else:

                    query = "select student_id from students where scholar_id = " + str(finalIdList_Narrators[i + 1]) + ";"

                    myCursor.execute(query)

                    result = myCursor.fetchall()

                    student_ids = []
                    for k in range(len(result)):
                        teacher_ids.append(result[k][0])

                    if (finalIdList_Narrators[i] in student_ids):
                        counter_Musnad += 1
                    else:
                        # print("The given hadith is Munqate.")

                        query = "select teacher_id from teachers where scholar_id = " + str(finalIdList_Narrators[i]) + ";"

                        myCursor.execute(query)

                        result1 = myCursor.fetchall()

                        munqateTeacherIds1 = []

                        for j in range(len(result1)):
                            munqateTeacherIds1.append(result1[j][0])

                        isNotPresent1 = 0

                        if (finalIdList_Narrators[i + 1] not in munqateTeacherIds1):
                            isNotPresent1 = 1

                        if (isNotPresent1):

                            munqateTeacherIds2 = []

                            for k in range(len(munqateTeacherIds1)):

                                query = "select teacher_id from teachers where scholar_id = " + str(
                                    munqateTeacherIds1[k]) + ";"

                                myCursor.execute(query)

                                result2 = myCursor.fetchall()

                                for m in range(len(result2)):
                                    munqateTeacherIds2.append(result2[m][0])

                            isNotPresent2 = 0

                            if (finalIdList_Narrators[i + 1] not in munqateTeacherIds2):
                                isNotPresent2 = 1

                            if (isNotPresent2):
                                # reason_Zaeef = "The given hadith is Zaeef."
                                reason_Zaeef = 'ضعيف'
                                reason_Muedal = "The given hadith is Muedal because two consecutive narrators are missing."

                            else:
                                # reason_Zaeef = "The given hadith is Zaeef."
                                reason_Zaeef = 'ضعيف'
                                reason_Munqate = "The given hadith is Munqate because chain is broken at some point."

        if (counter_Musnad == len(finalIdList_Narrators) - 1 and len(finalIdList_Narrators) > 1):
            if (1 in finalIdList_Narrators):
                reason_Musnad = "The given hadith is Musnad because no narrator is missing from the chain till Prophet (صلی اللہ علیہ وآلہ وسلم)."
                scholarsStatus = []
                for i in range(len(finalIdList_Narrators)):
                    query = "select Jarah_Taadeel from scholars where id = " + str(finalIdList_Narrators[i]) + ";"

                    myCursor.execute(query)

                    result = myCursor.fetchall()

                    scholarsStatus.append(result[0][0])

                if ("Zaeef" in scholarsStatus):
                    print("Here")
                else:
                    # reason_Sahih = "The given hadith is also Sahih."
                    reason_Sahih = 'صحيح'
            else:
                scholarsStatus = []
                for i in range(len(finalIdList_Narrators)):
                    query = "select Jarah_Taadeel from scholars where id = " + str(finalIdList_Narrators[i]) + ";"

                    myCursor.execute(query)

                    result = myCursor.fetchall()

                    scholarsStatus.append(result[0][0])

                if ("Zaeef" in scholarsStatus):
                    # print("Here")
                    reason_Zaeef = 'ضعيف'
                else:
                    # reason_Sahih = "The given hadith is Sahih."
                    reason_Sahih = 'صحيح'

        if (len(finalIdList_Narrators) == 1):
            if (1 in finalIdList_Narrators):
                # reason_Zaeef = "The given hadith is Zaeef."
                reason_Zaeef = 'ضعيف'
                reason_Muallaq = "The given hadith is Muallaq because whole chain of narrators is missing."

        statusList = []
        for i in range(len(finalIdList_Narrators)):
            query = "select status from scholars where id = " + str(finalIdList_Narrators[i]) + ";"

            myCursor.execute(query)

            result = myCursor.fetchall()

            for j in range(len(result)):
                statusList.append(result[j][0])

        # Code not for copy
        sanadOrder = []
        sanadOrder.append({'key': 1, 'status': 'Rasool Allah'})

        sanadOrder.append({'key': 2, 'status': 'Comp.(RA)'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [1st Generation]'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [2nd Generation]'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [3rd Generation]'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [4th generation]'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [6th generation]'})
        sanadOrder.append({'key': 2, 'status': 'Comp.(RA) [7th generation]'})

        sanadOrder.append({'key': 3, 'status': "Follower(Tabi')"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [1st Generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [2nd Generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [3rd Generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [4th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [5th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [6th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [7th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [8th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [9th generation]"})
        sanadOrder.append({'key': 3, 'status': "Follower(Tabi') [11th generation]"})

        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi')"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [7th generation] [Maliki]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [9th generation] [Shafi'ee]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [Hanafi]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [8th generation]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [7th generation]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [6th generation]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [9th generation]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [10th generation]"})
        sanadOrder.append({'key': 4, 'status': "Succ. (Taba' Tabi') [9th generation] [Other]"})

        sanadOrder.append({'key': 5, 'status': "3rd Century AH"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [11th generation] [Shafi'ee]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [11th generation] [Hanafi]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [Shafi'ee]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [12th generation]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [10th generation] [Hanbali]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [10th generation]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [11th generation]"})
        sanadOrder.append({'key': 5, 'status': "3rd Century AH [10th generation] [Hanafi]"})

        sanadOrder.append({'key': 6, 'status': "4th Century AH"})
        sanadOrder.append({'key': 6, 'status': "4th Century AH [Other]"})
        sanadOrder.append({'key': 6, 'status': "4th Century AH [Shafi'ee]"})
        sanadOrder.append({'key': 6, 'status': "4th Century AH [Hanbali]"})

        sanadOrder.append({'key': 7, 'status': "5th Century AH"})
        sanadOrder.append({'key': 7, 'status': "5th Century AH [Other]"})
        sanadOrder.append({'key': 7, 'status': "5th Century AH [Hanbali]"})

        sanadOrder.append({'key': 8, 'status': "6th Century AH"})
        sanadOrder.append({'key': 8, 'status': "6th Century AH [Hanbali]"})
        sanadOrder.append({'key': 8, 'status': "6th Century AH [Maliki]"})
        sanadOrder.append({'key': 8, 'status': "6th Century AH [Shafi'ee]"})

        sanadOrder.append({'key': 9, 'status': "7th Century AH"})
        sanadOrder.append({'key': 9, 'status': "7th Century AH [Shafi'ee]"})
        sanadOrder.append({'key': 9, 'status': "7th Century AH [Hanbali]"})

        sanadOrder.append({'key': 10, 'status': "8th Century AH"})
        sanadOrder.append({'key': 10, 'status': "8th Century AH [Hanbali]"})
        sanadOrder.append({'key': 10, 'status': "8th Century AH [Shafi'ee]"})

        sanadOrder.append({'key': 11, 'status': "9th Century AH"})
        sanadOrder.append({'key': 11, 'status': "9th Century AH [Shafi'ee]"})
        sanadOrder.append({'key': 11, 'status': "9th Century AH [Hanbali]"})

        sanadOrder.append({'key': 12, 'status': "10th Century AH"})
        sanadOrder.append({'key': 12, 'status': "10th Century AH [Hanbali]"})

        sanadOrder.append({'key': 13, 'status': "11th Century AH"})
        sanadOrder.append({'key': 13, 'status': "11th Century AH [Hanbali]"})

        sanadOrder.append({'key': 14, 'status': "12th Century AH"})
        sanadOrder.append({'key': 14, 'status': "12th Century AH [Hanbali]"})

        sanadOrder.append({'key': 15, 'status': "13th Century AH"})
        sanadOrder.append({'key': 15, 'status': "13th Century AH [Hanbali]"})

        sanadOrder.append({'key': 16, 'status': "14th Century AH"})
        sanadOrder.append({'key': 16, 'status': "14th Century AH [Hanbali]"})

        sanadOrder.append({'key': 17, 'status': "15th Century AH"})
        sanadOrder.append({'key': 17, 'status': "15th Century AH [Hanbali]"})

        extractingKeysFromSanadOrder = []
        for i in range(len(statusList)):
            for j in range(len(sanadOrder)):
                if (statusList[i] == sanadOrder[j].get("status")):
                    extractingKeysFromSanadOrder.append(sanadOrder[j].get('key'))

        if ((extractingKeysFromSanadOrder[-1] == 1) and (extractingKeysFromSanadOrder[-2] == 3)):
            reason_Mursal = "The given hadith is Mursal because Follower(Tabi') is directly narrated from Prophet (صلی اللہ علیہ وآلہ وسلم)."

        # print(reason_Musnad)
        print(reason_Sahih)
        print(reason_Zaeef)
        # print(reason_Munqate)
        # print(reason_Muedal)
        # print(reason_Muallaq)
        # print(reason_Mursal)


        rulebasedList.append(reason_Sahih)
    print(rulebasedList)
import pandas as pd
dfTestMatchList = pd.DataFrame()
dfTestMatchList['Rulebased']=rulebasedList
dfTestMatchList.to_excel("C:/Users/Iqra Sarfraz/Desktop/rulebasedclassify2.xlsx")


 # ....................................................Multiple chain of narrators..........................................................
# import pandas as pd
# dfTestMatchList = pd.DataFrame()
#
# dfTestMatchList['Rulebased']=rulebasedList
# #
# dfTestMatchList.to_excel("C:/Users/Iqra Sarfraz/Desktop/rulebasedclassify2.xlsx")

    # else:
    #     singleMatchList=[]
    #     for j in range(len(finalNarratorsNameList[i])):
    #         matchList=[]
    #         for k in range(len(finalNarratorsNameList[i][j])):
    #             # Query for checking Narrator's Info in scholars table
    #             query = '''select * from scholars where name like "''' + finalNarratorsNameList[i][j][k] + '''";'''
    #             myCursor.execute(query)
    #             result = myCursor.fetchall()
    #             # Check if Narrator's Info found in scholars table
    #             if (len(result) != 0):
    #                 finalInfoList_Narrators.append(result[0])
    #             # Check if Narrator's Info not found in scholars table
    #             if (len(result) == 0):
    #                 # Query for checking Narrator's Info in scholar_other_names table
    #                 query = '''select * from scholar_other_names where name like "''' + finalNarratorsNameList[i][j][k] + '''";'''
    #                 myCursor.execute(query)
    #                 result = myCursor.fetchall()
    #                 # Check if Narrator's Info found in scholar_other_names table
    #                 if (len(result) != 0):
    #                     finalInfoList_Narrators.append(result[0])
    #         print(finalInfoList_Narrators)
            # # List of all Narrator's Ids of given hadith that are present in our DataBase
            # finalIdList_Narrators = []
            # counter_Musnad = 0
            # # Code for Extracting all Narrator's Ids of Given Hadith and storing in finalIdList_Narrators List
            # for j in range(len(finalInfoList_Narrators)):
            #     # Check if Narrator's Info is found from scholars table
            #     if (len(finalInfoList_Narrators[j]) == 8):
            #         finalIdList_Narrators.append(finalInfoList_Narrators[j][0])
            #         continue
            #     # Check if Narrator's Info is found from scholar_other_names table
            #     if (len(finalInfoList_Narrators[j]) == 3):
            #         finalIdList_Narrators.append(finalInfoList_Narrators[j][1])
            #         continue
            #
            # print(finalIdList_Narrators)


#                 if(finalNarratorsNameList[i][j][k] in result) or (finalNarratorsNameList[i][j][k] in result2):
#                     matchList.append(finalNarratorsNameList[i][j][k])
#                     continue
#             singleMatchList.append(matchList)
#         finalMatchList.append(singleMatchList)
# print(finalMatchList)

# prob_class = []
#
# for i in range(len(prob)):
#     if(prob[i][0]>0.5):
#         prob_class.append('صحيح')
#     else:
#         prob_class.append('ضعيف')
#

df = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadirh reserach/basic files/HadithFromDifferentBooks.xlsx")
df2 = df.dropna()
d1 = df2.Status[5]
# print(d1)
# d1 = FinalStatus_test
# # Matching Predicted Results with Actual Testing Results
# notMatch = 0
# for i in range(len(prob_class)):
#     if(prob_class[i]!=d1[i]):
#         print(i, end=" ")
#         notMatch+=1
#
#
# accuracy = (len(Y_test)-notMatch)/len(Y_test)

correct_predictions = 0
total_predictions = len(d1)


for d1, rulebasedList in zip(d1, rulebasedList):
    if d1 == rulebasedList:
        correct_predictions += 1
    # print(correct_predictions)

accuracy = (correct_predictions / total_predictions) * 100
print("Accuracy:", accuracy)
