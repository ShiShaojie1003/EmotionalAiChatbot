import os
import socket
import time
import logging

import librosa
import soundfile

from utils.FlushingFileHandler import FlushingFileHandler
from ASR import ASRService
from Qwen import Qwenapi
from TTS import TTService
from SentimentEngine import SentimentEngine

console_logger = logging.getLogger()
console_logger.setLevel(logging.INFO)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
console_handler = console_logger.handlers[0]
console_handler.setFormatter(logging.Formatter(FORMAT))
console_logger.setLevel(logging.INFO)
file_handler = FlushingFileHandler("log.log", formatter=logging.Formatter(FORMAT))
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.setLevel(logging.INFO)
console_logger.addHandler(file_handler)
console_logger.addHandler(console_handler)

import subprocess

# 指定exe文件路径
paimonUI = "../Emotional_UI/T.exe"
SSHServe = "./AutoDL-SSH-Tools/AutoDL.exe"



class Server():
    def __init__(self):
        # SERVER STUFF
        self.addr = None
        self.conn = None
        logging.info('正在启动服务')
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 38438
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10240000)
        self.s.bind((self.host, self.port))
        self.tmp_recv_file = 'tmp/server_received.wav'
        self.tmp_proc_file = 'tmp/server_processed.wav'

        ## hard coded character map
        self.char_name = {
            'paimon': ['TTS/models/paimon6k.json', 'TTS/models/paimon6k_390k.pth', 'character_paimon', 1],
        }

        # PARAFORMER
        self.paraformer = ASRService.ASRService('./ASR/resources/config.yaml')

        # CHAT GPT
        self.Qwen = Qwenapi.QwenService()

        # TTS
        self.tts = TTService.TTService(*self.char_name['paimon'])

        # Sentiment Engine
        self.sentiment = SentimentEngine.SentimentEngine('SentimentEngine/models')

    def run(self):
        # MAIN SERVER LOOP
        while True:
            self.s.listen()
            logging.info(f"监听的地址和端口号为： {self.host}:{self.port}...")
            self.conn, self.addr = self.s.accept()
            logging.info(f"已连接到： {self.addr}.")
            # subprocess.run([paimonUI])
            self.conn.sendall(b'%s' % self.char_name['paimon'][2].encode())
            # subprocess.run([SSHServe])
            while True:
                file = self.__receive_file()
                # print('file received: %s' % file)
                with open(self.tmp_recv_file, 'wb') as f:
                    f.write(file)
                    logging.info('输入音频已经接受并保存到本地.')
                ask_text = self.process_voice()
                # logging.info(f"ask_text:{ask_text}")
                resp_text = self.Qwen.ask_stream(ask_text) 
                logging.info(f"输出文本应答为:{resp_text}")
                if resp_text != None:
                    self.send_voice(ask_text,resp_text)
                    self.notice_stream_end()
                
    def notice_stream_end(self):
        time.sleep(1)
        self.conn.sendall(b'stream_finished')

    def send_voice(self, ask_text,resp_text, senti_or = None):
        self.tts.read_save(resp_text, self.tmp_proc_file, self.tts.hps.data.sampling_rate)
        with open(self.tmp_proc_file, 'rb') as f:
            senddata = f.read()
        if senti_or:
            senti = senti_or
        else:
            senti = self.sentiment.infer(ask_text)
        senddata += b'?!'
        senddata += b'%i' % senti
        self.conn.sendall(senddata)
        time.sleep(0.5)
        logging.info('音频已经发送，大小为 %i' % len(senddata))

    def __receive_file(self):
        file_data = b''
        while True:
            data = self.conn.recv(1024)
            # print(data)
            self.conn.send(b'sb')
            if data[-2:] == b'?!':
                file_data += data[0:-2]
                break
            if not data:
                # logging.info('Waiting for WAV...')
                continue
            file_data += data

        return file_data

    def fill_size_wav(self):
        with open(self.tmp_recv_file, "r+b") as f:
            # Get the size of the file
            size = os.path.getsize(self.tmp_recv_file) - 8
            # Write the size of the file to the first 4 bytes
            f.seek(4)
            f.write(size.to_bytes(4, byteorder='little'))
            f.seek(40)
            f.write((size - 28).to_bytes(4, byteorder='little'))
            f.flush()

    def process_voice(self):
        # stereo to mono
        self.fill_size_wav()
        y, sr = librosa.load(self.tmp_recv_file, sr=None, mono=False)
        y_mono = librosa.to_mono(y)
        y_mono = librosa.resample(y_mono, orig_sr=sr, target_sr=16000)
        soundfile.write(self.tmp_recv_file, y_mono, 16000)
        text = self.paraformer.infer(self.tmp_recv_file)

        return text


if __name__ == '__main__':
    s = Server()
    s.run()
