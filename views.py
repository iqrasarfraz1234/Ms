from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
import pandas as pd
import mysql.connector

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}!, Your account is created successfully...')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    return render(request, 'users/profile.html')

@login_required()
def home(request):

    chapter_name = request.POST.get('chapter_name', '')

    book_name = ''
    if(chapter_name!=''):
        dum = chapter_name.split(",,,")
        chapter_name = dum[0]
        book_name = dum[1]

    # Database Connectivity
    myDb = mysql.connector.connect(host="localhost", user="root", passwd="fb834946220403", database="sihah_al_sittah")
    myCursor = myDb.cursor()

    chapters_bukhari = []
    chapters_muslim = []
    chapters_tirmizi = []
    chapters_nesai = []
    chapters_abuDaud = []
    chapters_ibnMaja = []
    Ahadith_chapter = []


    query1 = "select distinct chapter_arabic from bukhari_book;"
    myCursor.execute(query1)
    result1 = myCursor.fetchall()
    for i in range(len(result1)):
        dum = {"chapter_name": result1[i][0]}
        chapters_bukhari.append(dum)

    query2 = "select distinct chapter_arabic from muslim_book;"
    myCursor.execute(query2)
    result2 = myCursor.fetchall()
    for i in range(len(result2)):
        dum = {"chapter_name": result2[i][0]}
        chapters_muslim.append(dum)

    query3 = "select distinct chapter_arabic from tirmizi_book"
    myCursor.execute(query3)
    result3 = myCursor.fetchall()
    for i in range(len(result3)):
        dum = {"chapter_name": result3[i][0]}
        chapters_tirmizi.append(dum)

    query4 = "select distinct chapter_arabic from nesai_book;"
    myCursor.execute(query4)
    result4 = myCursor.fetchall()
    for i in range(len(result4)):
        dum = {"chapter_name": result4[i][0]}
        chapters_nesai.append(dum)

    query5 = "select distinct chapter_arabic from abuDaud_book;"
    myCursor.execute(query5)
    result5 = myCursor.fetchall()
    for i in range(len(result5)):
        dum = {"chapter_name": result5[i][0]}
        chapters_abuDaud.append(dum)

    query6 = "select distinct chapter_arabic from ibnMaja_book;"
    myCursor.execute(query6)
    result6 = myCursor.fetchall()
    for i in range(len(result6)):
        dum = {"chapter_name": result6[i][0]}
        chapters_ibnMaja.append(dum)

    if(chapter_name!='' and book_name!=''):
        query7 = "select arabic_hadith from "+book_name+" where chapter_arabic = '"+chapter_name+"';"
        myCursor.execute(query7)
        result7 = myCursor.fetchall()
        for i in range(len(result7)):
            Ahadith_chapter.append(result7[i][0])
    #print(Ahadith_chapter)
    params = {'chapters_bukhari': chapters_bukhari, 'chapters_muslim': chapters_muslim, 'chapters_tirmizi': chapters_tirmizi, 'chapters_nesai': chapters_nesai, 'chapters_abuDaud': chapters_abuDaud, 'chapters_ibnMaja': chapters_ibnMaja, 'Ahadith_chapter': Ahadith_chapter, 'book_name': book_name, 'chapter_name': chapter_name}
    return render(request, 'users/home.html', params)

def index(request):
    return render(request, 'users/index.html')

