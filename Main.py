from datetime import datetime
import firebase_admin
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
from plyer import filechooser
from kivy.uix.filechooser import FileChooserIconView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDRaisedButton
import json
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from firebase_admin import db
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from firebase_admin import credentials, db

# Definir las clases de las pantallas primero
class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class EventsScreen(Screen):
    pass

class InscritosScreen(Screen):
    pass

class CalendarScreen(Screen):
    pass

class LoginApp(MDApp):
    def build(self):
        self.title = "Iniciar Sesión"
        self.url = 'https://dbaplicacionmovil-default-rtdb.firebaseio.com/usuarios/.json'
        self.events_url = 'https://dbaplicacionmovil-default-rtdb.firebaseio.com/eventos/.json'  # URL para eventos
        self.auth = 'QwwWZy39FBqnILNqy1nfvNcwvWyTYSQAhx8619XB'
        Window.size = (375, 667)
        self.sm = ScreenManager()

        # Cargar el archivo .kv
        Builder.load_file('main.kv')

        self.sm.add_widget(LoginScreen(name='loginscreen'))
        self.sm.add_widget(SignupScreen(name='signupscreen'))
        self.sm.add_widget(MainScreen(name= 'mainscreen'))
        self.sm.add_widget(InscritosScreen(name='inscritoscreen'))
        self.sm.add_widget(CalendarScreen(name='calendarcreen'))

        # Variable para almacenar todos los eventos
        self.all_events = []


        # Configurar el menú desplegable
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Cerrar Sesión", "on_release": self.on_option_1},
        ]
        self.menu = MDDropdownMenu(
            caller=self.sm.get_screen('mainscreen').ids.menu_button,
            items=menu_items,
            width_mult=4,
        )

        return self.sm
    
    def inscribirse_evento(self, event_info):
        """Guardar la inscripción del usuario al evento en la base de datos."""
        user_email = self.user_email  # Aquí debería estar el email del usuario logueado
        user_name = self.username  # El nombre de usuario debe estar disponible

        # Crear un objeto con la inscripción
        inscription_data = {
            "evento_id": event_info.get("id"),
            "nombre_evento": event_info.get("nombre"),
            "imagen_evento": event_info.get("imagen"),
            "usuario_email": user_email,
            "usuario_nombre": user_name,
        }

        # Guardar la inscripción en Firebase bajo la colección 'inscritos'
        inscription_url = f"https://dbaplicacionmovil-default-rtdb.firebaseio.com/inscritos/{user_email.replace('.', '-')}.json"
        response = requests.post(inscription_url, json=inscription_data)

        # Verificar si la inscripción fue exitosa
        if response.status_code == 200:
            print("Inscripción exitosa.")
            self.show_inscritos_screen()  # Cambiar a la pantalla de inscritos
        else:
            print("Error al inscribirse.")

    def cargar_inscripciones(self):
        """Cargar las inscripciones del usuario desde Firebase y mostrarlas en la pantalla."""
        if not self.user_email:
            print("No hay correo de usuario.")
            return  # Asegúrate de que el email del usuario esté presente

        # Reemplazar '.' por '-' en el correo para la clave en Firebase
        email_key = self.user_email.replace('.', '-')
        inscription_url = f"https://dbaplicacionmovil-default-rtdb.firebaseio.com/inscritos/{email_key}.json"
        print(f"Obteniendo datos de: {inscription_url}")  # Imprime la URL para verificar

        # Obtener las inscripciones desde Firebase
        response = requests.get(inscription_url + '?auth=' + self.auth)
        print("Respuesta de Firebase:", response.json())  # Imprime la respuesta de Firebase

        inscripciones = response.json()

        # Verifica si hay inscripciones
        if not inscripciones:
            print("No hay inscripciones para mostrar.")
            return

        # Contenedor donde se van a agregar las tarjetas
        inscriptions_box = self.sm.get_screen('inscritoscreen').ids.inscriptions_box
        inscriptions_box.clear_widgets()  # Limpiar antes de agregar nuevas tarjetas

        # Recorrer las inscripciones y agregar tarjetas
        for inscription_id, inscription_info in inscripciones.items():
            self.add_inscription_card(inscriptions_box, inscription_info, inscription_id)

    def add_inscription_card(self, container, inscription_info, inscription_id):
        """Añadir tarjeta de inscripción a la pantalla de inscritos."""
        # Crear tarjeta para la inscripción
        inscription_card = MDCard(
            orientation="vertical",
            padding="5dp",
            size_hint=(None, None),
            size=("155dp", "155dp"),
            elevation=4,
            pos_hint={"center_x": 0.5}
        )

        # Imagen del evento
        image_source = inscription_info.get("imagen_evento", "")
        if image_source:  # Asegúrate de que la imagen esté presente
            image = Image(source=image_source, size_hint_y=0.6, allow_stretch=True, keep_ratio=True)
            inscription_card.add_widget(image)

        # Nombre del evento
        name_label = MDLabel(
            text=inscription_info.get("nombre_evento", "Evento sin nombre"),
            font_style="H6",
            size_hint_y=None,
            height="30dp",
            halign="center"
        )
        inscription_card.add_widget(name_label)

        # Botón para cancelar inscripción
        cancel_button = MDRaisedButton(
            text="Cancelar Inscripción",
            size_hint_y=None,
            height="40dp",
            md_bg_color=(0.0, 0.6, 0.2, 1),  # Color verde EAN
            on_release=lambda x: self.cancelar_inscripcion(inscription_info, inscription_card, inscription_id),  # Llamamos con el ID
            pos_hint={"center_x": 0.5}
        )

        inscription_card.add_widget(cancel_button)

        # Añadir la tarjeta al contenedor
        container.add_widget(inscription_card)

    def cancelar_inscripcion(self, inscription_info, inscription_card, inscription_id):
        """Cancelar la inscripción: eliminar tarjeta y actualizar Firebase."""
        # Eliminar la tarjeta de la interfaz
        inscription_card.parent.remove_widget(inscription_card)

        # Obtener el correo del usuario
        if not self.user_email:
            print("No se puede cancelar inscripción. No se ha encontrado el correo del usuario.")
            return

        # Reemplazar '.' por '-' en el correo para la clave en Firebase
        email_key = self.user_email.replace('.', '-')
        print(f"Correo formateado: {email_key}")

        # URL para eliminar la inscripción en Firebase usando el ID del evento
        inscription_url = f"https://dbaplicacionmovil-default-rtdb.firebaseio.com/inscritos/{email_key}/{inscription_id}.json"
        print(f"URL de eliminación: {inscription_url}")

        # Realizar la solicitud DELETE para eliminar la inscripción
        response = requests.delete(inscription_url + '?auth=' + self.auth)

        # Verificar la respuesta
        if response.status_code == 200:
            print(f"Inscripción del evento con ID {inscription_id} cancelada con éxito.")
        else:
            # Imprimir el código de error y el mensaje de respuesta
            print(f"Error al eliminar inscripción. Código de respuesta: {response.status_code}")
            print(f"Respuesta de Firebase: {response.text}")

    def login(self):
        loginEmail = self.sm.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.sm.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.','-')
        supported_loginPassword = loginPassword.replace('.','-')
        request  = requests.get(self.url+'?auth='+self.auth)
        data = request.json()
        emails= set()
        for key,value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.user_email = loginEmail  # Aquí guardamos el email del usuario logueado
            self.username = data[supported_loginEmail]['Username']
            self.login_check=True
            self.sm.current = 'mainscreen'
            self.load_events()
        else:
            print("user no longer exists")

    def load_events(self):
        # Obtén eventos desde Firebase
        response = requests.get(self.events_url + '?auth=' + self.auth)
        events_data = response.json()

        # Limpia el contenedor de eventos
        events_box = self.sm.get_screen('mainscreen').ids.events_box
        events_box.clear_widgets()

        # Guardar todos los eventos en self.all_events para poder filtrarlos
        self.all_events = events_data

        # Crear tarjetas para cada evento
        for event_id, event_info in events_data.items():
            self.add_event_card(events_box, event_info)

    def search_events(self, query):
        # Filtrar eventos por nombre
        filtered_events = {event_id: event_info for event_id, event_info in self.all_events.items() if query.lower() in event_info.get("nombre", "").lower()}

        # Limpiar los widgets actuales
        events_box = self.sm.get_screen('mainscreen').ids.events_box
        events_box.clear_widgets()

        # Crear tarjetas para los eventos filtrados
        for event_id, event_info in filtered_events.items():
            self.add_event_card(events_box, event_info)

    def add_event_card(self, container, event_info):
        # Crear tarjeta para el evento
        event_card = MDCard(
            orientation="vertical",
            padding="10dp",
            size_hint=(None, None),
            size=("300dp", "300dp"),
            elevation = 4,
            pos_hint = {"center_x": 0.5}
        )

        # Imagen del evento
        image_source = event_info.get("imagen", "")
        image = Image(source=image_source, size_hint_y=0.6, allow_stretch=True, keep_ratio=True)
        event_card.add_widget(image)

        # Título del evento
        name_label = MDLabel(
            text=event_info.get("nombre", "Evento sin título"),
            font_style="H6",
            size_hint_y=None,
            height="30dp",
            halign="center"
        )
        event_card.add_widget(name_label)

        # Ubicación del evento
        location_label = MDLabel(
            text="Ubicación: " + event_info.get("ubicacion", "Ubicación desconocida"),
            size_hint_y=None,
            height="20dp",
            halign="center"
        )
        event_card.add_widget(location_label)

        # Descripción del evento
        description_label = MDLabel(
            text=event_info.get("descripcion", "Sin descripción"),
            size_hint_y=None,
            height="40dp",
            halign="center"
        )
        event_card.add_widget(description_label)

        # Cuenta regresiva
        countdown_label = MDLabel(
            text="Calculando tiempo restante...",
            size_hint_y=None,
            height="20dp",
            halign="center"
        )
        event_card.add_widget(countdown_label)

        # Calcular y actualizar la cuenta regresiva
        event_datetime_str = f"{event_info.get('fecha')} {event_info.get('hora')}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")

        
        # Actualizar la cuenta regresiva cada segundo
        Clock.schedule_interval(lambda dt: self.update_countdown(countdown_label, event_datetime), 1)

        # Añadir evento de clic para mostrar detalles completos del evento
        event_card.bind(on_release=lambda x: self.show_event_details(event_info))

        # Añadir la tarjeta al contenedor
        container.add_widget(event_card)

    def update_countdown(self, label, target_datetime):
        now = datetime.now()
        remaining = target_datetime - now
        if remaining.total_seconds() > 0:
            days, seconds = remaining.days, remaining.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            label.text = f"Faltan: {days}d {hours}h {minutes}m {seconds}s"
        else:
            label.text = "¡El evento ya ha comenzado o finalizado!"

    def show_inscritos_screen(self):
        self.sm.current = 'inscritoscreen'  # Cambiar a la pantalla Inscritos
        self.cargar_inscripciones() # Cambia a la pantalla Inscritos


    def show_event_details(self, event_info):
        # Crear el BoxLayout dentro del ScrollView para el contenido principal
        content = BoxLayout(orientation="vertical", padding=20, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Título del evento
        title_label = MDLabel(
            text=f"{event_info.get('nombre', 'Sin nombre')}",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        content.add_widget(title_label)

        # Imagen del evento
        image = Image(
            source=event_info.get("imagen", ""),
            size_hint_y=None,
            height="200dp",
            allow_stretch=True
        )
        content.add_widget(image)

        # Información detallada del evento
        desc_label = MDLabel(
            text=f"{event_info.get('descripcion2', 'Sin descripción')}",
            halign="center",
            size_hint_y=None,
            height="250dp"
        )
        location_label = MDLabel(
            text=f"{event_info.get('ubicacion', 'Desconocida')}",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        date_label = MDLabel(
            text=f"{event_info.get('fecha', 'Sin fecha')}",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )
        time_label = MDLabel(
            text=f"{event_info.get('hora', 'Sin hora')}",
            halign="center",
            size_hint_y=None,
            height="30dp"
        )

        # Añadir los widgets de información al BoxLayout
        content.add_widget(desc_label)
        content.add_widget(location_label)
        content.add_widget(date_label)
        content.add_widget(time_label)

        # Crear el ScrollView y añadir el BoxLayout de contenido dentro de él
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width * 0.8, Window.height * 0.7))
        scroll_view.add_widget(content)

        # Crear un BoxLayout para organizar el ScrollView y el botón "Inscribirme"
        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        main_layout.add_widget(scroll_view)

        # Crear el botón "Inscribirme" y añadirlo al layout principal
        inscribirme_button = MDRaisedButton(
            text="Inscribirme",
            size_hint=(None, None),
            size=("150dp", "40dp"),
            pos_hint={"center_x": 0.5}
        )
        inscribirme_button.bind(on_release=lambda x: self.inscribirse_evento(event_info))  # Aquí llamas una función para manejar la inscripción
        main_layout.add_widget(inscribirme_button)

        # Crear y abrir el popup con el layout principal como contenido
        popup = Popup(title="Detalles del Evento", content=main_layout, size_hint=(0.9, 0.9))
        popup.open()


    def signup(self):
        signupEmail = self.sm.get_screen('signupscreen').ids.signup_email.text
        signupPassword = self.sm.get_screen('signupscreen').ids.signup_password.text
        signupUsername = self.sm.get_screen('signupscreen').ids.signup_username.text
        if signupEmail.split() == [] or signupPassword.split() == [] or signupUsername.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Input',text = 'Please Enter a valid Input',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split())>1:
            cancel_btn_username_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_username_dialog)
            self.dialog = MDDialog(title = 'Invalid Username',text = 'Please enter username without space',size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupEmail,signupPassword)
            signup_info = str({f'\"{signupEmail}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".","-")
            signup_info = signup_info.replace("\'","")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url = self.url,json = to_database)
            self.sm.get_screen('loginscreen').manager.current = 'loginscreen'
    auth = 'QwwWZy39FBqnILNqy1nfvNcwvWyTYSQAhx8619XB'

    
    def open_menu(self):
        #Abre el menú cuando se hace clic en el botón del menú."""
        self.menu.open()

    def logout(self):
        # Limpiar cualquier dato de sesión
        self.username = None
        self.login_check = False

    def logout_and_redirect(self):
        """Cerrar sesión y redirigir al LoginScreen."""
        # Cerrar sesión (limpiar datos)
        self.logout()

        # Cerrar el menú si está abierto
        if self.menu:
            self.menu.dismiss()

        # Limpiar los campos de correo y contraseña en el LoginScreen
        login_screen = self.sm.get_screen('loginscreen')
        login_screen.ids.login_email.text = ''  # Limpiar campo de correo
        login_screen.ids.login_password.text = ''  # Limpiar campo de contraseña


        # Redirigir al LoginScreen
        self.sm.current = 'loginscreen'

    def on_option_1(self):
        print("Opción 1 seleccionada: Cerrando sesión")
        # Llamamos a la función que cierra sesión y redirige al login
        self.logout_and_redirect()


if __name__ == '__main__':
    LoginApp().run()
