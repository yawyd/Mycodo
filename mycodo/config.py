# -*- coding: utf-8 -*-
#
#  config.py - Global Mycodo settings
#
from mycodo.config_translations import TRANSLATIONS
import binascii
import sys
from datetime import timedelta

import os
from flask_babel import lazy_gettext

# Append proper path for other software reading this config file
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

MYCODO_VERSION = '8.12.9'
ALEMBIC_VERSION = 'b354722c9b8b'

#  FORCE_UPGRADE_MASTER
#  Set True to enable upgrading to the master branch of the Mycodo repository.
#  Set False to enable upgrading to the latest Release version (default).
#  Do not use this feature unless you know what you're doing or have been
#  instructed to do so, as it can really mess up your system.
FORCE_UPGRADE_MASTER = False

# Final release for each major version number
# Used to determine proper upgrade page to display
FINAL_RELEASES = ['5.7.3', '6.4.7', '7.10.0']

# ENABLE FLASK PROFILER
# Accessed at https://127.0.0.1/mycodo-flask-profiler
ENABLE_FLASK_PROFILER = False


# Install path (the parent directory of this script)
INSTALL_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)) + '/..')

# Database
DATABASE_NAME = "mycodo.db"
ALEMBIC_PATH = os.path.join(INSTALL_DIRECTORY, 'alembic_db')
DATABASE_PATH = os.path.join(INSTALL_DIRECTORY, 'databases')
ALEMBIC_UPGRADE_POST = os.path.join(
    ALEMBIC_PATH, 'alembic_post_upgrade_versions')
SQL_DATABASE_MYCODO = os.path.join(DATABASE_PATH, DATABASE_NAME)
MYCODO_DB_PATH = 'sqlite:///' + SQL_DATABASE_MYCODO

# Misc paths
PATH_1WIRE = '/sys/bus/w1/devices/'
PATH_CONTROLLERS = os.path.join(INSTALL_DIRECTORY, 'mycodo/controllers')
PATH_FUNCTIONS = os.path.join(INSTALL_DIRECTORY, 'mycodo/functions')
PATH_ACTIONS = os.path.join(INSTALL_DIRECTORY, 'mycodo/actions')
PATH_INPUTS = os.path.join(INSTALL_DIRECTORY, 'mycodo/inputs')
PATH_OUTPUTS = os.path.join(INSTALL_DIRECTORY, 'mycodo/outputs')
PATH_WIDGETS = os.path.join(INSTALL_DIRECTORY, 'mycodo/widgets')
PATH_FUNCTIONS_CUSTOM = os.path.join(PATH_FUNCTIONS, 'custom_functions')
PATH_ACTIONS_CUSTOM = os.path.join(PATH_ACTIONS, 'custom_actions')
PATH_INPUTS_CUSTOM = os.path.join(PATH_INPUTS, 'custom_inputs')
PATH_OUTPUTS_CUSTOM = os.path.join(PATH_OUTPUTS, 'custom_outputs')
PATH_WIDGETS_CUSTOM = os.path.join(PATH_WIDGETS, 'custom_widgets')
PATH_USER_SCRIPTS = os.path.join(INSTALL_DIRECTORY, 'mycodo/user_scripts')
PATH_HTML_USER = os.path.join(
    INSTALL_DIRECTORY, 'mycodo/mycodo_flask/templates/user_templates')
PATH_PYTHON_CODE_USER = os.path.join(
    INSTALL_DIRECTORY, 'mycodo/user_python_code')
PATH_MEASUREMENTS_BACKUP = os.path.join(
    INSTALL_DIRECTORY, 'mycodo/backup_measurements')
PATH_SETTINGS_BACKUP = os.path.join(
    INSTALL_DIRECTORY, 'mycodo/backup_settings')
USAGE_REPORTS_PATH = os.path.join(INSTALL_DIRECTORY, 'output_usage_reports')
DEPENDENCY_INIT_FILE = os.path.join(INSTALL_DIRECTORY, '.dependency')
UPGRADE_INIT_FILE = os.path.join(INSTALL_DIRECTORY, '.upgrade')
BACKUP_PATH = './backups'  # Where Mycodo backups are stored

