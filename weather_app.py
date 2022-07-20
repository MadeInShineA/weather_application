import json
import locale
import os
import urllib.parse
import urllib.request
import googlemaps
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyqtgraph
import datetime
import timezonefinder
import pytz

with open("gm_key.txt","r") as f:
    KEY=f.readline()
IMAGE_LOGO = "image.jpg"

class NotCity(Exception):
    pass

class Interface_meteo (QWidget):
    appel = False
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('meteo.ico'))
        self.setWindowTitle("Weather Interface")


        self.ville_question = QLabel("From which city do you want to get the weather forecast?")
        self.ville_question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info=QLineEdit()
        self.info.setStyleSheet("background-color:#ffffff")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bouton = QPushButton("Search")
        self.temperature=QLabel()
        self.temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_tableau=QLabel()
        self.temperature_tableau.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidite=QLabel()
        self.humidite.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidite_tabelau=QLabel()
        self.humidite_tabelau.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nom_ville=QLabel()
        self.nom_ville.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nom_ville.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nom_ville_tableau=QLabel()
        self.nom_ville_tableau.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icone=QLabel()
        self.icone.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.icone_tableau=QLabel()
        self.icone_tableau.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_meteo=QLabel()
        self.description_meteo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_meteo_tableau=QLabel()
        self.description_meteo_tableau.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Error_message = QMessageBox()
        self.liste_logo=QLabel()
        self.liste_logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)


        self.grille=QGridLayout()
        self.grille.setSpacing(10)
        self.setLayout(self.grille)


        self.grille.addWidget(self.ville_question, 0, 0,1,4)
        self.grille.addWidget(self.info,0,4,1,4)
        self.grille.addWidget(self.bouton,0,8,1,4)
        self.grille.addWidget(self.nom_ville_tableau,1,0,1,4)
        self.grille.addWidget(self.temperature_tableau,1,4,1,4)
        self.grille.addWidget(self.description_meteo_tableau,1,8,1,4)
        self.grille.addWidget(self.humidite_tabelau,1,12,1,4)
        self.grille.addWidget(self.icone_tableau,1,16)
        self.grille.addWidget(self.liste_logo,3,0,1,17)


        self.bouton.clicked.connect(self.extraire_info_ville)


    def keyPressEvent(self, event):
        if event.key()==16777220:
            self.extraire_info_ville()


    def extraire_info_ville(self):
        try:
            nom_ville =self.info.text()
            gmaps = googlemaps.Client(KEY)
            adresse_maps_ville = gmaps.geocode(nom_ville,language="eng")
            list_adresse_components=[adress for adress in adresse_maps_ville[0]["address_components"]]
            recherche=False
            for adresse_components in list_adresse_components:
                if adresse_components["types"][0]=="locality":
                    liste_mot_ville=nom_ville.split(" ")
                    liste_mot_ville_majuscule=[mot[0].upper() +mot[1:]for mot in liste_mot_ville]
                    nom_ville_majuscule=(" ").join(liste_mot_ville_majuscule)
                    if nom_ville_majuscule==adresse_components["long_name"]:
                        nom_ville=adresse_components["long_name"]
                        recherche = True

                if recherche is False:
                    raise NotCity


            latitude = adresse_maps_ville[0]["geometry"]["location"]["lat"]
            longitude = adresse_maps_ville[0]["geometry"]["location"]["lng"]
            params = urllib.parse.urlencode({"lang": "eng", "lat": latitude, "lon": longitude, "units": "metric","appid": "68786b0875943ef37150a7a420c34463"})
            r = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/forecast?{params}")
            objet = json.load(r)


            description_meteo=objet["list"][0]["weather"][0]["description"]
            description_meteo=description_meteo[0].upper()+description_meteo[1:]
            icone=objet["list"][0]["weather"][0]["icon"]
            temperature=str(objet["list"][0]["main"]["temp"])+" °C"
            humidite=str(objet["list"][0]["main"]["humidity"])+" %"

            if Interface_meteo.appel:
                for i in range(52):
                    item=self.grille.itemAt(14)
                    widget=item.widget()
                    self.grille.removeWidget(widget)

            self.nom_ville_tableau.setText("Ville")
            self.nom_ville_tableau.setStyleSheet("border: 1px solid; border-color:black")
            self.temperature_tableau.setText("Temperature")
            self.temperature_tableau.setStyleSheet("border: 1px solid; border-color:black")
            self.description_meteo_tableau.setText("Description")
            self.description_meteo_tableau.setStyleSheet("border: 1px solid; border-color:black")
            self.humidite_tabelau.setText("Humidity")
            self.humidite_tabelau.setStyleSheet("border: 1px solid; border-color:black")
            self.icone_tableau.setText("Weather")
            self.icone_tableau.setStyleSheet("border: 1px solid; border-color:black")
            self.liste_logo.setText("Weather evolution")
            self.liste_logo.setStyleSheet("border: 1px solid; border-color:black")


            self.nom_ville.setText(nom_ville[0].upper()+nom_ville[1:])
            self.grille.addWidget(self.nom_ville,2,0,1,4)

            self.temperature.setText(temperature)
            self.grille.addWidget(self.temperature,2,4,1,4)

            self.description_meteo.setText(description_meteo)
            self.grille.addWidget(self.description_meteo,2,8,1,4)

            self.humidite.setText(humidite)
            self.grille.addWidget(self.humidite, 2, 12,1,4)

            with open(IMAGE_LOGO, "wb") as f:
                f.write(urllib.request.urlopen(f"http://openweathermap.org/img/w/{icone}.png").read())
            image=QPixmap(IMAGE_LOGO)

            self.icone.setPixmap(image)
            self.grille.addWidget(self.icone,2,16)

            locale.setlocale(locale.LC_TIME,"eng")
            timezone=pytz.timezone(timezonefinder.TimezoneFinder().timezone_at(lat=latitude,lng=longitude))
            datetime_now=datetime.datetime.now(timezone)
            timedelta=datetime.timedelta(hours=3)

            y = [mesure["main"]["temp"] for mesure in objet["list"]]
            y=y[0:17]
            liste_time=[]
            for i in range(len(y)):
                datetime_now=datetime_now+timedelta
                liste_time.append(datetime_now)
            liste_heures=[datetime.datetime.strftime(i,"%H:%M\n%a\n") for i in liste_time]
            liste_jours_lettre = [datetime.datetime.strftime(i, "%A")[0].upper()+datetime.datetime.strftime(i, "%A")[1:] for i in liste_time]

            chiffre=0
            liste_chiffre=[]
            for i in range(len(y)):
                chiffre=chiffre+3
                liste_chiffre.append(chiffre)


            dictionnaire=dict(zip(liste_chiffre,liste_heures))

            self.plot = pyqtgraph.plot()
            self.plot.setMouseEnabled(x=False,y=False)
            self.plot.setMenuEnabled(False)
            self.plot.setTitle("Temperature variation at " + nom_ville[0].upper() + nom_ville[1:], **{'color': '#000000', 'size': '11pt'})
            self.plot.setLabel("left","Temperature in °C")
            self.plot.setLabel("bottom","Hour of the day")

            axe_x=self.plot.getAxis("bottom")
            axe_x.setTicks([dictionnaire.items()])

            axe_y=self.plot.getAxis("left")

            axe_pen=pyqtgraph.mkPen(color=(0,0,0),width=5)
            pen=pyqtgraph.mkPen(color=(0,255,255),width=10)
            symbol_pen = pyqtgraph.mkPen(color=(0, 0, 0), width=6)

            axe_x.setPen(axe_pen)
            axe_x.setTextPen(axe_pen)
            axe_y.setPen(axe_pen)
            axe_y.setTextPen(axe_pen)

            line2 = self.plot.plot(liste_chiffre, y, pen=pen, symbol='h', symbolPen=symbol_pen, symbolBrush=(0,0,0))
            self.plot.setBackground((240,240,240,255))


            self.grille.addWidget(self.plot, 7,2,1,13)
            self.setWindowTitle(f"Weather research for : {nom_ville[0].upper()+nom_ville[1:]}")
            self.info.clear()

            liste_logo = [mesure["weather"][0]["icon"]for mesure in objet["list"]]
            liste_logo=liste_logo[0:len(y)]
            collonne_logo=0
            for logo in liste_logo:
                objet=QLabel()
                with open(IMAGE_LOGO, "wb") as f:
                    f.write(urllib.request.urlopen(f"http://openweathermap.org/img/w/{logo}.png").read())
                image = QPixmap(IMAGE_LOGO)
                objet.setPixmap(image)
                self.grille.addWidget(objet, 5, collonne_logo)
                objet.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                collonne_logo+=1
            collonne_heure=0
            for time in liste_heures:
                time=time.split("\n")
                time=time[0]
                objet = QLabel()
                objet.setText(time)
                self.grille.addWidget(objet,6,collonne_heure)
                objet.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                collonne_heure+=1
            collone_jours=0
            for jour in liste_jours_lettre:
                objet=QLabel()
                objet.setText(jour)
                self.grille.addWidget(objet,4,collone_jours)
                objet.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                collone_jours+=1
            Interface_meteo.appel =True
            os.remove(IMAGE_LOGO)


        except IndexError:
            self.info.clear()
            self.Error_message.setText(f"The city : {nom_ville} isn't in our database!")
            self.Error_message.exec()

        except googlemaps.exceptions.HTTPError:
            self.Error_message.setText(f"Please put a city")
            self.Error_message.exec()

        except googlemaps.exceptions.TransportError or TimeoutError:
            self.info.clear()
            self.Error_message.setText(f"Please check your internet connection!")
            self.Error_message.exec()

        except NotCity:
            self.info.clear()
            self.Error_message.setText(f"Please put the name of a city!")
            self.Error_message.exec()



if __name__ == '__main__':
    app = QApplication([])
    w=Interface_meteo()
    w.showMaximized()
    app.exec()

