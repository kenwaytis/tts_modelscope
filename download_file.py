from modelscope.hub.snapshot_download import snapshot_download

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

for model_id in models.keys():
    snapshot_download(models[model_id])