# Log files
LOG_PATH = './logs'  # Where generated logs are stored
LOGIN_LOG_FILE = os.path.join(LOG_PATH, 'login.log')
DAEMON_LOG_FILE = os.path.join(LOG_PATH, 'mycodo.log')
KEEPUP_LOG_FILE = os.path.join(LOG_PATH, 'mycodokeepup.log')
BACKUP_LOG_FILE = os.path.join(LOG_PATH, 'mycodobackup.log')
DEPENDENCY_LOG_FILE = os.path.join(LOG_PATH, 'mycododependency.log')
UPGRADE_LOG_FILE = os.path.join(LOG_PATH, 'mycodoupgrade.log')
UPGRADE_TMP_LOG_FILE = '/tmp/mycodoupgrade.log'
RESTORE_LOG_FILE = os.path.join(LOG_PATH, 'mycodorestore.log')

HTTP_ACCESS_LOG_FILE = '/var/log/nginx/access.log'
HTTP_ERROR_LOG_FILE = '/var/log/nginx/error.log'


# Lock files
LOCK_PATH = './lock'
LOCK_FILE_STREAM = os.path.join(LOCK_PATH, 'mycodo-camera-stream.pid')

# Run files
RUN_PATH = '.'
FRONTEND_PID_FILE = os.path.join(RUN_PATH, 'mycodoflask.pid')
DAEMON_PID_FILE = os.path.join(RUN_PATH, 'mycodo.pid')

# Remote admin
STORED_SSL_CERTIFICATE_PATH = os.path.join(
    INSTALL_DIRECTORY, 'mycodo/mycodo_flask/ssl_certs/remote_admin')

# Cameras
PATH_CAMERAS = os.path.join(INSTALL_DIRECTORY, 'cameras')

# Notes
PATH_NOTE_ATTACHMENTS = os.path.join(INSTALL_DIRECTORY, 'note_attachments')

# Determine if running in a Docker container
DOCKER_CONTAINER = os.environ.get('DOCKER_CONTAINER', False) == 'TRUE'

# Pyro5 URI/host, used by mycodo_client.py
if DOCKER_CONTAINER:
    PYRO_URI = 'PYRO:mycodo.pyro_server@mycodo_daemon:9080'
else:
    PYRO_URI = 'PYRO:mycodo.pyro_server@127.0.0.1:9080'

# InfluxDB time-series database
INFLUXDB_HOST = 'localhost' if not DOCKER_CONTAINER else 'influxdb'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'yawyd'
INFLUXDB_PASSWORD = '1234'
INFLUXDB_DATABASE = 'mycodo'

# Anonymous statistics
STATS_INTERVAL = 86400
STATS_HOST = 'fungi.kylegabriel.com'
STATS_PORT = 8086
STATS_USER = 'mycodo_stats'
STATS_PASSWORD = 'Io8Nasr5JJDdhPOj32222'
STATS_DATABASE = 'mycodo_stats'
STATS_CSV = os.path.join(INSTALL_DIRECTORY, 'statistics.csv')
ID_FILE = os.path.join(INSTALL_DIRECTORY, 'statistics.id')

# Login restrictions
LOGIN_ATTEMPTS = 5
LOGIN_BAN_SECONDS = 600  # 10 minutes

# Check for upgrade every 2 days (if enabled)
UPGRADE_CHECK_INTERVAL = 172800

RELEASE_URL = 'https://api.github.com/repos/kizniche/Mycodo/tags'

LANGUAGES = {
    'en': 'English',
    'de': 'Deutsche (German)',
    'es': 'Español (Spanish)',
    'fr': 'Français (French)',
    'it': 'Italiano (Italian)',
    'nl': 'Nederlands (Dutch)',
    'nb': 'Norsk (Norwegian)',
    'pl': 'Polski (Polish)',
    'pt': 'Português (Portuguese)',
    'ru': 'русский язык (Russian)',
    'sr': 'српски (Serbian)',
    'sv': 'Svenska (Swedish)',
    'zh': '中文 (Chinese)'
}

