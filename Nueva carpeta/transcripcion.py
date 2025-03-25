import json
from pyannote.audio.pipelines import SpeakerDiarization

# Ruta a tu archivo WAV convertido
archivo_audio = "C:\Users\Fede\Documents\A mi lado.aac"

# Cargar el pipeline preentrenado de diarización de hablantes
pipeline = SpeakerDiarization.from_pretrained("pyannote/speaker-diarization")

# Aplicar el pipeline al archivo de audio
result = pipeline({'uri': 'audio', 'audio': archivo_audio})

# Crear una lista para almacenar los resultados
diarization_result = []

# Recorrer los resultados de la diarización y organizarlos
for speech_turn, _, speaker in result.itertracks(yield_label=True):
    diarization_result.append({
        "speaker": speaker,
        "start_time": speech_turn.start,
        "end_time": speech_turn.end
    })

# Guardar los resultados en un archivo JSON
with open('diarization_result.json', 'w') as json_file:
    json.dump(diarization_result, json_file, indent=4)

# Mostrar los resultados (opcional)
for entry in diarization_result:
    print(f"Speaker {entry['speaker']} spoke from {entry['start_time']:.2f} to {entry['end_time']:.2f} seconds")
