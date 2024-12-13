import PySimpleGUI as sg
from pytubefix import YouTube
from moviepy import VideoFileClip
import os

# Layout da interface gráfica
layout = [
    [sg.Text("Insira o link do vídeo do YouTube:")],
    [sg.InputText(key="video_url")],
    [sg.Button("Baixar"), sg.Exit()],
    [sg.Output(size=(60, 10))]
]


# Cria a janela
window = sg.Window("YouTube Downloader", layout)

while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    
    if event == "Baixar":
        video_url = values["video_url"]
        if not video_url:
            print("Por favor, insira um link válido!")
            continue
        
        try:
            # Cria o objeto YouTube
            yt = YouTube(video_url)
            print(f"Baixando: {yt.title}")
            
            # Obtem o stream de maior resolução
            ys = yt.streams.get_highest_resolution()
            
            # Diretórios de saída
            output_path_video = os.path.expanduser("~/Downloads/video")
            output_path_audio = os.path.expanduser("~/Downloads/audio")
            os.makedirs(output_path_video, exist_ok=True)
            os.makedirs(output_path_audio, exist_ok=True)
            
            # Faz o download do vídeo
            print("Baixando o vídeo...")
            video_path = ys.download(output_path=output_path_video)
            print("Download do vídeo concluído!")
            
            # Extrai o áudio do vídeo
            print("Extraindo o áudio...")
            video_clip = VideoFileClip(video_path)
            audio_path = os.path.join(output_path_audio, f"{yt.title}.mp3")
            video_clip.audio.write_audiofile(audio_path)
            video_clip.close()
            print("Áudio extraído com sucesso!")
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

window.close()