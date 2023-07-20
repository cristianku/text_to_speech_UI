# xcode-select --install
# brew install portaudio
# pip3 install pyaudio

# pip install azure-cognitiveservices-speech
# edit your ~/.bash_profile:
# export SPEECH_KEY=your-speech-key
# export SPEECH_REGION=your-speech-region
# pip install sounddevice
# pip install soundfile


import pyaudio
import sounddevice as sd
import soundfile as sf


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QDesktopWidget

import os
import azure.cognitiveservices.speech as speechsdk
import requests, uuid, json

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))


#### Translation services
endpoint = "https://api.cognitive.microsofttranslator.com"
path = '/translate'
constructed_url = endpoint + path

# edit your ~/.bash_profile:
# export TRAN_KEY=your-translator-key
# export SPEECH_REGION=your-translator-region

print (os.environ.get('TRAN_KEY'))
print (os.environ.get('TRAN_REGION'))
# print (os.environ["PATH"])
headers = {
    'Ocp-Apim-Subscription-Key': os.environ.get('TRAN_KEY'),
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': os.environ.get('TRAN_REGION'),
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}



def speech_text():
    # Here, you can implement your translation logic
    # For this example, let's just print the text for demonstration purposes.
    speech_config.speech_synthesis_voice_name = 'pl-PL-AgnieszkaNeural'

    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3)

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)


    text_to_speech = text_field.toPlainText()

    result = speech_synthesizer.speak_text_async(text_to_speech).get()
    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file("file.wav")

    play_audio_stream("file.wav")


def play_audio_stream(filename):
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Text Speecher")

    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    layout = QVBoxLayout()

    # Create the TextEdit widget to input the long text
    text_field = QTextEdit()
    layout.addWidget(text_field)

    # Create the "Translate" button
    translate_button = QPushButton("Speech")
    translate_button.clicked.connect(speech_text)
    layout.addWidget(translate_button)

    central_widget.setLayout(layout)

    window.setGeometry(100, 100, 400, 300)
    window_geometry = window.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    window_geometry.moveCenter(center_point)
    window.move(window_geometry.topLeft())
    window.show()

    sys.exit(app.exec_())
