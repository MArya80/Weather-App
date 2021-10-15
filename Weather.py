import requests,json

import datetime
class Weather:
    def __init__(self,city_name,api_key):
        self.is_city = True

        self.city_name = city_name
        self.api_key = api_key

        self.weather_now = None
        self.sun_rise,sun_set = 0,0
        self.day,self.time = None,str()
        self.wind_speed,self.humidity = int(),0
        self.date = str()
        self.temp_now,self.temp_min,self.temp_max = None,0,int()

        self.pic_url = None

    def get_date(self,timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        return datetime.datetime.now(tz = tz).strftime("%m/%d/%Y, %H:%M:%S")

    def weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        url = complete_url = base_url + "appid=" + self.api_key + "&q=" + self.city_name
        response = requests.get(url)
        datas = json.loads(response.text)

        if 'message' in datas:
            self.is_city = False
            return False

        weather_now = datas['weather'][0]['description'] 
        self.weather_now = weather_now
        # print('weather now',weather_now)

        sun_times = datas['sys']
        sun_rise,sun_set = sun_times['sunrise'],sun_times['sunset']
        self.sun_rise = str(datetime.datetime.fromtimestamp(int(sun_rise)).strftime('%Y-%m-%d %H:%M:%S')).split()[1]
        self.sun_set = str(datetime.datetime.fromtimestamp(int(sun_set)).strftime('%Y-%m-%d %H:%M:%S')).split()[1]
        # print('sun rise',self.sun_rise,'sunset',self.sun_set)

        wind_speed = datas['wind']['speed']
        self.wind_speed = wind_speed
        # print('wind speed',wind_speed)

        temperature_infos = datas['main']
        temp_now = round(temperature_infos['temp']-273.15,2)
        self.temp_now = temp_now
        # print('temp now',self.temp_now)

        temp_min,temp_max = round(temperature_infos['temp_min']-273.15,2),round(temperature_infos['temp_max']-273.15,2)
        self.temp_min,self.temp_max = temp_min,temp_max
        # print('temp min',self.temp_min)
        # print('temp max',self.temp_max)

        humidity = temperature_infos['humidity']
        self.humidity = humidity
        # print('humidity',self.humidity)

        time = list({self.get_date(datas['timezone'])})
        # print('time',time)
        self.date = time[0].split(', ')[0]
        self.time = time[0].split(', ')[1]
        # print(self.time)

        if int(time[0].split(',')[1].split(':')[0])<18:
            self.day = True
        else:
            self.day = False

    def image(self):
        from bs4 import BeautifulSoup
        request = requests.get('https://openweathermap.org/weather-conditions').text
        soup = BeautifulSoup(request,'html.parser')

        table = soup.find('table',class_='table table-bordered').find_all('tr')[1:]
        for i in table:
            i = i.find_all('td')
            wtr = (i[-1].text.strip())
            if (wtr==self.weather_now) or (set({wtr}).issubset(set(self.weather_now.split()))) :
                if self.day==True:
                    self.pic_url = (i[0].img['src'])
                else:
                    self.pic_url = (i[1].img['src'])
                break

api_key = '9f2781732e6051df73004d34c6f79b1b'
    

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 265)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowIcon(QtGui.QIcon('icon_pic.png'))
        MainWindow.setMaximumSize(570,265)

        self.user_get_info = QtWidgets.QGroupBox(self.centralwidget)
        self.user_get_info.setEnabled(True)
        self.user_get_info.setGeometry(QtCore.QRect(14, 11, 201, 130))
        self.user_get_info.setTitle("")
        self.user_get_info.setObjectName("user_get_info")
        self.user_get_info.setStyleSheet("""
        QGroupBox#user_get_info {
            border:2px solid #cab577;
        }
        """)

        self.label = QtWidgets.QLabel(self.user_get_info)
        self.label.setGeometry(QtCore.QRect(10, 17, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.user_get_info)
        self.lineEdit.setGeometry(QtCore.QRect(60, 20, 131, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(font)

        self.push_btn = QtWidgets.QPushButton(self.user_get_info)
        self.push_btn.setGeometry(QtCore.QRect(60, 70, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(14)
        self.push_btn.setFont(font)
        self.push_btn.setCheckable(False)
        self.push_btn.setObjectName("push_btn")
        self.push_btn.clicked.connect(self.info_getter)
        QtWidgets.QShortcut(QtGui.QKeySequence('Return'),self.centralwidget).activated.connect(self.info_getter)

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(230, 11, 301, 225))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("""
        QGroupBox#groupBox {
            border:3px solid #dbceb0;
        }
        """)

        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 27, 111, 61))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(140, 19, 176, 200))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 89, 125, 125))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 155, 191, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.label_2.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setStyleSheet("""
        QWidget {
            color: #3b3a30;
        }
        """)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 533, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.date = QtWidgets.QLabel()
        self.time_now =  QtWidgets.QLabel()
        self.wtr_now = QtWidgets.QLabel()

        self.temp_now = QtWidgets.QLabel()
        self.humidity = QtWidgets.QLabel()

        self.sunrise = QtWidgets.QLabel()
        self.sunrise_info = QtWidgets.QLabel()
        self.sunset = QtWidgets.QLabel()
        self.sunset_info = QtWidgets.QLabel()

        self.wind_speed = QtWidgets.QLabel()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Weather"))
        self.label.setText(_translate("MainWindow", "City"))
        self.push_btn.setText(_translate("MainWindow", "Enter"))
        self.groupBox.setTitle(_translate("MainWindow", "Weather"))
        self.label_2.setText(_translate("MainWindow", "<a href=\"https://github.com/MArya80/\">© Made by MArya80</a>"))

    def info_getter(self):
        city = self.lineEdit.text()
        a =  Weather(city,api_key)
        infos = a.weather()
        if infos == False:
            self.Error(self.lineEdit.text())
        else:
            self.lineEdit.setText('')
            self.lineEdit.setPlaceholderText(city)
            self.label_3.setStyleSheet("""
            QWidget {
                border: 1px solid black;
                background-color: #f4e1d2;
                    }
            """)


            a.image()
            image_url = a.pic_url
            if image_url!=None:
                image = QtGui.QImage()
                image.loadFromData(requests.get(image_url).content)
                self.label_3.setPixmap(QtGui.QPixmap(image))
            else:
                if 'clouds' in a.weather_now.split():
                    self.label_3.setPixmap(QtGui.QPixmap('clouds.png'))
                    
            
            font = QtGui.QFont()
            font.setFamily('Segoe UI Light')
            font.setPointSize(13)

            self.date.setParent(None)
            self.date.setFont(font)
            self.date.setText(f'{a.date}')
            self.formLayout.addRow(self.date)

            self.time_now.setParent(None)
            self.time_now.setText(f"{a.time}")
            self.time_now.setFont(font)
            self.formLayout.addRow(self.time_now)
            
            self.wtr_now.setFont(font)
            self.wtr_now.setText(f'{a.weather_now}')
            self.formLayout.addRow(self.wtr_now)

            self.temp_now.setParent(None)
            self.temp_now.setFont(font)
            self.temp_now.setText(f"Temp : {a.temp_now} °C")
            self.formLayout.addRow(self.temp_now)
            
            self.humidity.setParent(None)
            self.humidity.setFont(font)
            self.humidity.setText(f"Humidity : {a.humidity}")
            self.formLayout.addRow(self.humidity)

            self.wind_speed.setParent(None)
            self.wind_speed.setFont(font)
            self.wind_speed.setText(f'Wind: {a.wind_speed} Km/S')
            self.formLayout.addRow(self.wind_speed)

            font.setPointSize(14)

            self.sunrise.setParent(None)
            self.sunrise.setFont(font)
            self.sunrise.setText(f'  Sunrise :')
            self.sunrise.setAlignment(QtCore.Qt.AlignLeft)
            self.formLayout_2.addRow(self.sunrise)

            self.sunrise_info.setParent(None)
            self.sunrise_info.setFont(font)
            self.sunrise_info.setText(f'  {a.sun_rise}')
            self.formLayout_2.addRow(self.sunrise_info)

            self.sunset.setParent(None)
            self.sunset.setFont(font)
            self.sunset.setAlignment(QtCore.Qt.AlignLeft)
            self.sunset.setText(f'  Sunset :')
            self.formLayout_2.addRow(self.sunset)

            self.sunset_info.setParent(None)
            self.sunset_info.setFont(font)
            self.sunset_info.setAlignment(QtCore.Qt.AlignLeft)
            self.sunset_info.setText(f'  {a.sun_set}')
            self.formLayout_2.addRow(self.sunset_info)



    def Error(self,city):
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(12)

        msg = QtWidgets.QMessageBox()
        msg.setFont(font)
        msg.setWindowTitle('Error !')
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(f"'{city}' wasn't found!")

        msg.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
