from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from mobileapp.models import Register
from django.contrib import messages
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


Registration = 'register.html'
def register(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        age = request.POST['Age']
        contact = request.POST['contact']

        print(Name, email, password, conpassword, age, contact)
        if password == conpassword:
            user = User(email=email, password=password)
            # user.save()
            return render(request, 'login.html')
        else:
            msg = 'Register failed!!'
            return render(request, Registration,{msg:msg})

    return render(request, Registration)

# Login Page 
def login(request):
    if request.method == 'POST':
        lemail = request.POST['email']
        lpassword = request.POST['password']

        d = User.objects.filter(email=lemail, password=lpassword).exists()
        print(d)
        return redirect(userhome)
    else:
        return render(request, 'login.html')

def userhome(request):
    return render(request,'userhome.html')

def view(request):
    global df
    if request.method=='POST':
        g = int(request.POST['num'])
        df = pd.read_csv('20230329093832Mobile-Addiction-.csv')
        df.drop(['Full Name :','Timestamp'], axis=1, inplace=True)
        col = df.head(g).to_html()
        return render(request,'view.html',{'table':col})
    return render(request,'view.html')


def module(request):
    global df,x_train, x_test, y_train, y_test
    # df = pd.read_csv('20230329093832Mobile-Addiction-.csv')
    # **fill a Null Values**
    col = df[['Gender :',
        'Do you use your phone to click pictures of class notes?',
        'Do you buy books/access books from your mobile?',
        "Does your phone's battery last a day?",
        "When your phone's battery dies out, do you run for the charger?",
        'Do you worry about losing your cell phone?',
        'Do you take your phone to the bathroom?',
        'Do you use your phone in any social gathering (parties)?',
        'Do you often check your phone without any notification? ',
        'Do you check your phone just before going to sleep/just after waking up?',
        'Do you keep your phone right next to you while sleeping?',
        'Do you check emails, missed calls, texts during class time? ',
        'Do you find yourself relying on your phone when things get awkward?',
        'Are you on your phone while watching TV or eating food?',
        'Do you have a panic attack if you leave your phone elsewhere?',
        "You don't mind responding to messages or checking your phone while on date? ",
        'For how long do you use your phone for playing games?',
        'Can you live a day without phone ? ',
        'whether you are addicted to phone?']]
    # filling a null Values applying a ffill method
    # df.drop('Full Name :', axis=1, inplace=True)
    for i in col:
        df[i].fillna(method='ffill',inplace=True)
    df['Can you live a day without phone ? '].fillna(method='bfill',inplace=True)
    df['whether you are addicted to phone?'].fillna(method='bfill',inplace=True)
    # Apply The Label Encoding
    le = LabelEncoder()
    for i in col:
        df[i]=le.fit_transform(df[i])
    # Delete The unknown column
    # df.drop('Timestamp', axis = 1,inplace = True)
    x = df.drop(['whether you are addicted to phone?'], axis = 1) 
    y = df['whether you are addicted to phone?']
    Oversample = RandomOverSampler(random_state=72)
    x_sm, y_sm = Oversample.fit_resample(x[:100],y[:100])
    x_train, x_test, y_train, y_test = train_test_split(x_sm, y_sm, test_size = 0.3, random_state= 72)
    if request.method=='POST':
        model = request.POST['algo']

        if model == "1":
            re = RandomForestClassifier(random_state=72)
            re.fit(x_train,y_train)
            re_pred = re.predict(x_test)
            ac = accuracy_score(y_test,re_pred)
            ac
            msg='Accuracy of RandomForest : ' + str(ac)
            return render(request,'module.html',{'msg':msg})
        elif model == "2":
            de = DecisionTreeClassifier()
            de.fit(x_train,y_train)
            de_pred = de.predict(x_test)
            ac1 = accuracy_score(y_test,de_pred)
            ac1
            msg='Accuracy of Decision tree : ' + str(ac1)
            return render(request,'module.html',{'msg':msg})
        elif model == "3":
            le = LogisticRegression()
            le.fit(x_train,y_train)
            le_pred = le.predict(x_test)
            ac2 = accuracy_score(y_test,le_pred)
            msg='Accuracy of LogisticRegression : ' + str(ac2)
            return render(request,'module.html',{'msg':msg})
    return render(request,'module.html')


def getsuggestion(l):
    suggset = ""
    
    sublist = l[0]

    # Adding data based on integer values (0 or 1)
    if sublist[5] == 1:
        suggset += "\n  ** Don't take your phone to the washroom \n"

    if sublist[7] == 1:
        suggset += "\n  ** Don't use your phone during social gatherings \n"

    if sublist[9] == 1:
        suggset += "\n  ** Don't use your phone before sleeping or after waking up \n"

    if sublist[11] == 1:
        suggset += "\n  ** Don't use your phone during classes \n"

    if sublist[16] == 1:
        suggset += "\n  **  Reduce time for playing games \n"
       

    return suggset


def prediction(request):
    global df,x_train, x_test, y_train, y_test

    if request.method == 'POST':
        
        b = float(request.POST['f2'])
        c = float(request.POST['f3'])
        d = float(request.POST['f4'])
        e = float(request.POST['f5'])
        f = float(request.POST['f6'])
        g = float(request.POST['f7'])
        h = float(request.POST['f8'])
        i = float(request.POST['f9'])
        j = float(request.POST['f10'])
        k = float(request.POST['f11'])
        l = float(request.POST['f12'])
        m = float(request.POST['f13'])
        n = float(request.POST['f14'])
        o = float(request.POST['f15'])
        p = float(request.POST['f16'])
        q = float(request.POST['f17'])
        r = float(request.POST['f18'])
        s = float(request.POST['f19'])

       
        
        l = [[b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s]]

        suggestion = getsuggestion(l)

        de = DecisionTreeClassifier()
        de.fit(x_train,y_train)
        pred = de.predict(l)
        if pred == 0:
            msg = 'Not addicted'
        elif pred == 1:
            msg = 'Maybe addicted'
        elif pred == 2:
         
            msg = "--------------------------------You are addicted---------------------------------\n"  +  "\n*****************Steps you can follow*************\n" + suggestion

            
                
         
        return render(request,'prediction.html',{'msg':msg})

    return render(request,'prediction.html')