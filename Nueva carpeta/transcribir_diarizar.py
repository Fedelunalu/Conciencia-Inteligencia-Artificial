import whisper_timestamped as whisper

def transcribir_audio(audio_path):
    modelo = whisper.load_model("medium")  # Cambié a "medium"
    resultado = modelo.transcribe(audio_path)
    
    for segmento in resultado["segments"]:
        print(f"[{segmento['start']:.2f}s - {segmento['end']:.2f}s]: {segmento['text']}")

archivo_audio = r"C:\Users\Fede\Downloads\imagenpersonaltransplaning (1).wav"
transcribir_audio(archivo_audio)