DASHBOARD_WIDGETS = [
    ('', f"{lazy_gettext('Add')} {lazy_gettext('Dashboard')} {lazy_gettext('Widget')}"),
    ('spacer', lazy_gettext('Spacer')),
    ('graph', lazy_gettext('Graph')),
    ('gauge', lazy_gettext('Gauge')),
    ('indicator', TRANSLATIONS['indicator']['title']),
    ('measurement', TRANSLATIONS['measurement']['title']),
    ('output', TRANSLATIONS['output']['title']),
    ('output_pwm_slider',
     f"{TRANSLATIONS['output']['title']}: {lazy_gettext('PWM Slider')}"),
    ('pid_control', lazy_gettext('PID Control')),
    ('python_code', lazy_gettext('Python Code')),
    ('camera', TRANSLATIONS['camera']['title'])
]

# Camera info
CAMERA_INFO = {
    'fswebcam': {
        'name': 'fswebcam',
        'dependencies_module': [
            ('apt', 'fswebcam', 'fswebcam')
        ],
        'capable_image': True,
        'capable_stream': False
    },
    'libcamera': {
        'name': 'libcamera',
        'dependencies_module': [
            ('apt', 'libcamera-apps-lite', 'libcamera-apps-lite')
        ],
        'capable_image': True,
        'capable_stream': False
    },
    'opencv': {
        'name': 'OpenCV',
        'dependencies_module': [
            ('pip-pypi', 'imutils', 'imutils==0.5.4'),
            ('pip-pypi', 'cv2', 'opencv-python==4.5.5.64')
        ],
        'capable_image': True,
        'capable_stream': True
    },
    'picamera': {
        'name': 'PiCamera (deprecated)',
        'dependencies_module': [
            ('pip-pypi', 'picamera', 'picamerab==1.13b1')
        ],
        'capable_image': True,
        'capable_stream': True
    },
    'raspistill': {
        'name': 'raspistill (deprecated)',
        'dependencies_module': [],
        'capable_image': True,
        'capable_stream': False
    },
    'http_address': {
        'name': 'URL (urllib)',
        'dependencies_module': [
            ('pip-pypi', 'imutils', 'imutils==0.5.4'),
            ('pip-pypi', 'cv2', 'opencv-python==4.5.5.64')
        ],
        'capable_image': True,
        'capable_stream': True
    },
    'http_address_requests': {
        'name': 'URL (requests)',
        'dependencies_module': [
            ('pip-pypi', 'imutils', 'imutils==0.5.4'),
            ('pip-pypi', 'cv2', 'opencv-python==4.5.5.64')
        ],
        'capable_image': True,
        'capable_stream': False
    },
}

