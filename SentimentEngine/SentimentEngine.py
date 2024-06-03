import torch
from transformers import BertTokenizer, BertForSequenceClassification
import logging

from transformers import BertTokenizer



class SentimentEngine():
    def __init__(self, model_path):
        logging.info('正在初始化情感分析模块...')
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)

        # 设置模型为推理模式
        self.model.eval()

    def infer(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()

        label_list = ['恐惧','愤怒','厌恶','喜好','悲伤', '高兴','惊讶']
        predicted_label = label_list[predicted_class]
        emotion_labels_str = ', '.join(label_list)
        indices = [1, 2, 5, 0, 3, 0, 4]
        logging.info(f'情感识别为: {predicted_label}')
        logging.info(f'情感得分依次是： {probabilities.tolist()},[{emotion_labels_str}]')
        return indices[predicted_class]
if __name__ == '__main__':
    t = '不许你这样说我，打你'
    s = SentimentEngine('models')
    r = s.infer(t)
    print(r)
