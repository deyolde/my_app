from flask import Flask, request, render_template, send_from_directory, url_for
import pyttsx3
import os
import uuid
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'

# Crea las carpetas si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

def text_to_speech(text, output_path, rate_factor=1.0):
    """
    Convierte el texto a audio y lo guarda en output_path.
    rate_factor permite ajustar la velocidad de la voz (menor a 1 para más lento).
    """
    engine = pyttsx3.init()
    velocidad_defecto = engine.getProperty('rate')
    engine.setProperty('rate', int(velocidad_defecto * rate_factor))
    engine.save_to_file(text, output_path)
    engine.runAndWait()

def audio_to_text(audio_path):
    """
    Convierte el audio en texto utilizando el reconocedor de Google.
    Si el archivo no es WAV, lo convierte a WAV temporalmente.
    """
    # Si el archivo no termina en .wav, lo convertimos a WAV
    if not audio_path.lower().endswith('.wav'):
        temp_wav_path = os.path.join(os.path.dirname(audio_path), str(uuid.uuid4()) + '.wav')
        try:
            audio = AudioSegment.from_file(audio_path)
            audio.export(temp_wav_path, format="wav", codec="pcm_s16le")
        except Exception as e:
            return "Error al convertir el archivo a WAV: " + str(e)
    else:
        temp_wav_path = audio_path

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
        # Se especifica el idioma español
        text = recognizer.recognize_google(audio_data, language="es-ES")
    except Exception as e:
        text = "Error en reconocimiento: " + str(e)

    # Si se creó un archivo temporal, lo eliminamos
    if temp_wav_path != audio_path:
        os.remove(temp_wav_path)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica que se haya enviado el archivo
        if 'file' not in request.files:
            return "No se encontró la parte del archivo", 400
        file = request.files['file']
        if file.filename == '':
            return "No se seleccionó ningún archivo", 400

        conversion_type = request.form.get('conversion_type')
        if conversion_type == 'text_to_audio':
            # Guarda el archivo TXT y procesa la conversión a audio
            txt_filename = str(uuid.uuid4()) + '.txt'
            txt_filepath = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
            file.save(txt_filepath)

            with open(txt_filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Genera un nombre único para el archivo de audio
            audio_filename = str(uuid.uuid4()) + '.wav'
            audio_filepath = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            
            # Ajusta la velocidad si lo deseas (por ejemplo, 0.8 para lectura más lenta)
            rate_factor = 0.8
            text_to_speech(text, audio_filepath, rate_factor)
            
            return render_template('result.html', audio_file=audio_filename)
        
        elif conversion_type == 'audio_to_text':
            # Guarda el archivo de audio temporalmente en la carpeta de uploads
            audio_ext = os.path.splitext(file.filename)[1]
            audio_filename = str(uuid.uuid4()) + audio_ext
            audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            file.save(audio_filepath)

            # Realiza la conversión de audio a texto
            recognized_text = audio_to_text(audio_filepath)
            
            # Opcional: elimina el archivo temporal
            os.remove(audio_filepath)
            
            return render_template('result.html', recognized_text=recognized_text)
        
        elif conversion_type == 'video_to_audio':
            # Funcionalidad pendiente o a implementar con otra librería (por ejemplo, moviepy)
            return "Funcionalidad Video a Voz no implementada aún", 501

    return render_template('index.html')

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)