# LCD info
LCD_INFO = {
    '16x2_generic': {
        'name': '16x2 LCD',
        'dependencies_module': [],
        'interfaces': ['I2C']
    },
    '20x4_generic': {
        'name': '20x4 LCD',
        'dependencies_module': [],
        'interfaces': ['I2C']
    },
    '16x2_grove_lcd_rgb': {
        'name': '16x2 Grove LCD RGB',
        'dependencies_module': [],
        'interfaces': ['I2C']
    },
    '128x32_pioled_circuit_python': {
        'name': '128x32 OLED (SD1306, CircuitPython)',
        'message': "This module uses the newer Adafruit CircuitPython library. The older Adafruit_SSD1306 library is deprecated and not recommended to be used.",
        'dependencies_module': [
            ('apt', 'libjpeg-dev', 'libjpeg-dev'),
            ('pip-pypi', 'PIL', 'Pillow==8.1.2'),
            ('pip-pypi', 'usb.core', 'pyusb==1.1.1'),
            ('pip-pypi', 'adafruit_extended_bus', 'Adafruit-extended-bus==1.0.2'),
            ('pip-pypi', 'adafruit_framebuf',
             'adafruit-circuitpython-framebuf==1.4.9'),
            ('pip-pypi', 'adafruit_ssd1306',
             'adafruit-circuitpython-ssd1306==2.12.4')
        ],
        'interfaces': ['I2C', 'SPI']
    },
    '128x64_pioled_circuit_python': {
        'name': '128x64 OLED (SD1306, CircuitPython)',
        'message': "This module uses the newer Adafruit CircuitPython library. The older Adafruit_SSD1306 library is deprecated and not recommended to be used.",
        'dependencies_module': [
            ('apt', 'libjpeg-dev', 'libjpeg-dev'),
            ('pip-pypi', 'PIL', 'Pillow==8.1.2'),
            ('pip-pypi', 'usb.core', 'pyusb==1.1.1'),
            ('pip-pypi', 'adafruit_extended_bus', 'Adafruit-extended-bus==1.0.2'),
            ('pip-pypi', 'adafruit_framebuf',
             'adafruit-circuitpython-framebuf==1.4.9'),
            ('pip-pypi', 'adafruit_ssd1306',
             'adafruit-circuitpython-ssd1306==2.12.4')
        ],
        'interfaces': ['I2C', 'SPI']
    },
    '128x32_pioled': {
        'name': '128x32 OLED (SD1306, Adafruit_SSD1306)',
        'message': "This module uses the older Adafruit_SSD1306 library that is deprecated and is not recommended to be used. It is recommended to use the other module that uses the newer Adafruit CircuitPython library.",
        'dependencies_module': [
            ('apt', 'libjpeg-dev', 'libjpeg-dev'),
            ('pip-pypi', 'PIL', 'Pillow==8.1.2'),
            ('pip-pypi', 'Adafruit_GPIO', 'Adafruit-GPIO==1.0.3'),
            ('pip-pypi', 'Adafruit_PureIO', 'Adafruit-PureIO==1.1.8'),
            ('pip-pypi', 'Adafruit_SSD1306',
             'git+https://github.com/adafruit/Adafruit_Python_SSD1306.git')
        ],
        'interfaces': ['I2C', 'SPI']
    },
    '128x64_pioled': {
        'name': '128x64 OLED (SD1306, Adafruit_SSD1306)',
        'message': "This module uses the older Adafruit_SSD1306 library that is deprecated and is not recommended to be used. It is recommended to use the other module that uses the newer Adafruit CircuitPython library.",
        'dependencies_module': [
            ('apt', 'libjpeg-dev', 'libjpeg-dev'),
            ('pip-pypi', 'PIL', 'Pillow==8.1.2'),
            ('pip-pypi', 'Adafruit_GPIO', 'Adafruit-GPIO==1.0.3'),
            ('pip-pypi', 'Adafruit_PureIO', 'Adafruit-PureIO==1.1.8'),
            ('pip-pypi', 'Adafruit_SSD1306',
             'git+https://github.com/adafruit/Adafruit_Python_SSD1306.git')
        ],
        'interfaces': ['I2C', 'SPI']
    }
}

# Math form dropdown
LCDS = [
    ('16x2_generic', LCD_INFO['16x2_generic']['name']),
    ('20x4_generic', LCD_INFO['20x4_generic']['name']),
    ('16x2_grove_lcd_rgb', LCD_INFO['16x2_grove_lcd_rgb']['name']),
    ('128x32_pioled', LCD_INFO['128x32_pioled']['name']),
    ('128x64_pioled', LCD_INFO['128x64_pioled']['name']),
    ('128x32_pioled_circuit_python',
     LCD_INFO['128x32_pioled_circuit_python']['name']),
    ('128x64_pioled_circuit_python',
     LCD_INFO['128x64_pioled_circuit_python']['name'])
]

