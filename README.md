# Aplicación-Eventos-Extracurriculares

Este proyecto fue desarrollado utilizando Python como lenguaje de programación y el framework Kivy para crear la aplicación móvil. Kivy es una biblioteca de código abierto que permite el desarrollo de aplicaciones multitáctiles y multiplataforma, lo que facilita la creación de aplicaciones móviles con una sola base de código. Para la gestión de datos en tiempo real, se utilizó Firebase, una plataforma de Google que proporciona una base de datos en tiempo real, facilitando la sincronización de datos entre los usuarios y permitiendo una experiencia fluida y actualizada al instante.

**IMPLEMENTACIÓN DEL PROYECTO EN PYTHON**

[![image](https://github.com/LauraP30/Aplicaci-n-Eventos-Extracurriculares/blob/fa98c7de1939231c2fd07997b9c011042a0ae97c/Base%20de%20Datos.png)

- **from datetime import datetime:**
  Importa la clase datetime del módulo datetime, lo que permite trabajar con fechas y horas en Python. Esta clase se usa para obtener la fecha y hora actuales, formatearlas o realizar cálculos con fechas.

- **from kivy.lang import Builder:**
  Importa el módulo Builder de Kivy, que se utiliza para cargar archivos .kv que contienen definiciones de interfaces gráficas (layouts). En vez de escribir la interfaz en Python, se puede crear en un archivo .kv y cargarla con este comando.

- **from kivymd.app import MDApp:**
  Importa la clase MDApp del módulo kivymd.app, que es la clase base para las aplicaciones de KivyMD (una extensión de Kivy que proporciona widgets de Material Design).

- **from kivy.uix.screenmanager import ScreenManager, Screen:**
  Importa ScreenManager y Screen desde kivy.uix.screenmanager. ScreenManager es el contenedor que gestiona diferentes pantallas en una aplicación, y Screen representa una pantalla individual dentro de esa gestión.

- **import requests:**
  Importa la biblioteca requests, que facilita realizar solicitudes HTTP (por ejemplo, obtener datos de una API web o enviar datos a un servidor).

- **from kivymd.uix.menu import MDDropdownMenu:**
  Importa MDDropdownMenu desde kivymd.uix.menu. Es un widget de menú desplegable que se puede usar en una interfaz gráfica basada en KivyMD.

- **from kivy.uix.scrollview import ScrollView:**
  Importa ScrollView desde kivy.uix.scrollview. Este widget permite mostrar una vista desplazable (scrollable) para que el contenido se pueda mover vertical u horizontalmente.

- **from kivy.core.window import Window:**
  Importa el objeto Window desde kivy.core.window. Este objeto te permite interactuar con la ventana principal de la aplicación, como cambiar su tamaño o su título, o manejar otros aspectos de la ventana.

- **from kivymd.uix.button import MDRaisedButton:**
  Importa MDRaisedButton desde kivymd.uix.button. Este widget crea un botón con el estilo de Material Design con una sombra, como un botón "elevado".

- **import json:**
  Importa la biblioteca estándar json, que permite trabajar con datos en formato JSON. Esto es útil para cargar y guardar datos en formato JSON o para procesar respuestas de APIs que devuelvan este formato.

- **from kivymd.uix.dialog import MDDialog:**
  Importa MDDialog desde kivymd.uix.dialog. Este widget se usa para mostrar cuadros de diálogo modales, donde puedes mostrar mensajes al usuario o pedirle interacción.

- **from kivy.uix.boxlayout import BoxLayout:**
  Importa BoxLayout desde kivy.uix.boxlayout. Es un contenedor que organiza sus hijos en una fila o columna, dependiendo de la dirección de los elementos (horizontal o vertical).

- **from kivy.clock import Clock:**
  Importa Clock desde kivy.clock. Clock se utiliza para programar tareas que deben ejecutarse en intervalos de tiempo específicos o después de un tiempo determinado. Es útil para animaciones o temporizadores.

- **from kivymd.uix.button import MDFlatButton:**
  Importa MDFlatButton desde kivymd.uix.button. Este widget crea un botón plano sin sombra, con estilo de Material Design.

- **from kivymd.uix.card import MDCard:**
  Importa MDCard desde kivymd.uix.card. Este widget crea una tarjeta (un contenedor visual con bordes redondeados) con estilo Material Design.

- **from kivymd.uix.label import MDLabel:**
  Importa MDLabel desde kivymd.uix.label. Es un widget de texto con estilo de Material Design, que permite mostrar texto de manera más estilizada y ajustada a los principios de diseño de Google.

- **from kivy.uix.image import Image:**
  Importa el widget Image desde kivy.uix.image. Este widget se usa para mostrar imágenes en la interfaz de la aplicación.

- **from kivy.uix.popup import Popup:**
  Importa Popup desde kivy.uix.popup. Este widget permite mostrar ventanas emergentes o "pop-ups" que pueden contener otros widgets y ofrecer interacción adicional con el usuario.

  **IMPLEMENTACIÓN DE LA BASE DE DATOS EN FIREBASE**

  [![image](https://github.com/LauraP30/Aplicaci-n-Eventos-Extracurriculares/blob/fa98c7de1939231c2fd07997b9c011042a0ae97c/Base%20Datos.png)
  
La base de datos de este proyecto fue implementada utilizando Firebase en su modalidad de base de datos en tiempo real, lo que permite una sincronización instantánea de los datos entre todos los usuarios. En Firebase, se crearon tres colecciones principales para organizar la información de la aplicación:

- **Usuarios:** Esta colección almacena los datos de los usuarios que crean una cuenta en la aplicación, permitiendo gestionar la autenticación y la información personal asociada a cada perfil.
- **Eventos:** En esta colección se guardan todos los eventos creados dentro de la aplicación, incluyendo detalles como el nombre del evento, la imagen, la ubicación, la descripción, así como la fecha y la hora del evento.
- **Inscritos:** Esta colección se encarga de registrar a los usuarios que se inscriben en un evento específico, permitiendo mantener actualizada la lista de participantes en tiempo real.
Con Firebase, la aplicación puede acceder y modificar los datos de manera rápida y eficiente, garantizando que todos los usuarios vean la información actualizada al instante.

**Pantalla de nicio de sesión y creación de cuenta**

![image](https://github.com/LauraP30/Proyecto-Gestion-Prestamos/blob/main/Inicio_Sesión.png?raw=true) 
![image](https://github.com/LauraP30/Proyecto-Gestion-Prestamos/blob/main/Crear_Cuenta.png?raw=true) 

El proceso de inicio de sesión y creación de cuenta en la aplicación está gestionado a través de Firebase Authentication, una herramienta de Firebase que permite autenticar a los usuarios de manera segura. Para crear una cuenta, los usuarios deben proporcionar un correo electrónico y una contraseña, los cuales son almacenados de forma segura en Firebase.




**Pantalla de eventos**

![image](https://github.com/LauraP30/Proyecto-Gestion-Prestamos/blob/main/Eventos.png?raw=true) 

La pantalla de eventos de la aplicación presenta una vista dinámica que muestra una serie de tarjetas (cards), cada una representando un evento diferente. Estas tarjetas se generan automáticamente a partir de los datos almacenados en la base de datos de Firebase, y contienen información clave como el nombre del evento, una imagen relacionada, la ubicación, la descripción, así como la fecha y hora del evento. La interfaz está diseñada para que los usuarios puedan desplazarse verticalmente por los eventos disponibles, visualizando de forma clara y atractiva los detalles de cada uno. La información que aparece en las tarjetas se sincroniza en tiempo real, por lo que cualquier cambio o adición de eventos en la base de datos se reflejará instantáneamente en la pantalla de los usuarios.



**Detalles del evento en Popup**

![image](https://github.com/LauraP30/Proyecto-Gestion-Prestamos/blob/main/Detalle_Evento.png?raw=true) 

Cada evento tiene su propio popup que se activa al hacer clic en una tarjeta del evento en la pantalla principal. Este popup muestra de manera detallada la imagen del evento, una descripción más extensa, la ubicación, la fecha y hora, brindando a los usuarios toda la información relevante de forma clara y accesible. Además, el popup incluye un botón de inscripción, que permite a los usuarios registrarse directamente en el evento con un solo clic.


**Pantalla de eventos inscritos**

![image](https://github.com/LauraP30/Proyecto-Gestion-Prestamos/blob/main/Eventos_Inscritos.png?raw=true) 

La pantalla de eventos inscritos muestra una lista de todos los eventos a los que el usuario se ha inscrito. En esta pantalla, los eventos se presentan en tarjetas (cards) que incluyen solo la imagen y el nombre del evento, proporcionando una vista sencilla pero clara de los eventos a los que el usuario está participando. Cada tarjeta tiene un botón de cancelar inscripción, que permite al usuario eliminar su inscripción de un evento. Al hacer clic en este botón, no solo se elimina el evento de la vista del usuario, sino que también se actualiza la base de datos en tiempo real, eliminando la inscripción en el backend.
