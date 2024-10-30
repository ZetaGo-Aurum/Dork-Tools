import os
import sys
import json
import base64
import hashlib
import requests
import subprocess
from cryptography.fernet import Fernet
from PIL import Image
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import socket
import paramiko
import psutil
import speedtest
from googletrans import Translator
from pydub import AudioSegment
import cv2
import face_recognition # type: ignore

class DevTools:
    def __init__(self):
        self.tools = {
            1: self.enkripsi_teks,
            2: self.dekripsi_teks,
            3: self.kompresi_gambar,
            4: self.dekompresi_gambar,
            5: self.analisis_sentimen,
            6: self.terjemahkan_teks,
            7: self.konversi_audio,
            8: self.deteksi_wajah,
            9: self.analisis_jaringan,
            10: self.pemantauan_sistem,
            # ... (tambahkan lebih banyak fungsi di sini)
        }

    def enkripsi_teks(self):
        teks = input("Masukkan teks yang ingin dienkripsi: ")
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_text = f.encrypt(teks.encode())
        print(f"Teks terenkripsi: {encrypted_text}")
        print(f"Kunci: {key}")

    def dekripsi_teks(self):
        encrypted_text = input("Masukkan teks terenkripsi: ").encode()
        key = input("Masukkan kunci: ").encode()
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_text)
        print(f"Teks terdekripsi: {decrypted_text.decode()}")

    def kompresi_gambar(self):
        input_path = input("Masukkan path gambar input: ")
        output_path = input("Masukkan path gambar output: ")
        quality = int(input("Masukkan kualitas kompresi (1-95): "))
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        print("Gambar berhasil dikompresi.")

    def dekompresi_gambar(self):
        input_path = input("Masukkan path gambar input: ")
        output_path = input("Masukkan path gambar output: ")
        with Image.open(input_path) as img:
            img.save(output_path)
        print("Gambar berhasil didekompresi.")

    def analisis_sentimen(self):
        teks = input("Masukkan teks untuk analisis sentimen: ")
        positif = ['baik', 'bagus', 'hebat', 'luar biasa']
        negatif = ['buruk', 'jelek', 'payah', 'mengecewakan']
        
        kata = teks.lower().split()
        skor = sum([1 for k in kata if k in positif]) - sum([1 for k in kata if k in negatif])
        
        if skor > 0:
            print("Sentimen: Positif")
        elif skor < 0:
            print("Sentimen: Negatif")
        else:
            print("Sentimen: Netral")

    def terjemahkan_teks(self):
        teks = input("Masukkan teks yang ingin diterjemahkan: ")
        bahasa_tujuan = input("Masukkan kode bahasa tujuan (mis. 'en' untuk Inggris): ")
        translator = Translator()
        hasil = translator.translate(teks, dest=bahasa_tujuan)
        print(f"Hasil terjemahan: {hasil.text}")

    def konversi_audio(self):
        input_path = input("Masukkan path file audio input: ")
        output_path = input("Masukkan path file audio output: ")
        format_output = input("Masukkan format output (mis. 'mp3', 'wav'): ")
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=format_output)
        print("Konversi audio berhasil.")

    def deteksi_wajah(self):
        image_path = input("Masukkan path gambar: ")
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        print(f"Jumlah wajah terdeteksi: {len(face_locations)}")

    def analisis_jaringan(self):
        st = speedtest.Speedtest()
        print("Mengukur kecepatan download...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        print("Mengukur kecepatan upload...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        print(f"Kecepatan Download: {download_speed:.2f} Mbps")
        print(f"Kecepatan Upload: {upload_speed:.2f} Mbps")

    def pemantauan_sistem(self):
        print(f"Penggunaan CPU: {psutil.cpu_percent()}%")
        print(f"Penggunaan RAM: {psutil.virtual_memory().percent}%")
        print(f"Ruang Disk Tersedia: {psutil.disk_usage('/').free / (1024 * 1024 * 1024):.2f} GB")

    # ... (tambahkan lebih banyak metode di sini)

    def jalankan(self):
        while True:
            print("\nPilih alat yang ingin Anda gunakan:")
            for key, value in self.tools.items():
                print(f"{key}. {value.__name__.replace('_', ' ').capitalize()}")
            print("0. Keluar")

            pilihan = int(input("Masukkan pilihan Anda: "))
            
            if pilihan == 0:
                print("Terima kasih telah menggunakan DevTools!")
                break
            elif pilihan in self.tools:
                self.tools[pilihan]()
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    tools = DevTools()
    tools.jalankan()
