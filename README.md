# EmotionalChatbot
## 运行准备
1. 安装相关库 `requirements.txt`文件；
2. 选择一个云平台部署语言大模型并实现端口映射（本代码使用AutoDL平台云部署大模型并映射到6006端口）；
3. 在QWen/Qwenapi.py中修改接口设置；
4. 运行以下命令：
```
cd "TTS/vits/monotonic_align"
mkdir monotonic_align
python setup.py build_ext --inplace
cp monotonic_align/*.pyd .
```
## 主要模块介绍
```
ASR ----语音识别模块
Qwen ----语言大模型部分
SentimentEngine ----情感识别部分
TTS  ----语音生成部分
```
为减小硬件使用成本，本次推理全部采用cpu进行，如果使用GPU可在`\TTS\TTService.py`中`TTService`的cpu部分全部改为cuda

完整模型权重可在`https://drive.google.com/file/d/1QZD9DwY_5H6FeFfMm4Q8w941OXWiFWAd/view?usp=sharing`中下载

## 程序运行
克隆UI界面`https://github.com/QSWWLTN/DigitalLife.git`
1. 打开UI界面 `T.exe`
2. 运行`EmotionAi.py`文件
3. 在UI中填写相关信息