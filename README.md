# EmotionalChatbot
## 运行准备
1. 安装相关库 `requirements.txt`文件；
2. 选择一个云平台部署语言大模型并实现端口映射；
3. 在QWen/Qwenapi.py中修改接口设置；
4. 运行以下命令：
```
cd "TTS/vits/monotonic_align"
mkdir monotonic_align
python setup.py build_ext --inplace
cp monotonic_align/*.pyd .
```
## 主要模块介绍
ASR ----语音识别模块
	Qwen ----语言大模型部分
	SentimentEngine ----情感识别部分
	TTS  ----语音生成部分

## 程序运行
1. 打开UI界面 `T.exe`
2. 运行`EmotionAi.py`文件
3. 在UI中填写相关信息