def mlSubmit(request):
    # Getting hadith text from webpage
    getHadithText = request.POST.get('hadithText', '')

    getHadithText = str(getHadithText)

    # Removing before and after white spaces
    hadithText = getHadithText.strip()

    # Variable that contains without_Aeraab hadithText
    withoutAerabText = ""

    # Aeraab Remover Code
    for i in range(len(hadithText)):
        no = ord(hadithText[i])
        if (
                no == 1614 or no == 1615 or no == 1616 or no == 1618 or no == 1617 or no == 1612 or no == 1613 or no == 1611):
            continue
        else:
            withoutAerabText += hadithText[i]

    bookChapinfo = request.POST.get('sub_button1', '')

    book_name = ''
    chapter_name = ''
    if (bookChapinfo != ''):
        dum = bookChapinfo.split(",,,")
        book_name = dum[0]
        chapter_name = dum[1]

    from sklearn import model_selection
    import pandas as pd
    import numpy as np
    import collections

    df = pd.read_csv("C:/Users/iammu/OneDrive/Desktop/PyhtonProgram/DataForMachineLearning.csv", encoding="utf-8")

    df1 = pd.read_csv("C:/Users/iammu/OneDrive/Desktop/PyhtonProgram/DataForMachineLearningV1.csv", encoding="utf-8")

    arabicIsnads = df1.arabic_hadith
    arabicIsnads = list(arabicIsnads)

    arabicGrades = df1.arabic_grade
    arabicGrades = list(arabicGrades)

    from nltk.corpus import stopwords

    def clean_text(text):
        text1 = text
        WithoutAhrabTxt = ""
        finalText = ' '

        for i in range(len(text1)):
            no = ord(text1[i])
            if (
                    no == 1614 or no == 1615 or no == 1616 or no == 1618 or no == 1617 or no == 1612 or no == 1613 or no == 1611):
                continue
            else:
                WithoutAhrabTxt += text1[i]

        WordReplace = ["حدثني", "وحدثنا", "حدثنا", "نحوه", "قال", "فقال", "سمعت", "يقول", "سمع", "أخبرني", "مولى",
                       "أخبرنا", "اخبرنا", "قالت", ":", "قالا", "جميعا", "وحدثني", "في حديثه", "تابعه", "اخبرني",
                       "حريثا", "يحدث", "حدثتنا", "حفص", "لفظ", "وهذا", "روى", "متهما", "صاحب", "قيل", "كان", "حدثه",
                       "واحد", "تلا", "إنما", "لعن", 'كان', "رواية", "قال", "عليا", "حدثته", "أنها", "‏.‏", "وقد",
                       "روي", "أخبره", "كنت", "وأخبرني"]
        RA_List = ['رضى الله عنهما', 'رضى الله عنه', 'رضى الله عنها', 'رضي الله عنه', "ح‏.‏ "]

        STOPWORDS = set(stopwords.words('arabic'))
        dummy = list(STOPWORDS)
        tokenList = WithoutAhrabTxt.split()
        newList = [word for word in tokenList if word not in STOPWORDS]
        newtext = ' '.join(newList)

        finalTokenList = newtext.split("،")

        for i in range(len(finalTokenList)):
            finalTokenList[i] = finalTokenList[i].strip()

            for j in range(len(RA_List)):
                if (finalTokenList[i].__contains__(RA_List[j])):
                    finalTokenList[i] = finalTokenList[i].replace(RA_List[j], "")

            finalTokenList[i] = finalTokenList[i].strip()

        for i in range(len(finalTokenList)):
            for j in range(len(WordReplace)):
                if (finalTokenList[i].__contains__(WordReplace[j])):
                    finalTokenList[i] = finalTokenList[i].replace(WordReplace[j], "")
                    finalTokenList[i] = finalTokenList[i].strip()

        return (finalTokenList)

    dum = df['arabic_isnad'].apply(clean_text)
    dum = list(dum)

    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.metrics import accuracy_score

    df.head()
    X = df.iloc[:, 1].values

    Y = df.iloc[:, -1].values

    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.05)

    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfTransformer

    lr = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression()),
                   ])

    lr.fit(X_train, Y_train)
    y_pred = lr.predict(X_test)

    accuracyLg = accuracy_score(y_pred, Y_test)

    from sklearn.naive_bayes import MultinomialNB

    naivebayes = Pipeline([('vect', CountVectorizer()),
                           ('tfidf', TfidfTransformer()),
                           ('clf', MultinomialNB()),
                           ])
    naivebayes.fit(X_train, Y_train)

    y_pred1 = naivebayes.predict(X_test)

    accuracyNb = accuracy_score(y_pred, Y_test)

    ind = arabicIsnads.index(getHadithText)
    resultStatus = arabicGrades[ind]
    params = {'hadithText': withoutAerabText, 'logisticPred': accuracyLg, 'naiveBayesPred': accuracyNb, 'resultStatus': resultStatus}
    return render(request, 'users/mlSubmit.html',params)


