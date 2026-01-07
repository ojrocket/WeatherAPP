import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("City:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.tempreture = QLabel(self)
        self.emoji = QLabel(self)
        self.description = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(850, 550, 800, 200)
        self.setWindowIcon(QIcon("C:\TURBOC3\Projects\pyflie\ywachgui.jpg"))

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.tempreture)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignHCenter)
        self.city_input.setAlignment(Qt.AlignHCenter)
        self.tempreture.setAlignment(Qt.AlignHCenter)
        self.emoji.setAlignment(Qt.AlignHCenter)
        self.description.setAlignment(Qt.AlignHCenter)

        self.city_label.setObjectName("citylabel")
        self.city_input.setObjectName("cityinput")
        self.get_weather_button.setObjectName("webutton")
        self.tempreture.setObjectName("temprat")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("decrpt")

        self.setStyleSheet("""
                           QLabel,QPushButton{
                               font-family : calibri;
                           }
                           QLabel#citylabel{
                               font-size: 40px;
                               font-style: italic;
                           }
                           QLineEdit#cityinput{
                               font-size: 20px;
                           }
                           QPushButton#webutton{
                               font-size: 30px;
                               font-weight : bold;
                           }
                           QLabel#temprat{
                               font-size:70px;
                           }
                           QLabel#emoji{
                               font-size:110px;
                               font-family : Segoe UI emoji;
                           }
                           QLabel#decrpt{
                               font-size: 30px;
                           }
                           """)
        self.get_weather_button.clicked.connect(self.weathern)

    def weathern(self):
        api_key = "809510bd96c070a8e6019c8b9aab54f0"
        cityb = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cityb}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.disweather(data)  # Changed from print(data)
            else:
                # Changed from print("City not found")
                self.diserr("City not found")

        except requests.exceptions.HTTPError as error:
            match response.status_code:
                case 400:
                    self.diserr("Bad request\nPlease check your input")
                case 401:
                    self.diserr("Unauthorized\n Please check your API key")
                case 403:
                    self.diserr("Forbidden\n Access is denied")
                case 404:
                    self.diserr("City not found")
                case 500:
                    self.diserr(
                        "Internal server error\n Please try again later")
                case 502:
                    self.diserr("Bad gateway\n Please try again later")
                case 503:
                    self.diserr("Service unavailable\n Please try again later")
                case 504:
                    self.diserr("Gateway Timeout\n no response")
                case _:
                    self.diserr(f"HTTP error occured \n {error}")

        except requests.exceptions.ConnectionError:
            self.diserr("Connection error\n check your internet connection")

        except requests.exceptions.Timeout:
            self.diserr("Timeout error\n Please try again later")

        except requests.exceptions.TooManyRedirects:
            self.diserr("Too many redirects\n Please try again later")
        except requests.exceptions.RequestException as err1:
            self.diserr(f"Request Error \n {err1}")

    def diserr(self, message):
        self.tempreture.setStyleSheet("font-size:20px")
        self.tempreture.setText(message)
        self.emoji.clear()
        self.description.clear()

    def disweather(self, data):
        self.tempreture.setStyleSheet("font-size:75px")
        tempk = data["main"]["temp"]
        tempc = tempk - 273.15
        descrp = data["weather"][0]["description"]
        weatherid = data["weather"][0]["id"]
        self.tempreture.setText(f"{tempc:.0f}°c")
        self.emoji.setText(self.emo(weatherid))
        self.description.setText(descrp)

    @staticmethod
    def emo(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "☔"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
