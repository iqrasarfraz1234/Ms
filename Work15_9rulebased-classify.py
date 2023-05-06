# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:18:54 2022

@author: iammu
"""


def multipleSanads(txt):
    WordReplace=["حدثني","وحدثنا","حدثنا","نحوه","عن","قال،","فقال","سمعت","يقول","أنه","سمع","أخبرني","أن","أخبرنا","أنه","اخبرنا","سال","وقال","قالت","قالا","جميعا","قلت","أنها","وحدثني","في حديثه","يخطب","أخبره","تابعه","إنه","انه","كثيرا","قال:","قال","أنبأنا","إذا","أحدثكم","قام","فكتب","حديث","حديثه","أخبرهم","وكانت","يحدث","يخبر","فقلت","حدث","وكان","يخبر","لحديث","حدثها","حدثتنيه","ثقة","عقلت","أخبروني","حدث","وقد","روى","صحبت","حدثناه","سألت","هرقل","لي","هذا","الحديث","وأنبأنا","حدثكم","من","ولقد","وعن","شهدت","كتب","زوج","يذكر","سألني","قالوا","إلى","فكان","لما","قدم","أشياء","رواية","رأيت","أقبلت","قراءة","وأنا","أسمع","إن","حدثه","بهذا","حديثا","بأى","اخبرني","كان",'كنت',"يحدثونه","حدثتني","شىء","وغير","واحد","أسمع","وأخبرني"]
    WithoutAhrabTxt=""
    for  i in range(len(txt)):
        no=ord(txt[i])
        if(no==1614 or no==1615 or no==1616 or no==1618 or no==1617 or no==1612 or no==1613 or no==1611):
            continue
        else:
            WithoutAhrabTxt+=txt[i]
            
    # print(WithoutAhrabTxt)
    
    sanadList =[]
    txtList = []
    # txtList=WithoutAhrabTxt.split(" ")
    if(WithoutAhrabTxt.__contains__("ح‏.")):
        txtList=WithoutAhrabTxt.split("ح‏.")
    elif(WithoutAhrabTxt.__contains__(" ح، ")):
        txtList=WithoutAhrabTxt.split(" ح، ")
    elif(WithoutAhrabTxt.__contains__(" ح. ")):
        txtList=WithoutAhrabTxt.split(" ح. ")
    else:
        txtList=WithoutAhrabTxt.split(" ح ") 
    for sanad in range(len(txtList)):
        # Extract all words from hadithText Like "حدثني","وحدثنا","حدثنا"
        wordReplaceList_givenHadith = []

        # Extract all Narrator's Names from given hadith
        narratorsNameList = []

        # Variable for extracting WordReplace's element from hadithText  Like "حدثني","وحدثنا","حدثنا"
        get_WordReplace_Element = ""
        # Variable for extracting Name of Narrator from hadithText and at the end Matn of hadith
        narratorName = ""
        
        tokens_WithoutAerabText = txtList[sanad].split()
        for i in range(len(tokens_WithoutAerabText)):

            if (tokens_WithoutAerabText[i] in WordReplace) == True:
                get_WordReplace_Element += (tokens_WithoutAerabText[i] + " ")
                if (narratorName != ""):
                    narratorsNameList.append(narratorName)
                    narratorName = ""
            if (tokens_WithoutAerabText[i] in WordReplace) == False:
                narratorName += (tokens_WithoutAerabText[i] + " ")
                if (get_WordReplace_Element != ""):
                    wordReplaceList_givenHadith.append(get_WordReplace_Element)
                    get_WordReplace_Element = ""
        if(narratorName!="" and tokens_WithoutAerabText[i]):
            narratorsNameList.append(narratorName)
        sanadList.append(narratorsNameList)

    # # List of Prophet's صلی اللہ علیہ وآلہ وسلم name that are used in Ahadith
    prophetNamesReplacerList = ["رسول الله صلى الله عليه وسلم","النبي ـ صلى الله عليه وسلم" ,"النبي صلى الله عليه وسلم", "يا رسول الله","رسول الله","النبي ‌صلی ‌اللہ ‌علیہ ‌وآلہ ‌وسلم","صلى الله عليه وسلم","للنبي صلی اللہ علیہ وسلم","محمد صلی اللہ علیہ وآلہ وسلم"]

    for i in range(len(sanadList)):
        dum=[]
        for j in range(len(sanadList[i])):
            for name in range(len(prophetNamesReplacerList)):
                if(sanadList[i][j].__contains__(prophetNamesReplacerList[name])):
                    sanadList[i][j] = "محمد صلی اللہ علیہ وآلہ وسلم"
                    break
                
            if(sanadList[i][j].__contains__("محمد صلی اللہ علیہ وآلہ وسلم")):
                 dum.append(sanadList[i][j])
                 break
            else:
                 dum.append(sanadList[i][j])
        sanadList[i]=dum
    # print(sanadList)
    
    for i in range(len(sanadList)):
        for j in range(len(sanadList[i])):
            sanadList[i][j] = sanadList[i][j].strip()
            if (len(sanadList[i][j]) != 0):
                sanadList[i][j] = sanadList[i][j].replace('''"''', '')
                sanadList[i][j] = sanadList[i][j].replace("ـ رضى الله عنها ـ", "")
                sanadList[i][j] = sanadList[i][j].replace("رضى الله عنه", "")
                sanadList[i][j] = sanadList[i][j].replace("- رضى الله عنه -", "")
                sanadList[i][j] = sanadList[i][j].replace("رضى الله عنهما ", "")
                sanadList[i][j] = sanadList[i][j].replace("رضى الله عنها", "")
                sanadList[i][j] = sanadList[i][j].replace("رضى الله عنه", "")   
                sanadList[i][j] = sanadList[i][j].replace("رضى الله عنه -", "")
                sanadList[i][j] = sanadList[i][j].replace("رضى الله تعالى عنه", "")
                sanadList[i][j] = sanadList[i][j].replace("ـ رضي الله عنها ـ", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنهما ", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنهما", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنها", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنه", "")
                sanadList[i][j] = sanadList[i][j].replace("- رضي الله عنه -", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنه", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله عنه -", "")
                sanadList[i][j] = sanadList[i][j].replace("رضي الله تعالى عنه", "")
                sanadList[i][j] = sanadList[i][j].replace("على المنبر", "")
                sanadList[i][j] = sanadList[i][j].replace("-","")
                sanadList[i][j] = sanadList[i][j].replace("ـ","")
                sanadList[i][j] = sanadList[i][j].replace("،","")
                sanadList[i][j] = sanadList[i][j].replace("{", "")
                sanadList[i][j] = sanadList[i][j].replace("}", "")

                sanadList[i][j] = sanadList[i][j].strip()
                
        while("" in sanadList[i]) :
            sanadList[i].remove("")
            
            
    return sanadList
# _____________________________________________________________________

def singleSanad(HadithText):
    hadithText = HadithText.strip()

    # Variable that contains without_Aeraab hadithText
    withoutAerabText = ""

    # Aeraab Remover Code
    for i in range(len(hadithText)):
        no = ord(hadithText[i])
        if (no == 1614 or no == 1615 or no == 1616 or no == 1618 or no == 1617 or no == 1612 or no == 1613 or no == 1611):
            continue
        else:
            withoutAerabText += hadithText[i]
            
    tokens_WithoutAerabText = withoutAerabText.split(" ")
 
    # Words that replace from hadithText  
    WordReplace=["حدثني","وحدثنا","حدثنا","نحوه","عن","قال","فقال","سمعت","يقول","أنه","سمع","أخبرني","أن","أخبرنا","اخبرنا","حدث","أنه","سال","قالت","قالا","جميعا","قلت","أنها","وحدثني","أخبره","في حديثه","يخطب","تابعه","إنه","انه","كثيرا","قال:","أنبأنا","أحدثكم","إذا","قام","فكتب","يحدث","فقلت","قالوا","حديثه","يخبر","أخبرهم","وكانت","حديث","وقد","عقلت","وكان","لحديث","ثقة","حدثتنيه","حدثها","يخبر","أخبروني","وقال","حدث","روى","هذا","سألت","حدثناه","هرقل","لي","صحبت","الحديث","حدثكم","وأنبأنا","من","كتب","شهدت","وعن","زوج","ولقد","يذكر","سألني","فكان","إلى","لما","قدم","أشياء","بهذا","رأيت","أقبلت","رواية","قال،","قراءة","وأنا","إن","أسمع","حدثه","بأى","حديثا","كان",'كنت',"اخبرني","يحدثونه","حدثتني","شىء","أسمع","وغير","واحد","وأخبرني"]



    # Extract all words from hadithText Like "حدثني","وحدثنا","حدثنا"
    wordReplaceList_givenHadith = []

    # Extract all Narrator's Names from given hadith
    narratorsNameList = []

    # Variable for extracting WordReplace's element from hadithText  Like "حدثني","وحدثنا","حدثنا"
    get_WordReplace_Element = ""

    # Variable for extracting Name of Narrator from hadithText and at the end Matn of hadith
    narratorName = ""

    for i in range(len(tokens_WithoutAerabText)):

        if (tokens_WithoutAerabText[i] in WordReplace) == True:
            get_WordReplace_Element += (tokens_WithoutAerabText[i] + " ")
            if (narratorName != ""):
                narratorsNameList.append(narratorName)
                narratorName = ""
        if (tokens_WithoutAerabText[i] in WordReplace) == False:
            narratorName += (tokens_WithoutAerabText[i] + " ")
            if (get_WordReplace_Element != ""):
                wordReplaceList_givenHadith.append(get_WordReplace_Element)
                get_WordReplace_Element = ""


    # List of Prophet's صلی اللہ علیہ وآلہ وسلم name that are used in Ahadith
    prophetNamesReplacerList = ["رسول الله صلى الله عليه وسلم","النبي ـ صلى الله عليه وسلم" ,"النبي صلى الله عليه وسلم","النبي ‌صلی ‌اللہ ‌علیہ ‌وآلہ ‌وسلم","رسول الله","للنبي صلی اللہ علیہ وسلم","صلى الله عليه وسلم", "يا رسول الله",
                                        "محمد صلی اللہ علیہ وآلہ وسلم"]


    # Script for Qauli and Faeli Hadith in which Prophet's(صلی اللہ علیہ وآلہ وسلم) name used in Matn only
    for i in range(len(prophetNamesReplacerList)):
        if (prophetNamesReplacerList[i] not in narratorsNameList and narratorName.__contains__(prophetNamesReplacerList[i])):
            narratorsNameList.append("محمد صلی اللہ علیہ وآلہ وسلم")

    # Script also used for same work as mentioned in above comment
    for i in range(len(narratorsNameList)):
        for j in range(len(prophetNamesReplacerList)):
            if (narratorsNameList[i].__contains__(prophetNamesReplacerList[j]) and narratorsNameList[i] !=prophetNamesReplacerList[j]):
                narratorsNameList[i] = "محمد صلی اللہ علیہ وآلہ وسلم"

    for i in range(len(prophetNamesReplacerList)):
        if(withoutAerabText.__contains__(prophetNamesReplacerList[i])):
            narratorsNameList.append("محمد صلی اللہ علیہ وآلہ وسلم")
    # Removing duplicate values
    narratorsNameList = list(dict.fromkeys(narratorsNameList))


    #   ****************New Search Algorithm asked by Sir****************

    # narratorsNameList[0] = "الحميدي عبد الله بن أبي الزبير"
    # Filtering Names of narrators
    for i in range(len(narratorsNameList)):
        narratorsNameList[i] = narratorsNameList[i].strip()
        if (len(narratorsNameList[i]) != 0):
            if (narratorsNameList[i][-1] == "،"):
                narratorsNameList[i] = narratorsNameList[i].replace("،", "")
     
        narratorsNameList[i] = narratorsNameList[i].replace('''"''', '')
        narratorsNameList[i] = narratorsNameList[i].replace("ـ رضى الله عنها ـ", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنهما ", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنهما", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنها", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنه", "")
        narratorsNameList[i] = narratorsNameList[i].replace("- رضى الله عنه -", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنه", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله عنه -", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضى الله تعالى عنه", "")
        
        narratorsNameList[i] = narratorsNameList[i].replace("ـ رضي الله عنها ـ", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنهما ", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنهما", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنها", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنه", "")
        narratorsNameList[i] = narratorsNameList[i].replace("- رضي الله عنه -", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنه", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنه -", "")
        narratorsNameList[i] = narratorsNameList[i].replace("رضي الله تعالى عنه", "")
        
        narratorsNameList[i] = narratorsNameList[i].replace("على المنبر", "")
        narratorsNameList[i] = narratorsNameList[i].replace("المنبر", "")
        narratorsNameList[i] = narratorsNameList[i].replace("-","")
        narratorsNameList[i] = narratorsNameList[i].replace("ـ","")
        narratorsNameList[i] = narratorsNameList[i].replace("،","")
        narratorsNameList[i] = narratorsNameList[i].replace("{", "")
        narratorsNameList[i] = narratorsNameList[i].replace("}", "")
        narratorsNameList[i] = narratorsNameList[i].strip()

    
    while("" in narratorsNameList) :
        narratorsNameList.remove("")
        
    #agr remove comma here than malik will be name 
    narratorsNameList =[name.replace("،","") for name in narratorsNameList]
    
    FinalList=[]
    for i in range(len(narratorsNameList)):
        if(narratorsNameList[i] == "محمد صلی اللہ علیہ وآلہ وسلم"):
            FinalList.append(narratorsNameList[i])
            break
        else:
            FinalList.append(narratorsNameList[i])
    
    return FinalList


    # return narratorsNameList




#_______________Main Code___________

# finalNarratorsNameList=[]
#
# #
# import pandas as pd
# # df = pd.read_excel("C:/Users/iammu/OneDrive/Desktop/SahihAhadith2400.xlsx")
# # df = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadirh reserach/Other Files/SahihAhadith2400.xlsx" , engine='openpyxl')
#
# df2 = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadith py/Name Extraction Work/comparison/Overall Comparison (after removing error in rule-based)/Exact_RuleBased_OldNER_NewNERNames.xlsx" , engine='openpyxl' )
# #df2 = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadirh reserach/Other Files/Testing600Hadith.xlsx" , engine='openpyxl')
#
# df2 = df2.dropna()
# hadithList = df2.HadithText
#
# for i in hadithList:
#
#     if (i.__contains__(" ح ") or i.__contains__(" ح، ") or i.__contains__("ح‏.") or i.__contains__(" ح. ")):
#         return_M_List= multipleSanads(i)
#         finalNarratorsNameList.append(return_M_List)
#     else:
#         return_S_List = singleSanad(i)
#         finalNarratorsNameList.append(return_S_List)


#
# For Testing Purpose (Only For One Hadith)

finalNarratorsNameList=[]
import pandas as pd
df = pd.read_excel("C:/Users/Iqra Sarfraz/Desktop/hadirh reserach/Name Extraction Work/comparison/HadithFromDifferentBooks.xlsx")
hadithList = df["HadithText"][65]


if(hadithList.__contains__(" ح ") or hadithList.__contains__(" ،ح ") or hadithList.__contains__(".ح‏") or hadithList.__contains__(" .ح ")):
    return_M_List= multipleSanads(hadithList)
    finalNarratorsNameList.append(return_M_List)
else:
    return_S_List = singleSanad(hadithList)
    finalNarratorsNameList.append(return_S_List)
finalNarratorsNameList

#Data frame for list of names after rules based name extract

# df3 = pd.DataFrame()
# df3['HadithText'] = df2['HadithText']
# df3['Exact_Names'] = df2['Exact_Names']
# df3['NarratorListAfterRuleBased'] = finalNarratorsNameList
# df3.to_excel("C:/Users/Iqra Sarfraz/Desktop/AfterRuleBasedFullHadith.xlsx")

df3 = pd.DataFrame()
df3['HadithText'] = df['HadithText']
df3['Exact_Names'] = df['Exact_Names']
df3['NarratorListAfterRuleBased'] = finalNarratorsNameList
df3.to_excel("C:/Users/Iqra Sarfraz/Desktop/AfterRuleBasedFullHadith.xlsx")
# ###########################################

# output_path = "/content/gdrive/My Drive/"
# dfDum.to_excel(output_path + "Compare Exact With Rule Based After removing RA.xlsx",index=False)
# dfDum.to_excel("C:/Users/Iqra Sarfraz/Desktop/matchnamedatabase.xlsx")
# print(dfDum.head(1))

###############################################################################################################
