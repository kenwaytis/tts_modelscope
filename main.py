from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Union, Optional
from loguru import logger
import json
import base64
import time

from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

app = FastAPI()
class Items(BaseModel):
    text: str
    model_id: str = 'multisp'

model_name = None
model = None

# 加载模型权重
models = {
        #   'multisp':'speech_tts/speech_sambert-hifigan_tts_zh-cn_multisp_pretrain_16k' , # SambertHifigan语音合成-中文-多人预训练-16k
        #   'ainan':'speech_tts/speech_sambert-hifigan_tts_ainan_zh-cn_16k', # 中文-通用领域-16k-发音人ainan
          'zhiya':'damo/speech_sambert-hifigan_tts_zhiya_zh-cn_16k', # 中文-通用领域-16k-发音人zhiya
        #   'aixiang':'speech_tts/speech_sambert-hifigan_tts_aixiang_zh-cn_16k', # 中文-通用领域-16k-发音人aixiang
        #   'zhigui':'damo/speech_sambert-hifigan_tts_zhigui_zh-cn_16k', # 中文-通用领域-16k-发音人zhigui
        #   'zhida':'damo/speech_sambert-hifigan_tts_zhida_zh-cn_16k', # 中文-通用领域-16k-发音人zhida
        #   'zhishuo':'damo/speech_sambert-hifigan_tts_zhishuo_zh-cn_16k', # 中文-通用领域-16k-发音人zhishuo
          'zhimao':'damo/speech_sambert-hifigan_tts_zhimao_zh-cn_16k', # 中文-直播领域-16k-发音人zhimao
          'zhiyue':'damo/speech_sambert-hifigan_tts_zhiyue_zh-cn_16k', # 中文-通用领域-16k-发音人zhiyue
          'zhisha':'damo/speech_sambert-hifigan_tts_zhisha_zh-cn_16k', # 中文-直播领域-16k-发音人zhisha
          'zhiyuan':'damo/speech_sambert-hifigan_tts_zhiyuan_zh-cn_16k', # 中文-通用领域-16k-发音人zhiyuan
          'Zhiyan':'damo/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k', # 中文-多情感领域-16k-发音人Zhiyan
          'Zhitian':'damo/speech_sambert-hifigan_tts_zhitian_emo_zh-cn_16k', # 中文-多情感领域-16k-发音人Zhitian
          'Zhizhe':'damo/speech_sambert-hifigan_tts_zhizhe_emo_zh-cn_16k', # 中文-多情感领域-16k-发音人Zhizhe
          'Zhibei':'damo/speech_sambert-hifigan_tts_zhibei_emo_zh-cn_16k', # 中文-多情感领域-16k-发音人Zhibei
         }

# 根据已有模型选择模型加载
def init_model(model_id):
    if model_id == "":
        logger.error('model_id is empty')
        raise ValueError('model_id is empty')
    elif model_id in models:
        model = pipeline(task=Tasks.text_to_speech, model=models[model_id], device='gpu')
        model_name = models[model_id]
        logger.info('loading model: {%s}'%model_id)
    else:
        logger.error('model_id is not in models')
        raise ValueError('model_id is not in models')
    return model, model_name

# 请求选择到未加载的模型时开始替换模型
def load_model(model_id):
    global model_name, model
    if model_name is None or model_name != models[model_id]:
        model, model_name = init_model(model_id=model_id)
    return model


# TTS返回
@app.post("/tts")
async def tts(items:Items):
    try:
        time1 = time.time()
        text = items.text
        model_id = items.model_id
        logger.info('tts is begining.')
        model = load_model(model_id)
        output = model(input=text)
        wav = output[OutputKeys.OUTPUT_WAV]

        # 音频转换为base64编码传输
        wav = base64.b64encode(wav).decode()
        time2 = time.time()
        consume_time = (time2 - time1)
        result = {"cosume_time":consume_time, "model_id":items.model_id, "model_weight":models[model_id], "wav":wav}
        return result

    except Exception as e:
        errors = str(e)
        mod_errors = errors.replace('"', '**').replace("'", '**')
        logger.error(mod_errors)
        message = {
            "err_no": "400",
            "err_msg": mod_errors
            }
        return message
    
# 检查服务器是否存活
@app.get("/health")
async def health_check():
    try:
        logger.info("health 200")
        return status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# 检查模型推理是否正常
@app.get("/health/inference")
async def health_check():
    try:
        text = '公司围绕以动漫相关业务的基础开展了大量工作，公司具备独立研发制作原创动漫影视作品的技术能力。'
        # 默认发音人‘zhiya’推理
        model_id = 'zhiya'
        load_model(model_id)
        output = load_model(model_id)(input=text)
        logger.info("health 200")
        return status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.on_event("startup")
async def startup_event():
    # Perform initialization or setup tasks here
    logger.info("Application is starting up!")
    try:
        text = '公司围绕以动漫相关业务的基础开展了大量工作，公司具备独立研发制作原创动漫影视作品的技术能力。'
        # 启动服务默认发音人‘zhiya’推理
        model_id = 'zhiya'
        load_model(model_id)
        output = load_model(model_id)(input=text)
        logger.info("{} model load is sucessful!".format(model_id))
        return status.HTTP_200_OK
    except Exception as e:
        logger.info('{} model load is failed!'.format(model_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