def ml(request):
    chapter_name = request.POST.get('chapter_name', '')

    book_name = ''
    if (chapter_name != ''):
        dum = chapter_name.split(",,,")
        chapter_name = dum[0]
        book_name = dum[1]

    # Database Connectivity
    myDb = mysql.connector.connect(host="localhost", user="root", passwd="fb834946220403", database="sihah_al_sittah")
    myCursor = myDb.cursor()

    chapters_bukhari = []
    chapters_muslim = []
    chapters_tirmizi = []
    chapters_nesai = []
    chapters_abuDaud = []
    chapters_ibnMaja = []
    Ahadith_chapter = []

    query1 = "select distinct chapter_arabic from bukhari_book;"
    myCursor.execute(query1)
    result1 = myCursor.fetchall()
    for i in range(len(result1)):
        dum = {"chapter_name": result1[i][0]}
        chapters_bukhari.append(dum)

    query2 = "select distinct chapter_arabic from muslim_book;"
    myCursor.execute(query2)
    result2 = myCursor.fetchall()
    for i in range(len(result2)):
        dum = {"chapter_name": result2[i][0]}
        chapters_muslim.append(dum)

    query3 = "select distinct chapter_arabic from tirmizi_book"
    myCursor.execute(query3)
    result3 = myCursor.fetchall()
    for i in range(len(result3)):
        dum = {"chapter_name": result3[i][0]}
        chapters_tirmizi.append(dum)

    query4 = "select distinct chapter_arabic from nesai_book;"
    myCursor.execute(query4)
    result4 = myCursor.fetchall()
    for i in range(len(result4)):
        dum = {"chapter_name": result4[i][0]}
        chapters_nesai.append(dum)

    query5 = "select distinct chapter_arabic from abuDaud_book;"
    myCursor.execute(query5)
    result5 = myCursor.fetchall()
    for i in range(len(result5)):
        dum = {"chapter_name": result5[i][0]}
        chapters_abuDaud.append(dum)

    query6 = "select distinct chapter_arabic from ibnMaja_book;"
    myCursor.execute(query6)
    result6 = myCursor.fetchall()
    for i in range(len(result6)):
        dum = {"chapter_name": result6[i][0]}
        chapters_ibnMaja.append(dum)

    if (chapter_name != '' and book_name != ''):
        query7 = "select arabic_hadith from " + book_name + " where chapter_arabic = '" + chapter_name + "';"
        myCursor.execute(query7)
        result7 = myCursor.fetchall()
        for i in range(len(result7)):
            Ahadith_chapter.append(result7[i][0])
    # print(Ahadith_chapter)
    params = {'chapters_bukhari': chapters_bukhari, 'chapters_muslim': chapters_muslim,
              'chapters_tirmizi': chapters_tirmizi, 'chapters_nesai': chapters_nesai,
              'chapters_abuDaud': chapters_abuDaud, 'chapters_ibnMaja': chapters_ibnMaja,
              'Ahadith_chapter': Ahadith_chapter, 'book_name': book_name, 'chapter_name': chapter_name}

    return render(request, 'users/ml.html', params)

