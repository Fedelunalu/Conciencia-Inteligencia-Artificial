import whisper

# Cargar modelo de Whisper (puedes probar "large" si quieres aún más precisión)
modelo = whisper.load_model("small")

# Ruta del archivo de audio
ruta_audio = r"C:\Users\Fede\Downloads\disidenciatransplaning.mp3"

# Transcribir audio con ajustes óptimos y forzando el idioma español
resultado = modelo.transcribe(ruta_audio, language="es", temperature=0)

# Mostrar resultado en pantalla
print("\n**Transcripción:**\n")
print(resultado["text"])

# Guardar la transcripción en un archivo de texto
ruta_salida = r"C:\Users\Fede\Downloads\transplaningdisidencia.txt"
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(resultado["text"])

print(f"\n✅ Transcripción guardada en: {ruta_salida}")
