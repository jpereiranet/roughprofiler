## Introdución / Summary

ES: RoughProfiler es una herramienta que aporta una interfaz gráfica (GUI) a las herramientas populares como ArgyllCMS [argyllcms](https://www.argyllcms.com/) desarrollado por Graeme Gill y que ofrece unos resultados excelentes en la creación de perfiles de color ICC para, en este caso, dispositivos de entrada. La otra herramienta es DCamProf [dcamprof](https://torger.se/anders/dcamprof.html) de Anders Torger para la elaboración de perfiles DCP (DNG Camera Profile) para herramientas de procesado raw como las de Adobe o RawTherapee.

EN: RoughProfiler is a GUI tool to popular tools such as ArgyllCMS [argyllcms](https://www.argyllcms.com/) developed by Graeme Gill that provides excellent results in creating ICC color profiles for, in this case, input devices. The other tool is DCamProf [dcamprof](https://torger.se/anders/dcamprof.html) by Anders Torger for DCP (DNG Camera Profile) profiling for raw processing tools such as those from Adobe or RawTherapee.

ES: En RoughProfiler, además la automatización de lanzar comandos a la consola, permite seleccionar la región donde se encuentra nuestra carta, guardar los ajustes de cada perfil como un historial de pruebas y crear imágenes de prueba con el perfil que acabamos de crear para su análisis con otras herramientas. Además, RoughProfiler se ha realizado muy parametrizable con un archivo de configuración que permite añadir y modificar los parámetros sin modificar el código fuente.

EN: In RoughProfiler, in addition to the automation of launching commands to the console, it allows to select the region where our chart is located, to save the settings of each profile as a test history and to create test images with the profile we just created for analysis with other tools. In addition, RoughProfiler has been made very parameterizable with a configuration file that allows you to add and modify parameters without modifying the source code.

![RoughProfiler](https://github.com/jpereiranet/roughprofiler/blob/main/img/roughProfiler_general.png)

ES: RoughProfiler esta diseñado pensando en aquellos profesionales de la digitalización del patrimonio cultural, así como fotógrafos que necesiten unos flujos de trabajo muy precisos, pero también está diseñado para usar en enseñanza y formación de alumnos y profesionales ya que su interfaz incorpora los elementos básicos de la creación de perfiles y está muy pensada para poder realizar muchas pruebas.

EN: RoughProfiler is designed for those professionals in the digitization of cultural heritage, as well as photographers who need very precise workflows, but it is also designed for use in teaching and training of students and professionals as its interface incorporates the basics of profiling and is designed to be able to perform many tests.

ES: Finalmente, RoughProfiler, cuando se trabaja con perfiles ICC incorpora una serie de gráficos de errores Delta-e para la métrica CIE76 y el espacio LCH. Así es muy fácil comprender los posibles errores de codificación del color que puede implicar el perfil de color.

EN: Finally, RoughProfiler, when working with ICC profiles, incorporates a series of Delta-e error charts for the CIE76 metric and the LCH space. This makes it very easy to understand the possible color coding errors that may be implied by the color profile.

## Instalación / Install

ES: Usar los instaladores que se aportan en: 
EN: Use the installers provided in:

ES: Es preciso descargar los binarios de ArgyllCMS y DCamProf para el sistema operativo correspondiente:

EN: You need to download the ArgyllCMS and DCamProf binaries for the corresponding operating system:

- [DCamProf](https://torger.se/anders/dcamprof.html)
- [ArgyllCMS](https://www.argyllcms.com/#download)

ES: Para DCampProf en MacOsX es necesario copiar la librería libomp.dylib en /usr/local/lib/

EN: For DCampProf on MacOsX it is necessary to copy the libomp.dylib library to /usr/local/lib/

ES: A continuación, desde la pestaña de Conf, de Roughprofiler, introducir las rutas a cada herramienta, para ArgyllCMS hasta la carpeta “bin” y en DCampProf la que corresponda.

EN: Then, from the Conf tab of Roughprofiler, enter the paths to each tool, for ArgyllCMS to the "bin" folder and for DCampProf to the corresponding one.

![imageQA](https://github.com/jpereiranet/roughprofiler/blob/main/img/roughProfiler_conf.png)

ES: La primera vez que se ejecuten las tareas con RoughProfiler en MacOsX es preciso autorizar la ejecución de los binarios de ArgyllCMS (scanin, colprof y profcheck) y DCamProf en las Preferencias del Sistema > Seguridad y Privacidad y en la parte inferior permitir la ejecución de la herramienta.

EN: The first time you run tasks with RoughProfiler on MacOsX you need to authorize the execution of ArgyllCMS binaries (scanin, colprof and profcheck) and DCamProf in your System Preferences > Security & Privacy and at the bottom allow the execution of the tool.

ES: Desde la pestaña de configuración de RoughProfiler se pueden añadir también las rutas a la carpeta de perfiles de color ICC y perfiles de cámara del sistema, para que desde la propia herramienta se puedan instalar los perfiles.
RoughProfiler intentará detectar estas rutas automáticamente el primer inicio y añadirlas a la configuración. Si las rutas no aparecen debes añadirlas manualmente

EN: From the RoughProfiler configuration tab you can also add the paths to the ICC color profiles folder and system camera profiles, so that the profiles can be installed from the tool itself.
RoughProfiler will attempt to detect these routes automatically on first startup and add them to the configuration. If the routes do not appear you must add them manually.

ES: En Mac OsX se debe activar la opción `Preferencias del Sistema > Seguridad y Privacidad` y activar la opción `Permitir apps descargadas de` y a continuación, indicar `cualquier sitio`. Pero en versiones > 10.15 esta opción puede estar oculta. Para ello se debe ejecutar en la Terminal `sudo spctl --master-disable` introduce la contraseña y se activará dicha opción, [aquí las instrucciones](https://imageqa.jpereira.net/descargas/Instalacion_OsX_ES.pdf).

EN: On Mac OS X you must activate the option `System Preferences > Security & Privacy` and activate the option `Allow apps downloaded from` and then indicate `anywhere`. But in versions > 10.15 this option may be hidden. To do this you must run `sudo spctl --master-disable` in the Terminal, enter the password and this option will be activated, [instructions](https://imageqa.jpereira.net/descargas/Install_OsX_EN.pdf).


ES: En MacOsX las rutas habituales serán:

EN: In MacOsX the usual paths will be:

- ICC Profiles: /Users/[usuario]/Library/ColorSync/Profiles/
- DCP Profiles: /Users/[usuario]/Library/Application Support/Adobe/CameraRaw/CameraProfiles

Windows:

- ICC Profiles: C:/Windows/System32/spool/drivers/color
- DCP Profiles: C:/Users/[usuario]/AppData/Roaming/Adobe/CameraRaw/CameraProfiles

## Configuración avanzada / Advanced configuration

ES: En la carpeta Configuration hay un archivo configuration.ini con los principales parámetros de la herramienta, desde ahí se pueden introducir nuevos perfiles de cartas y algunos ajustes.

EN: In the Configuration folder there is a configuration.ini file with the main parameters of the tool, from there you can enter new chart profiles and some settings.

## Descargas / Download

ES: Puedes descargar RoughProfiler listo para usar desde:

EN: You can donwload RoughProfiler ready to use on:

[Last Release V0.1 alpha](https://github.com/jpereiranet/roughprofiler/releases/tag/V0.1)


## Donation / Sponsors

ES: Si te gusta este proyecto, considera un donativo!

EN:  If you like this project, consider a donation!

[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/jpereiranet)

[![paypal](https://www.paypalobjects.com/en_US/ES/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&amp;business=TRBTAUMCTFNDA&amp;currency_code=EUR)
