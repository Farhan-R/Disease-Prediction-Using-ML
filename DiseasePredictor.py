import pypyodbc as odbc
from tkinter import *
import ctypes
from tkinter import messagebox
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ctypes.windll.shcore.SetProcessDpiAwareness(2)

DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-34I8OUD'

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Trust_Connection=yes;
"""
# Connecting to Database
try:
    conn = odbc.connect(conn_string, autocommit=True)
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()
else:
    print("DATABASE CONNECTED")
    cursor = conn.cursor()


class LoginScreen:
    main_screen = Tk()

    def __init__(self):
        self.user_name = StringVar()
        self.password = StringVar()
        self.user_logged_in = False

    def login(self):
        if self.user_name.get() == "" or self.password.get() == "":
            messagebox.showerror("Error!", "Enter User Name And Password", parent=self.main_screen)
        else:
            try:
                cursor.execute("USE DBMS_USERS_DB")
                cursor.commit()
                cursor.execute("SELECT * FROM USER_DETAILS WHERE UserName='%s' AND Password='%s'"
                               % (self.user_name.get(), self.password.get()))
                cursor.commit()
                row = cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error!", "Invalid User Name Or Password", parent=self.main_screen)
                else:
                    messagebox.showinfo("Success", "Successfully Login", parent=self.main_screen)
                    logged_in_user = Dashboard(self.user_name.get(), self.password.get())
                    logged_in_user.account_screen()

            except Exception as err:
                print(err)
                cursor.rollback()
                print("SELECT Query execution Failed!")

    def login_screen(self):
        self.main_screen.title("LOGIN WINDOW")
        self.main_screen.geometry("900x600")
        background_img = PhotoImage(file="images/image1.png")

        # Create a Canvas
        my_canvas = Canvas(self.main_screen, width=800, height=500)
        my_canvas.pack(fill="both", expand=True)

        my_canvas.create_image(0, 0, image=background_img, anchor=NW)
        my_canvas.create_text(400, 50, text="DISEASE PREDICTION USING MACHINE LEARNING", font=("Constantia", 15))
        my_canvas.create_text(140, 220, text="USERNAME: ", font=("Arabic Transparent", 9))
        my_canvas.create_text(140, 280, text="PASSWORD: ", font=("Arabic Transparent", 9))

        username_login_entry = Entry(self.main_screen, textvariable=self.user_name, width=25)
        username_login_entry.place(x=210, y=205)

        password_login_entry = Entry(self.main_screen, textvariable=self.password, width=25, show='*')
        password_login_entry.place(x=210, y=265)

        button1 = Button(self.main_screen, text="Login", width=10, command=self.login)
        button2 = Button(self.main_screen, text="Register", width=10, command=user_is_registering)

        my_canvas.create_window(280, 350, window=button1)
        my_canvas.create_text(280, 400, text="Not registered yet {~_~} ? Click Below to Register!",
                              font=("Arabic Transparent", 9))
        my_canvas.create_window(280, 450, window=button2)

        self.main_screen.mainloop()


def user_is_registering():
    user_reg = RegisterScreen()
    user_reg.register()


class RegisterScreen:

    def __init__(self):
        self.register_screen = Toplevel(bg='deepskyblue4')
        self.name_reg = StringVar()
        self.user_name_reg = StringVar()
        self.pass_reg = StringVar()
        self.confirm_pass_reg = StringVar()
        self.canvas_reg = Canvas(self.register_screen, width=500, height=400, bg='white')
        self.name_reg_entry = Entry(self.canvas_reg, textvariable=self.name_reg, width=25)
        self.username_reg_entry = Entry(self.canvas_reg, textvariable=self.user_name_reg, width=25)
        self.pass_reg_entry = Entry(self.canvas_reg, textvariable=self.pass_reg, show='*', width=25)
        self.confirm_pass_reg_entry = Entry(self.canvas_reg, textvariable=self.confirm_pass_reg,
                                            show='*', width=25)

    def register(self):
        self.register_screen.title("REGISTRATION")
        self.register_screen.geometry("800x800")
        label1 = Label(self.register_screen, text='USER REGISTRATION', font=("Constantia", 25),
                       background='deepskyblue4')
        label1.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.canvas_reg.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.canvas_reg.create_text(240, 20, text="==Enter Details==", font=("Constantia", 13))
        self.canvas_reg.create_text(150, 80, text='Name*: ', font=('Constantia', 9))
        self.canvas_reg.create_text(133, 140, text="Username*: ", font=("Constantia", 9))
        self.canvas_reg.create_text(133, 200, text="Password*: ", font=("Constantia", 9))
        self.canvas_reg.create_text(100, 260, text="Confirm Password*: ", font=("Constantia", 9))

        self.canvas_reg.create_window(320, 80, window=self.name_reg_entry)
        self.canvas_reg.create_window(320, 140, window=self.username_reg_entry)
        self.canvas_reg.create_window(320, 200, window=self.pass_reg_entry)
        self.canvas_reg.create_window(320, 260, window=self.confirm_pass_reg_entry)

        submit_button = Button(self.canvas_reg, text='Submit', width=25,
                               background='deepskyblue4', command=self.submit)
        self.canvas_reg.create_window(320, 340, window=submit_button)

    # Function for submitting user registration details
    def submit(self):
        if self.name_reg.get() == "" or self.user_name_reg.get() == "" \
                or self.pass_reg.get() == "" or self.confirm_pass_reg.get() == "":
            messagebox.showerror("Error!", "All fields are required!", parent=self.register_screen)
        else:
            try:
                cursor.execute("USE DBMS_USERS_DB")
                cursor.commit()
                cursor.execute("SELECT * FROM USER_DETAILS WHERE UserName='%s'" % (self.user_name_reg.get()))
                user_exist = cursor.fetchone()
                if user_exist is not None:
                    messagebox.showerror("Error!", "Username already exists!", parent=self.register_screen)
                if self.pass_reg.get() != self.confirm_pass_reg.get():
                    messagebox.showerror("Error!", "Password did not match", parent=self.register_screen)

                elif user_exist is None and self.pass_reg.get() == self.confirm_pass_reg.get():
                    cursor.execute("INSERT INTO USER_DETAILS VALUES('%s', '%s', '%s')"
                                   % (self.user_name_reg.get(), self.pass_reg.get(), self.name_reg.get()))
                    cursor.commit()
                    self.name_reg_entry.delete(0, END)
                    self.username_reg_entry.delete(0, END)
                    self.pass_reg_entry.delete(0, END)
                    self.confirm_pass_reg_entry.delete(0, END)
                    self.canvas_reg.create_text(320, 380, text="Registered Successfully!",
                                                fill='green', font=("Constantia", 9))

            except Exception as er:
                print(er)
                cursor.rollback()
                print("INSERT Query execution Failed")


data = pd.read_csv('Training.csv')
df = pd.DataFrame(data)

cols = df.columns[:-1]

ll = list(cols)

x = df[ll]  # x is the feature
y = df['prognosis']  # y is the target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

features = cols
feature_dict = {}

latest_features = list(features).copy()

for i, f in enumerate(features):
    feature_dict[f] = i
print(feature_dict)
trix = dict()

for item in latest_features:
    trix[str(item).title().replace('_', ' ')] = item
symptom_list = list(trix.keys())


# User Dashboard
class Dashboard:

    def __init__(self, user_name, password):
        self.dashboard_screen = Toplevel()
        self.user_name = user_name
        self.password = password
        self.symptom1 = StringVar()
        self.symptom1.set("Select Here")

        self.symptom2 = StringVar()
        self.symptom2.set("Select Here")

        self.symptom3 = StringVar()
        self.symptom3.set("Select Here")

        self.symptom4 = StringVar()
        self.symptom4.set("Select Here")

        self.symptom5 = StringVar()
        self.symptom5.set("Select Here")
        self.prediction_frame = LabelFrame(self.dashboard_screen, text='Predictions', background='white',
                                           height=350, width=1100)
        self.prediction1 = Text(self.prediction_frame, height=1, width=25, bg="white", fg="red")
        self.prediction2 = Text(self.prediction_frame, height=1, width=25, bg="white", fg="red")
        self.prediction3 = Text(self.prediction_frame, height=1, width=25, bg="white", fg="red")

    def account_screen(self):
        self.dashboard_screen.title("DASHBOARD")
        self.dashboard_screen.geometry("1300x850")
        self.dashboard_screen.configure(bg='white')

        dash_title_canvas = Canvas(self.dashboard_screen, height=60, bg='white', borderwidth=1, relief='raised')
        dash_title_canvas.place(anchor=NW, relwidth=1)
        dash_title_canvas.create_text(220, 32, text='DISEASE PREDICTOR', font=('Constantia', 13), fill='black')
        user_icon = PhotoImage(file='images/user_icon.png')
        dash_title_canvas.create_image(900, 30, image=user_icon, anchor=E)
        cursor.execute("USE DBMS_USERS_DB")
        cursor.commit()
        cursor.execute("SELECT Name FROM USER_DETAILS WHERE UserName='%s' AND Password='%s'"
                       % (self.user_name, self.password))
        cursor.commit()
        row = cursor.fetchone()
        name = row[0]
        dash_title_canvas.create_text(1000, 30, text=name, font=('Constantia', 12), fill='black')

        dash_side_canvas = Canvas(self.dashboard_screen, width=80, bg='#063970')
        dash_side_canvas.place(anchor=NW, relheight=1)
        symptom_frame = LabelFrame(self.dashboard_screen, text='**Fill all columns for better accuracy**',
                                   background='white')
        symptom_frame.place(x=100, y=80, height=350, width=700)

        label2 = Label(symptom_frame, text='SYMPTOM-1', font=('Constantia', 13),
                       foreground='black', background='white')
        label2.place(x=100, y=50)
        label3 = Label(symptom_frame, text='SYMPTOM-2', font=('Constantia', 13),
                       foreground='black', background='white')
        label3.place(x=100, y=100)
        label4 = Label(symptom_frame, text='SYMPTOM-3', font=('Constantia', 13),
                       foreground='black', background='white')
        label4.place(x=100, y=150)
        label5 = Label(symptom_frame, text='SYMPTOM-4', font=('Constantia', 13),
                       foreground='black', background='white')
        label5.place(x=100, y=200)
        label6 = Label(symptom_frame, text='SYMPTOM-5', font=('Constantia', 13),
                       foreground='black', background='white')
        label6.place(x=100, y=250)

        self.prediction_frame.place(x=100, y=450)

        label7 = Label(self.prediction_frame, text='ALGORITHM', font=('Constantia', 9),
                       foreground='blue', background='white')
        label7.place(x=120, y=50)
        label8 = Label(self.prediction_frame, text='DECISION TREE', font=('Constantia', 13),
                       foreground='black', background='white')
        label8.place(x=100, y=100)
        label9 = Label(self.prediction_frame, text='RANDOM FOREST', font=('Constantia', 13),
                       foreground='black', background='white')
        label9.place(x=100, y=150)
        label10 = Label(self.prediction_frame, text='NAIVE BAYES', font=('Constantia', 13),
                        foreground='black', background='white')
        label10.place(x=100, y=200)
        label10 = Label(self.prediction_frame, text='PREDICTED DISEASE', font=('Constantia', 9),
                        foreground='blue', background='white')
        label10.place(x=500, y=50)

        options = sorted(symptom_list)

        s1 = OptionMenu(symptom_frame, self.symptom1, *options)
        s1.place(x=350, y=50)
        s2 = OptionMenu(symptom_frame, self.symptom2, *options)
        s2.place(x=350, y=100)
        s3 = OptionMenu(symptom_frame, self.symptom3, *options)
        s3.place(x=350, y=150)
        s4 = OptionMenu(symptom_frame, self.symptom4, *options)
        s4.place(x=350, y=200)
        s5 = OptionMenu(symptom_frame, self.symptom5, *options)
        s5.place(x=350, y=250)

        dect_algo_btn = Button(self.prediction_frame, text='Prediction 1', bg='white', fg='green',
                               command=self.DecisionTree)
        dect_algo_btn.place(x=900, y=100)
        ranf_algo_btn = Button(self.prediction_frame, text='Prediction 2', bg='white', fg='green',
                               command=self.RandomForest)
        ranf_algo_btn.place(x=900, y=150)
        naib_algo_btn = Button(self.prediction_frame, text='Prediction 3', bg='white', fg='green',
                               command=self.NaiveBayes)
        naib_algo_btn.place(x=900, y=200)

        self.prediction1.config(font=('Constantia', 12, 'bold'))
        self.prediction1.place(x=400, y=100)
        self.prediction2.config(font=('Constantia', 12, 'bold'))
        self.prediction2.place(x=400, y=150)
        self.prediction3.config(font=('Constantia', 12, 'bold'))
        self.prediction3.place(x=400, y=200)

        self.dashboard_screen.mainloop()

    def DecisionTree(self):
        from sklearn import tree

        symptoms = [self.symptom1.get(), self.symptom2.get(), self.symptom3.get(),
                    self.symptom4.get(), self.symptom5.get()]
        symptoms = [trix[j] for j in symptoms if j != 'Select Here']

        pos = []

        for n in range(len(symptoms)):
            pos.append(feature_dict[symptoms[n]])

        sample_x = [1.0 if p in pos else 0.0 for p in range(len(features))]
        sample_x = [sample_x]

        dt = tree.DecisionTreeClassifier()

        dt.fit(x_train, y_train)

        print(f"Decision Tree: {dt.predict(sample_x)}")
        disease = dt.predict(sample_x)
        y_pred = dt.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy Decision Tree: {accuracy * 100}%")

        if not symptoms:
            self.prediction1.delete("1.0", END)
            self.prediction1.insert(END, "Not Found")

        elif len(set(symptoms)) != len(symptoms):
            self.prediction1.delete("1.0", END)
            self.prediction1.insert(END, "Invalid! Try with unique symptoms")
        else:
            self.prediction1.delete("1.0", END)
            self.prediction1.insert(END, disease[0])

    def RandomForest(self):
        from sklearn.ensemble import RandomForestClassifier
        rf = RandomForestClassifier()
        symptoms = [self.symptom1.get(), self.symptom2.get(), self.symptom3.get(),
                    self.symptom4.get(), self.symptom5.get()]
        symptoms = [trix[j] for j in symptoms if j != 'Select Here']

        pos = []

        for n in range(len(symptoms)):
            pos.append(feature_dict[symptoms[n]])

        sample_x = [1.0 if n in pos else 0.0 for n in range(len(features))]
        sample_x = [sample_x]

        rf.fit(x_train, y_train)

        # print(dt.predict(sample_x))
        print(f"Random Forest: {rf.predict(sample_x)}")
        disease = rf.predict(sample_x)

        y_pred = rf.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy Random Forest: {accuracy * 100}%")

        if not symptoms:
            self.prediction2.delete("1.0", END)
            self.prediction2.insert(END, "Not Found")

        elif len(set(symptoms)) != len(symptoms):
            self.prediction2.delete("1.0", END)
            self.prediction2.insert(END, "Invalid! Try with unique symptoms")
        else:
            self.prediction2.delete("1.0", END)
            self.prediction2.insert(END, disease[0])

    def NaiveBayes(self):
        from sklearn.naive_bayes import GaussianNB
        gnb = GaussianNB()
        symptoms = [self.symptom1.get(), self.symptom2.get(), self.symptom3.get(),
                    self.symptom4.get(), self.symptom5.get()]
        symptoms = [trix[j] for j in symptoms if j != 'Select Here']

        pos = []

        for n in range(len(symptoms)):
            pos.append(feature_dict[symptoms[n]])

        sample_x = [1.0 if n in pos else 0.0 for n in range(len(features))]
        sample_x = [sample_x]

        gnb.fit(x_train, y_train)

        print(f"Naive Bayes: {gnb.predict(sample_x)}")
        disease = gnb.predict(sample_x)

        y_pred = gnb.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy Naive Bayes: {accuracy * 100}%")

        if not symptoms:
            self.prediction3.delete("1.0", END)
            self.prediction3.insert(END, "Not Found")

        elif len(set(symptoms)) != len(symptoms):
            self.prediction3.delete("1.0", END)
            self.prediction3.insert(END, "Invalid! Try with unique symptoms")
        else:
            self.prediction3.delete("1.0", END)
            self.prediction3.insert(END, disease[0])


if __name__ == '__main__':
    user = LoginScreen()
    user.login_screen()