def submit(request):

        # Getting hadith text from webpage
        getHadithText = request.POST.get('text', '')

        getHadithText = str(getHadithText)
        bookChapinfo = request.POST.get('sub_button', '')

        book_name = ''
        chapter_name = ''
        if(bookChapinfo!=''):
            dum = bookChapinfo.split(",,,")
            book_name = dum[0]
            chapter_name = dum[1]
        print(book_name,chapter_name)
        # Removing before and after white spaces
        hadithText = getHadithText.strip()

    # tryError = ''
    # try:
    #     # Database Connectivity
    #     myDb = mysql.connector.connect(host="localhost", user="root", passwd="fb834946220403",database="sihah_al_sittah")
    #     myCursor = myDb.cursor()
    #
    #     query11 = "select arabic_isnad from "+book_name+" where chapter_arabic = '" + chapter_name + "' and arabic_hadith = '"+hadithText+"';"
    #     myCursor.execute(query11)
    #     result11 = myCursor.fetchall()
    #     print(len(result11))
    #     hadithIsnad = ''
    #     if(len(result11)==0):
    #         print(1/0)
    #     else:
    #
    #
    #         hadithIsnad = result11[0][0]
    #
    #         from nltk.corpus import stopwords
    #
    #         # text1=df2.Arabic_Isnad[0]
    #
    #
    #         # text="حَدَّثَنَا عَمْرُو بْنُ خَالِدٍ، قَالَ حَدَّثَنَا اللَّيْثُ، عَنْ يَزِيدَ، عَنْ أَبِي الْخَيْرِ، عَنْ عَبْدِ اللَّهِ بْنِ عَمْرٍو ـ رضى الله عنهما ـ"
    #         text1 = hadithIsnad
    #         withoutAerabText = ""
    #         finalText = ' '
    #
    #         for i in range(len(text1)):
    #             no = ord(text1[i])
    #             if (no == 1614 or no == 1615 or no == 1616 or no == 1618 or no == 1617 or no == 1612 or no == 1613 or no == 1611):
    #                 continue
    #             else:
    #                 withoutAerabText += text1[i]
    #
    #         WordReplace = ["حدثني", "وحدثنا", "حدثنا", "نحوه", "قال", "فقال", "سمعت", "يقول", "سمع", "أخبرني",
    #                        "مولى", "أخبرنا", "اخبرنا", "قالت", ":", "قالا", "جميعا", "وحدثني", "في حديثه", "تابعه",
    #                        "اخبرني", "حريثا", "يحدث", "حدثتنا", "حفص", "لفظ", "وهذا", "روى", "متهما", "صاحب", "قيل",
    #                        "كان", "حدثه", "واحد", "تلا", "إنما", "لعن", 'كان', "رواية", "قال", "عليا", "حدثته",
    #                        "أنها", "‏.‏", "وقد", "روي", "أخبره", "كنت", "وأخبرني"]
    #         RA_List = ['رضى الله عنهما','رضى الله عنه','رضى الله عنها','رضي الله عنه',"ح‏.‏ "]
    #
    #         STOPWORDS = set(stopwords.words('arabic'))
    #         dummy = list(STOPWORDS)
    #         tokenList = withoutAerabText.split()
    #         newList = [word for word in tokenList if word not in STOPWORDS]
    #         newtext = ' '.join(newList)
    #
    #         finalTokenList = newtext.split("،")
    #
    #         for i in range(len(finalTokenList)):
    #             finalTokenList[i] = finalTokenList[i].strip()
    #
    #             for j in range(len(RA_List)):
    #                 if (finalTokenList[i].__contains__(RA_List[j])):
    #                     finalTokenList[i] = finalTokenList[i].replace(RA_List[j], "")
    #
    #             finalTokenList[i] = finalTokenList[i].strip()
    #
    #         for i in range(len(finalTokenList)):
    #             for j in range(len(WordReplace)):
    #                 if (finalTokenList[i].__contains__(WordReplace[j])):
    #                     finalTokenList[i] = finalTokenList[i].replace(WordReplace[j], "")
    #                     finalTokenList[i] = finalTokenList[i].strip()
    #
    #
    #
    #         # dumForBukhari= df3['Arabic_Isnad'].apply(clean_text)
    #
    #         narratorsNameList = finalTokenList
    #         narratorsNameList = list(narratorsNameList)
    #         print(narratorsNameList)
    #
    #
    #
    #
    # except:
    #     tryError = "Exception Occured"

        # keys = ["وحدثنا", "حدثنا", "نحوه", "عن", "قال", "فقال", "سمعت", "يقول", "أنه", "سمع", "أخبرني", "مولى", "أن",
        #                "أخبرنا", "في حديثه", "تابعه", "انه", "اخبرني", "وأخبرني"]


        # Variable that contains without_Aeraab hadithText
        withoutAerabText = ""

        # Aeraab Remover Code
        for i in range(len(hadithText)):
            no = ord(hadithText[i])
            if (no == 1614 or no == 1615 or no == 1616 or no == 1618 or no == 1617 or no == 1612 or no == 1613 or no == 1611):
                continue
            else:
                withoutAerabText += hadithText[i]

        # Split hadithText into words on the basis of space and create a list
        tokens_WithoutAerabText = withoutAerabText.split(" ")

        # Words that replace from hadithText
        WordReplace = ["حدثني", "في" , "أنها" , "وحدثنا", "حدثنا", "أنبأنا","ـ", "نحوه", "عن", "قال", "فقال", "سمعت", "يقول", "أنه", "سمع", "أخبرني",
                       "مولى", "أخبرنا", "اخبرنا", "سال", "أن", "قالت", ":", "في حديثه", "تابعه", "أخبره", "ان", "انه",
                       "اخبرني", "وحدثني", "وأخبرني"]

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
        prophetNamesReplacerList = ["رسول الله صلى الله عليه وسلم","النبي ـ صلى الله عليه وسلم" ,"النبي صلى الله عليه وسلم", "يا رسول الله",
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
    # finally:
        # List of all Narrator's Info of given hadith that are present in our DataBase
        finalInfoList_Narrators = []

        notFoundNarrators = ''

        # Cross Check of Narrators_Names with Database
        for i in range(len(narratorsNameList)):
            # Database Connectivity
            myDb = mysql.connector.connect(host="localhost",user="root",passwd="fb834946220403",database="scholar_database")
            myCursor = myDb.cursor()
            # add
            narratorsNameList[i] = narratorsNameList[i].strip()
            if (len(narratorsNameList[i]) != 0):
                if (narratorsNameList[i][-1] == "،"):
                    narratorsNameList[i] = narratorsNameList[i].replace("،", "")

            narratorsNameList[i] = narratorsNameList[i].replace('''"''', '')
            narratorsNameList[i] = narratorsNameList[i].replace("ـ رضى الله عنها ـ", "")
            narratorsNameList[i] = narratorsNameList[i].replace("ـ رضى الله عنهما ـ", "")
            narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنها", "")
            narratorsNameList[i] = narratorsNameList[i].replace("رضي الله عنه", "")
            narratorsNameList[i] = narratorsNameList[i].replace("على المنبر", "")
            narratorsNameList[i] = narratorsNameList[i].strip()


            # Query for checking Narrator's Info in scholars table
            query = '''select * from scholars where name like "''' + narratorsNameList[i] + '''";'''
            myCursor.execute(query)
            result = myCursor.fetchall()
            # Check if Narrator's Info found in scholars table
            if (len(result) != 0):
                finalInfoList_Narrators.append(result[0])
            # Check if Narrator's Info not found in scholars table
            if (len(result) == 0):
                # Query for checking Narrator's Info in scholar_other_names table
                query = '''select * from scholar_other_names
                          where name like "''' + narratorsNameList[i] + '''";'''
                myCursor.execute(query)
                result = myCursor.fetchall()
                # Check if Narrator's Info found in scholar_other_names table
                if (len(result) != 0):
                    finalInfoList_Narrators.append(result[0])
                else:
                    notFoundNarrators = "Some narrators Not Found in our database"
        # print(finalInfoList_Narrators)
        # Dummy List that contains Refined narratorsNameList i.e. Removing empty cells/values
        dummyNarratorsNameList = []

        # Code for Removing Empty values from narratorsNameList
        for i in range(len(narratorsNameList)):
            if (len(narratorsNameList[i].strip()) != 0):
                dummyNarratorsNameList.append(narratorsNameList[i])

        # Assigning dummyNarratorsNameList back to narratorsNameList
        narratorsNameList = dummyNarratorsNameList

        # List of all Narrator's Ids of given hadith that are present in our DataBase
        finalIdList_Narrators = []

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

        # List that contains dictionary of scholar_ids and scholar_names used/present in our given hadith and DataBase also
        checkList = []

        # Code for combining Scholar_Ids and Scholar_Names in a Dictionary and storing this dictionary in checkList
        for i in range(len(finalInfoList_Narrators)):
            if (len(finalInfoList_Narrators[i]) == 8):
                dum = finalInfoList_Narrators[i][0]
                dum1 = finalInfoList_Narrators[i][1]
                dumDict = {'id': dum, 'name': dum1}
                checkList.append(dumDict)
                dum1 = ''
                dum = ''
                dumDict = {}

            if (len(finalInfoList_Narrators[i]) == 3):
                dum = finalInfoList_Narrators[i][1]
                dum1 = finalInfoList_Narrators[i][2]
                dumDict = {'id': dum, 'name': dum1}
                checkList.append(dumDict)
                dum1 = ''
                dum = ''
                dumDict = {}

        # List that contains Status_of_Narrators of Given Hadith
        statusList = []

        # Code for Extracting Status_of_Narrators from Database using Scholar_Ids and storing in statusList
        for i in range(len(finalIdList_Narrators)):
            query = "select status from scholars where id = " + str(finalIdList_Narrators[i]) + ";"

            myCursor.execute(query)

            result = myCursor.fetchall()

            for j in range(len(result)):
                statusList.append(result[j][0])

        # List that contains dictionary at each index in which we categorized Scholars According to their status
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

        # List that contains all the Keys of Narrators of Given Hadith from sanadOrder
        extractingKeysFromSanadOrder = []

        # Code for Extracting all the Keys of Narrators from sanadOrder based on their status
        for i in range(len(statusList)):
            for j in range(len(sanadOrder)):
                if (statusList[i] == sanadOrder[j].get("status")):
                    extractingKeysFromSanadOrder.append(sanadOrder[j].get('key'))

        # Variable that contains the Reason According to the Nisbat of the Hadith
        reasonAccordingToNisbat = ""
        # Variable that contains the Type According to the Nisbat of the Hadith
        typeAccordingToNisbat = ""

        if (1 in extractingKeysFromSanadOrder):
            typeAccordingToNisbat = "Given Hadith is Murfoo."
            reasonAccordingToNisbat = "Because it is narrated from/by Prophet Muhammad (P.B.U.H)."
        elif (2 in extractingKeysFromSanadOrder):
            typeAccordingToNisbat = "Given Hadith is Mauqoof."
            reasonAccordingToNisbat = "Because it is narrated from/by Companion (R.A)."
        elif (3 in extractingKeysFromSanadOrder):
            typeAccordingToNisbat = "Given Hadith is Maqtoo."
            reasonAccordingToNisbat = "Because it is narrated from/by Follower(Tabi')."
        elif (len(narratorsNameList) == 0):
            typeAccordingToNisbat = ""
            reasonAccordingToNisbat = "There is no Narrator in the given Hadith."
        else:
            typeAccordingToNisbat = "Given Hadith does not exist in this category."
            reasonAccordingToNisbat = "Because it is neither narrated from/by Prophet Muhammad (P.B.U.H) nor Companion (R.A) nor Follower(Tabi')."

        # List that contains Narrator's Names for showing them on Submit Page
        showNarratorsList = []
        for i in range(len(checkList)):
            dic = {'name': checkList[i].get("name"), 'id': "" + str(checkList[i].get("id"))}
            showNarratorsList.append(dic)

        # if(notFoundNarrators!=''):
        #     showNarratorsList.append({'name': notFoundNarrators, 'id':0})
        # print(finalIdList_Narrators)

        myDb = mysql.connector.connect(host="localhost",user="root",passwd="fb834946220403",database="scholar_database")
        myCursor = myDb.cursor()

        reason_Musnad = ""
        reason_Sahih = ""
        reason_Zaeef = ""
        reason_Munqate = ""
        reason_Muedal = ""
        reason_Muallaq = ""
        reason_Mursal = ""

        counter_Musnad = 0
        print(finalIdList_Narrators)

        for i in range(len(finalIdList_Narrators)):
            if (i <= len(finalIdList_Narrators) - 2):
                query = "select teacher_id from teachers where scholar_id = " + str(finalIdList_Narrators[i]) + ";"

                myCursor.execute(query)

                result = myCursor.fetchall()

                teacher_ids = []
                for j in range(len(result)):
                    teacher_ids.append(result[j][0])

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
                                reason_Zaeef = "The given hadith is Zaeef."
                                reason_Muedal = "The given hadith is Muedal because two consecutive narrators are missing."

                            else:
                                reason_Zaeef = "The given hadith is Zaeef."
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
                    reason_Zaeef="The given hadith is Zaeef."
                else:
                    reason_Sahih = "The given hadith is also Sahih."
            else:
                scholarsStatus = []
                for i in range(len(finalIdList_Narrators)):
                    query = "select Jarah_Taadeel from scholars where id = " + str(finalIdList_Narrators[i]) + ";"

                    myCursor.execute(query)

                    result = myCursor.fetchall()

                    scholarsStatus.append(result[0][0])

                if ("Zaeef" in scholarsStatus):
                    reason_Zaeef="The given hadith is Zaeef."
                else:
                    reason_Sahih = "The given hadith is Sahih."

        if (len(finalIdList_Narrators) == 1):
            if (1 in finalIdList_Narrators):
                reason_Zaeef = "The given hadith is Zaeef."
                reason_Muallaq = "The given hadith is Muallaq because whole chain of narrators is missing."
        print(extractingKeysFromSanadOrder)
        if ((extractingKeysFromSanadOrder[-1] == 1) and (extractingKeysFromSanadOrder[-2] == 3)):
            reason_Mursal = "The given hadith is Mursal because Follower(Tabi') is directly narrated from Prophet (صلی اللہ علیہ وآلہ وسلم)."


        params = {'hadithText': withoutAerabText, 'list': showNarratorsList, 'typeAccordingToNisbat': typeAccordingToNisbat,
                  'reasonAccordingToNisbat': reasonAccordingToNisbat, 'reason_Musnad': reason_Musnad, 'reason_Sahih': reason_Sahih,
                  'reason_Zaeef': reason_Zaeef, 'reason_Munqate': reason_Munqate, 'reason_Muedal': reason_Muedal, 'reason_Muallaq': reason_Muallaq,
                  'reason_Mursal': reason_Mursal}

        return render(request, 'users/submit.html', params)

def Info(request):
    narrator_id = request.POST.get('narrator_id', '')
    myDb = mysql.connector.connect(host="localhost",user="root",passwd="fb834946220403",database="scholar_database")
    myCursor = myDb.cursor()

    # Query to GET Name of Narrator
    query1 = '''select name from scholars where id=''' + narrator_id+ ''';'''
    myCursor.execute(query1)
    result1 = myCursor.fetchall()
    narrator_name = ''
    for i in result1:
        narrator_name = narrator_name + i[0]

    # Query to GET Status of Narrator
    query2 = '''select status from scholars where id=''' + narrator_id + ''';'''
    myCursor.execute(query2)
    result2 = myCursor.fetchall()
    narrator_status = ''
    for i in result2:
        narrator_status = narrator_status + i[0]

    # Query to GET Full_Name of Narrator
    query3 = '''select full_name from scholars where id=''' + narrator_id + ''';'''
    myCursor.execute(query3)
    result3 = myCursor.fetchall()
    narrator_full_name = ''
    for i in result3:
        narrator_full_name = narrator_full_name + i[0]

    # Query to GET Parents of Narrator
    query4 = '''select parents from scholars where id=''' + narrator_id + ''';'''
    myCursor.execute(query4)
    result4 = myCursor.fetchall()
    narrator_parents = ''
    for i in result4:
        narrator_parents = narrator_parents + i[0]
    #Check for 'nan' values
    if(narrator_parents=='nan'):
        narrator_parents = "No Data Available"

    # Query to GET Siblings of Narrator
    query5 = '''select name from siblings where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query5)
    result5 = myCursor.fetchall()
    narrator_siblings = ""
    for i in range(len(result5)):
        if (i == len(result5) - 1):
            narrator_siblings = narrator_siblings + result5[i][0].strip()
        else:
            narrator_siblings = narrator_siblings + result5[i][0].strip() + ", "
    # Check for 'nan' values
    if (narrator_siblings == "nan"):
        narrator_siblings = "No Data Available / This Scholar has no siblings"

    # Query to GET date_of_birth_place of Narrator
    query6 = '''select date_of_birth_place from scholars where id=''' + narrator_id + ''';'''
    myCursor.execute(query6)
    result6 = myCursor.fetchall()
    narrator_date_of_birth_place = ''
    for i in result6:
        narrator_date_of_birth_place = narrator_date_of_birth_place + i[0]
    # Check for 'nan' values
    if (narrator_date_of_birth_place == 'nan'):
        narrator_date_of_birth_place = "No Data Available"

    # Query to GET date_of_death_place of Narrator
    query7 = '''select date_of_death_place from scholars where id=''' + narrator_id + ''';'''
    myCursor.execute(query7)
    result7 = myCursor.fetchall()
    narrator_date_of_death_place = ''
    for i in result7:
        narrator_date_of_death_place = narrator_date_of_death_place + i[0]
    # Check for 'nan' values
    if (narrator_date_of_death_place == 'nan'):
        narrator_date_of_death_place = "No Data Available"

    # Query to GET place_of_stays of Narrator
    query8 = '''select name from place_of_stays where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query8)
    result8 = myCursor.fetchall()
    narrator_place_of_stays = ''
    for i in range(len(result8)):
        if (i == len(result8) - 1):
            narrator_place_of_stays = narrator_place_of_stays + result8[i][0].strip()
        else:
            narrator_place_of_stays = narrator_place_of_stays + result8[i][0].strip() + "/"
    # Check for 'nan' values
    if (narrator_place_of_stays == 'nan'):
        narrator_place_of_stays = "No Data Available"

    # Query to GET area_of_intrest of Narrator
    query9 = '''select name from area_of_intrest where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query9)
    result9 = myCursor.fetchall()
    narrator_area_of_intrest = ""
    for i in range(len(result9)):
        if (i == len(result9) - 1):
            narrator_area_of_intrest = narrator_area_of_intrest + result9[i][0].strip()
        else:
            narrator_area_of_intrest = narrator_area_of_intrest + result9[i][0].strip() + ", "
    # Check for 'nan' values
    if (narrator_area_of_intrest == "nan"):
        narrator_area_of_intrest = "No Data Available"

    # Query to GET spouses of Narrator
    query10 = '''select name from spouses where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query10)
    result10 = myCursor.fetchall()
    narrator_spouses = ""
    for i in range(len(result10)):
        if (i == len(result10) - 1):
            narrator_spouses = narrator_spouses + result10[i][0].strip()
        else:
            narrator_spouses = narrator_spouses + result10[i][0].strip() + ", "
    # Check for 'nan' values
    if (narrator_spouses == "nan"):
        narrator_spouses = "No Data Available / This Scholar has no spouse(s)"

    # Query to GET childrens of Narrator
    query11 = '''select name from childrens where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query11)
    result11 = myCursor.fetchall()
    narrator_childrens = ""
    for i in range(len(result11)):
        if (i == len(result11) - 1):
            narrator_childrens = narrator_childrens + result11[i][0].strip()
        else:
            narrator_childrens = narrator_childrens + result11[i][0].strip() + ", "
    # Check for 'nan' values
    if (narrator_childrens == "nan"):
        narrator_childrens = "No Data Available / This Scholar has no children(s)"

    # Query to GET teachers of Narrator
    query12 = '''select teacher_id from teachers where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query12)
    result12 = myCursor.fetchall()
    narrator_teachers = ""
    for i in range(len(result12)):
        # Check for 'nan' values
        if (result12[i][0] == 0):
            narrator_teachers = "No Data Available / This Scholar has no teacher(s)"
            break
        elif (i == len(result12) - 1):
            query13 = "select name from scholars where id=" + str(result12[i][0]) + ";"
            myCursor.execute(query13)
            result13 = myCursor.fetchall()

            narrator_teachers = narrator_teachers + result13[0][0].strip()
        else:
            query14 = "select name from scholars where id=" + str(result12[i][0]) + ";"
            myCursor.execute(query14)
            result14 = myCursor.fetchall()

            narrator_teachers = narrator_teachers + result14[0][0].strip() + ",  "

    # Query to GET students of Narrator
    query15 = '''select student_id from students where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query15)
    result15 = myCursor.fetchall()
    narrator_students = ""
    for i in range(len(result15)):
        # Check for 'nan' values
        if (result15[i][0] == 0):
            narrator_students = "No Data Available / This Scholar has no student(s)"
            break
        elif (i == len(result15) - 1):
            query16 = "select name from scholars where id=" + str(result15[i][0]) + ";"
            myCursor.execute(query16)
            result16 = myCursor.fetchall()

            narrator_students = narrator_students + result16[0][0].strip()
        else:
            query17 = "select name from scholars where id=" + str(result15[i][0]) + ";"
            myCursor.execute(query17)
            result17 = myCursor.fetchall()

            narrator_students = narrator_students + result17[0][0].strip() + ",  "

    # Query to GET tags of Narrator
    query18 = '''select tag_name from tags where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query18)
    result18 = myCursor.fetchall()
    narrator_tags = ""
    for i in range(len(result18)):
        if (i == len(result18) - 1):
            narrator_tags = narrator_tags + result18[i][0].strip()
        else:
            narrator_tags = narrator_tags + result18[i][0].strip() + ", "
    # Check for 'nan' values
    if (narrator_tags == "nan"):
        narrator_tags = "No Data Available"

    # Query to GET brief_biography of Narrator
    query19 = '''select biography from brief_biography where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query19)
    result19 = myCursor.fetchall()
    narrator_biography = ''
    for i in result19:
        narrator_biography = narrator_biography + i[0].strip()
    #Check for 'nan' values
    if(narrator_biography=='nan'):
        narrator_biography = "No Data Available"

    # Query to GET book_reference of Narrator
    query20 = '''select reference from book_reference where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query20)
    result20 = myCursor.fetchall()
    narrator_book_reference = ""
    for i in range(len(result20)):
        if (i == len(result20) - 1):
            narrator_book_reference = narrator_book_reference + result20[i][0].strip()
        else:
            narrator_book_reference = narrator_book_reference + result20[i][0].strip() + "\n"
    # Check for 'nan' values
    if (narrator_book_reference == 'nan'):
        narrator_book_reference = "No Data Available"

    # Query to GET scholar_other_names of Narrator
    query21 = '''select name from scholar_other_names where scholar_id=''' + narrator_id + ''';'''
    myCursor.execute(query21)
    result21 = myCursor.fetchall()
    narrator_other_names = ""
    for i in range(len(result21)):
        if (i == len(result21) - 1):
            narrator_other_names = narrator_other_names + result21[i][0].strip()
        else:
            narrator_other_names = narrator_other_names + result21[i][0].strip() + "\n"
    # Check for 'nan' values
    if (narrator_other_names == 'nan'):
        narrator_other_names = "No Data Available"

    print(narrator_id)
    params = {'narrator_name': narrator_name, 'narrator_status': narrator_status, 'narrator_full_name': narrator_full_name, 'narrator_parents': narrator_parents, 'narrator_siblings': narrator_siblings, 'narrator_date_of_birth_place': narrator_date_of_birth_place, 'narrator_date_of_death_place': narrator_date_of_death_place, 'narrator_place_of_stays': narrator_place_of_stays, 'narrator_area_of_intrest': narrator_area_of_intrest, 'narrator_spouses': narrator_spouses, 'narrator_childrens': narrator_childrens, 'narrator_teachers': narrator_teachers, 'narrator_students': narrator_students, 'narrator_tags': narrator_tags, 'narrator_biography': narrator_biography, 'narrator_book_reference': narrator_book_reference, 'narrator_other_names': narrator_other_names}
    return render(request, 'users/Info.html', params)