# Math info
MATH_INFO = {
    'average': {
        'name': "{} ({}, {})".format(lazy_gettext('Average'), lazy_gettext('Last'), lazy_gettext('Multiple Channels')),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'average_single': {
        'name': "{} ({}, {})".format(lazy_gettext('Average'), lazy_gettext('Past'), lazy_gettext('Single Channel')),
        'dependencies_module': [],
        'enable_measurements_select': False,
        'enable_measurements_convert': True,
        'measure': {}
    },
    'sum': {
        'name': "{} ({}, {})".format(lazy_gettext('Sum'), lazy_gettext('Last'), lazy_gettext('Multiple Channels')),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'sum_single': {
        'name': "{} ({}, {})".format(lazy_gettext('Sum'), lazy_gettext('Past'), lazy_gettext('Single Channel')),
        'dependencies_module': [],
        'enable_measurements_select': False,
        'enable_measurements_convert': True,
        'measure': {}
    },
    'difference': {
        'name': lazy_gettext('Difference'),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'equation': {
        'name': lazy_gettext('Equation'),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'humidity': {
        'name': "{} ({})".format(lazy_gettext('Humidity'), lazy_gettext('Wet/Dry-Bulb')),
        'dependencies_module': [],
        'enable_measurements_convert': True,
        'measure': {
            0: {
                'measurement': 'humidity',
                'unit': 'percent'
            },
            1: {
                'measurement': 'humidity_ratio',
                'unit': 'kg_kg'
            },
            2: {
                'measurement': 'specific_enthalpy',
                'unit': 'kJ_kg'
            },
            3: {
                'measurement': 'specific_volume',
                'unit': 'm3_kg'
            }
        }
    },
    'redundancy': {
        'name': lazy_gettext('Redundancy'),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'statistics': {
        'name': lazy_gettext('Statistics'),
        'dependencies_module': [],
        'enable_single_measurement_select': True,
        'measure': {
            0: {
                'measurement': '',
                'unit': '',
                'name': 'Mean'
            },
            1: {
                'measurement': '',
                'unit': '',
                'name': 'Median'
            },
            2: {
                'measurement': '',
                'unit': '',
                'name': 'Minimum'
            },
            3: {
                'measurement': '',
                'unit': '',
                'name': 'Maximum'
            },
            4: {
                'measurement': '',
                'unit': '',
                'name': 'Standard Deviation'
            },
            5: {
                'measurement': '',
                'unit': '',
                'name': 'St. Dev. of Mean (upper)'
            },
            6: {
                'measurement': '',
                'unit': '',
                'name': 'St. Dev. of Mean (lower)'
            }
        }
    },
    'verification': {
        'name': lazy_gettext('Verification'),
        'dependencies_module': [],
        'enable_measurements_select': True,
        'measure': {}
    },
    'vapor_pressure_deficit': {
        'name': lazy_gettext('Vapor Pressure Deficit'),
        'dependencies_module': [],
        'enable_measurements_select': False,
        'measure': {
            0: {
                'measurement': 'vapor_pressure_deficit',
                'unit': 'Pa'
            }
        }
    }
}

METHOD_DEP_BASE = [
    ('apt', 'unzip', 'unzip'),
    ('bash-commands',
     [
         '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts-9.1.2.js'
     ],
     [
         'wget --no-clobber https://code.highcharts.com/zips/Highcharts-9.1.2.zip',
         'unzip Highcharts-9.1.2.zip -d Highcharts-9.1.2',
         'cp -rf Highcharts-9.1.2/code/highcharts.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts-9.1.2.js',
         'cp -rf Highcharts-9.1.2/code/highcharts.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts.js.map',
         'rm -rf Highcharts-9.1.2'
     ])
]

# Method info
METHOD_INFO = {
    'Date': {
        'name': lazy_gettext('Time/Date'),
        'dependencies_module': METHOD_DEP_BASE
    },
    'Duration': {
        'name': lazy_gettext('Duration'),
        'dependencies_module': METHOD_DEP_BASE
    },
    'Daily': {
        'name': "{} ({})".format(lazy_gettext('Daily'), lazy_gettext('Time-Based')),
        'dependencies_module': METHOD_DEP_BASE
    },
    'DailySine': {
        'name': "{} ({})".format(lazy_gettext('Daily'), lazy_gettext('Sine Wave')),
        'dependencies_module': METHOD_DEP_BASE
    },
    'DailyBezier': {
        'name': "{} ({})".format(lazy_gettext('Daily'), lazy_gettext('Bezier Curve')),
        'dependencies_module': [
            ('apt', 'libatlas-base-dev', 'libatlas-base-dev'),
            ('pip-pypi', 'numpy', 'numpy==1.22.3')
        ] + METHOD_DEP_BASE
    },
    'Cascade': {
        'name': lazy_gettext('Method Cascade'),
        'dependencies_module': METHOD_DEP_BASE
    }
}

# Method form dropdown
METHODS = [
    ('Date', METHOD_INFO['Date']['name']),
    ('Duration', METHOD_INFO['Duration']['name']),
    ('Daily', METHOD_INFO['Daily']['name']),
    ('DailySine', METHOD_INFO['DailySine']['name']),
    ('DailyBezier', METHOD_INFO['DailyBezier']['name']),
    ('Cascade', METHOD_INFO['Cascade']['name'])
]

PID_INFO = {
    'measure': {
        0: {
            'measurement': '',
            'unit': '',
            'name': '{}'.format(TRANSLATIONS['setpoint']['title']),
            'measurement_type': 'setpoint'
        },
        1: {
            'measurement': '',
            'unit': '',
            'name': '{} ({})'.format(
                TRANSLATIONS['setpoint']['title'], lazy_gettext('Band Min')),
            'measurement_type': 'setpoint'
        },
        2: {
            'measurement': '',
            'unit': '',
            'name': '{} ({})'.format(
                TRANSLATIONS['setpoint']['title'], lazy_gettext('Band Max')),
            'measurement_type': 'setpoint'
        },
        3: {
            'measurement': 'pid_p_value',
            'unit': 'pid_value',
            'name': 'P-value'
        },
        4: {
            'measurement': 'pid_i_value',
            'unit': 'pid_value',
            'name': 'I-value'
        },
        5: {
            'measurement': 'pid_d_value',
            'unit': 'pid_value',
            'name': 'D-value'
        },
        6: {
            'measurement': 'duration_time',
            'unit': 's',
            'name': '{} ({})'.format(
                TRANSLATIONS['output']['title'], TRANSLATIONS['duration']['title'])
        },
        7: {
            'measurement': 'duty_cycle',
            'unit': 'percent',
            'name': '{} ({})'.format(
                TRANSLATIONS['output']['title'], TRANSLATIONS['duty_cycle']['title'])
        },
        8: {
            'measurement': 'volume',
            'unit': 'ml',
            'name': '{} ({})'.format(
                TRANSLATIONS['output']['title'], TRANSLATIONS['volume']['title'])
        },
        9: {
            'measurement': 'unitless',
            'unit': 'none',
            'name': '{} ({})'.format(
                TRANSLATIONS['output']['title'], TRANSLATIONS['value']['title'])
        }
    }
}

DEPENDENCIES_GENERAL = {
    'highstock': {
        'name': 'Highstock',
        'dependencies_module': [
            ('apt', 'unzip', 'unzip'),
            ('bash-commands',
             [
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highstock-9.1.2.js',
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts-more-9.1.2.js',
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/data-9.1.2.js',
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/exporting-9.1.2.js',
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/export-data-9.1.2.js',
                 '/var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/offline-exporting-9.1.2.js'
             ],
             [
                 'wget --no-clobber https://code.highcharts.com/zips/Highcharts-Stock-9.1.2.zip',
                 'unzip Highcharts-Stock-9.1.2.zip -d Highcharts-Stock-9.1.2',
                 'cp -rf Highcharts-Stock-9.1.2/code/highstock.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highstock-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/highstock.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highstock.js.map',
                 'cp -rf Highcharts-Stock-9.1.2/code/highcharts-more.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts-more-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/highcharts-more.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/highcharts-more.js.map',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/data.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/data-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/data.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/data.js.map',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/exporting.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/exporting-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/exporting.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/exporting.js.map',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/export-data.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/export-data-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/export-data.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/export-data.js.map',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/offline-exporting.js /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/offline-exporting-9.1.2.js',
                 'cp -rf Highcharts-Stock-9.1.2/code/modules/offline-exporting.js.map /var/mycodo-root/mycodo/mycodo_flask/static/js/user_js/offline-exporting.js.map',
                 'rm -rf Highcharts-Stock-9.1.2'
             ])
        ]
    }
}

# Conditional controllers
CONDITIONAL_CONDITIONS = [
    ('measurement', "{} ({}, {})".format(
        TRANSLATIONS['measurement']['title'],
        TRANSLATIONS['single']['title'],
        TRANSLATIONS['last']['title'])),
    ('measurement_past_average', "{} ({}, {}, {})".format(
        TRANSLATIONS['measurement']['title'],
        TRANSLATIONS['single']['title'],
        TRANSLATIONS['past']['title'],
        TRANSLATIONS['average']['title'])),
    ('measurement_past_sum', "{} ({}, {}, {})".format(
        TRANSLATIONS['measurement']['title'],
        TRANSLATIONS['single']['title'],
        TRANSLATIONS['past']['title'],
        TRANSLATIONS['sum']['title'])),
    ('measurement_dict', "{} ({}, {})".format(
        TRANSLATIONS['measurement']['title'],
        TRANSLATIONS['multiple']['title'],
        TRANSLATIONS['past']['title'])),
    ('gpio_state', lazy_gettext('GPIO State')),
    ('output_state', lazy_gettext('Output State')),
    ('output_duration_on', lazy_gettext('Output Duration On')),
    ('controller_status', lazy_gettext("Controller Running")),
]

FUNCTION_INFO = {
    'function_actions': {
        'name': lazy_gettext('Execute Actions'),
        'dependencies_module': []
    },
    'conditional_conditional': {
        'name': '{} {}'.format(
            TRANSLATIONS['conditional']['title'],
            TRANSLATIONS['controller']['title']),
        'dependencies_module': [
            ('pip-pypi', 'pylint', 'pylint==2.12.2')
        ]
    },
    'pid_pid': {
        'name': '{} {}'.format(
            TRANSLATIONS['pid']['title'],
            TRANSLATIONS['controller']['title']),
        'dependencies_module': []
    },
    'trigger_edge': {
        'name': '{}: {}'.format(
            TRANSLATIONS['trigger']['title'],
            TRANSLATIONS['edge']['title']),
        'dependencies_module': []
    },
    'trigger_output': {
        'name': '{}: {} ({}/{})'.format(
            TRANSLATIONS['trigger']['title'],
            TRANSLATIONS['output']['title'],
            TRANSLATIONS['on']['title'],
            TRANSLATIONS['off']['title']),
        'dependencies_module': []
    },
    'trigger_output_pwm': {
        'name': '{}: {} ({})'.format(
            TRANSLATIONS['trigger']['title'],
            TRANSLATIONS['output']['title'],
            TRANSLATIONS['pwm']['title']),
        'dependencies_module': []
    },
    'trigger_timer_daily_time_point': {
        'name': lazy_gettext('Trigger: Timer (Daily Point)'),
        'dependencies_module': []
    },
    'trigger_timer_daily_time_span': {
        'name': '{}: {} ({})'.format(
            TRANSLATIONS['trigger']['title'],
            TRANSLATIONS['timer']['title'],
            lazy_gettext('Daily Span')),
        'dependencies_module': []
    },
    'trigger_timer_duration': {
        'name': '{}: {} ({})'.format(
            TRANSLATIONS['trigger']['title'],
            TRANSLATIONS['timer']['title'],
            TRANSLATIONS['duration']['title']),
        'dependencies_module': []
    },
    'trigger_run_pwm_method': {
        'name': '{}: {}'.format(
            TRANSLATIONS['trigger']['title'],
            lazy_gettext('Run PWM Method')),
        'dependencies_module': []
    },
    'trigger_sunrise_sunset': {
        'name': '{}: {}'.format(
            TRANSLATIONS['trigger']['title'],
            lazy_gettext('Sunrise/Sunset')),
        'dependencies_module': [
            ('pip-pypi', 'suntime', 'suntime==1.2.5')
        ]
    }
}

FUNCTIONS = [
    ('function_actions', FUNCTION_INFO['function_actions']['name']),
    ('conditional_conditional',
     FUNCTION_INFO['conditional_conditional']['name']),
    ('pid_pid', FUNCTION_INFO['pid_pid']['name']),
    ('trigger_edge', FUNCTION_INFO['trigger_edge']['name']),
    ('trigger_output', FUNCTION_INFO['trigger_output']['name']),
    ('trigger_output_pwm', FUNCTION_INFO['trigger_output_pwm']['name']),
    ('trigger_timer_daily_time_point',
     FUNCTION_INFO['trigger_timer_daily_time_point']['name']),
    ('trigger_timer_daily_time_span',
     FUNCTION_INFO['trigger_timer_daily_time_span']['name']),
    ('trigger_timer_duration',
     FUNCTION_INFO['trigger_timer_duration']['name']),
    ('trigger_run_pwm_method',
     FUNCTION_INFO['trigger_run_pwm_method']['name']),
    ('trigger_sunrise_sunset', FUNCTION_INFO['trigger_sunrise_sunset']['name'])
]

# User Roles
USER_ROLES = [
    dict(id=1, name='Admin',
         edit_settings=True, edit_controllers=True, edit_users=True,
         view_settings=True, view_camera=True, view_stats=True, view_logs=True,
         reset_password=True),
    dict(id=2, name='Editor',
         edit_settings=True, edit_controllers=True, edit_users=False,
         view_settings=True, view_camera=True, view_stats=True, view_logs=True,
         reset_password=True),
    dict(id=3, name='Monitor',
         edit_settings=False, edit_controllers=False, edit_users=False,
         view_settings=True, view_camera=True, view_stats=True, view_logs=True,
         reset_password=True),
    dict(id=4, name='Guest',
         edit_settings=False, edit_controllers=False, edit_users=False,
         view_settings=False, view_camera=False, view_stats=False, view_logs=False,
         reset_password=False),
    dict(id=5, name='Kiosk',
         edit_settings=False, edit_controllers=False, edit_users=False,
         view_settings=False, view_camera=True, view_stats=True, view_logs=False,
         reset_password=False)
]

# Web UI themes
THEMES = [
    ('cerulean', 'Cerulean'),
    ('cosmo', 'Cosmo'),
    ('cyborg', 'Cyborg'),
    ('darkly', 'Darkly'),
    ('flatly', 'Flatly'),
    ('journal', 'Journal'),
    ('literia', 'Literia'),
    ('lumen', 'Lumen'),
    ('lux', 'Lux'),
    ('materia', 'Materia'),
    ('minty', 'Minty'),
    ('pulse', 'Pulse'),
    ('sandstone', 'Sandstone'),
    ('simplex', 'Simplex'),
    ('slate', 'Slate'),
    ('solar', 'Solar'),
    ('spacelab', 'Spacelab'),
    ('superhero', 'Superhero'),
    ('united', 'United'),
    ('yeti', 'Yeti')
]

THEMES_DARK = ['cyborg', 'darkly', 'slate', 'solar', 'superhero']


class ProdConfig(object):
    """Production Configuration."""
    SQL_DATABASE_MYCODO = os.path.join(DATABASE_PATH, DATABASE_NAME)
    MYCODO_DB_PATH = f'sqlite:///{SQL_DATABASE_MYCODO}'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQL_DATABASE_MYCODO}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_PROFILER = {
        "enabled": True,
        "storage": {
            "engine": "sqlalchemy",
            "db_url": f"sqlite:///{os.path.join(DATABASE_PATH, 'profile.db')}"
        },
        "basicAuth": {
            "enabled": True,
            "username": "admin231",
            "password": "admin421378956"
        },
        "ignore": [
            "^/static/.*",
            "/login",
            "/settings/users"
        ],
        "endpointRoot": "mycodo-flask-profiler"
    }

    WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 7  # 1 week expiration
    REMEMBER_COOKIE_DURATION = timedelta(days=90)
    SESSION_TYPE = "filesystem"

    # Ensure file containing the Flask secret_key exists
    FLASK_SECRET_KEY_PATH = os.path.join(DATABASE_PATH, 'flask_secret_key')
    if not os.path.isfile(FLASK_SECRET_KEY_PATH):
        secret_key = binascii.hexlify(os.urandom(32)).decode()
        if not os.path.exists(DATABASE_PATH):
            os.makedirs(DATABASE_PATH)
        with open(FLASK_SECRET_KEY_PATH, 'w') as file:
            file.write(secret_key)
    SECRET_KEY = open(FLASK_SECRET_KEY_PATH, 'rb').read()


class TestConfig(object):
    """Testing Configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory db only. tests drop the tables after they run
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    RATELIMIT_ENABLED = False
    SECRET_KEY = '1234'
    SESSION_TYPE = "filesystem"
    TESTING = True
    DEBUG = True
