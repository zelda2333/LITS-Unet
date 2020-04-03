# LITS-Unet
数据集LITS2017，基于Unet对肝脏以及肿瘤进行分割。

### prameter.py
主要包括一些路径和其他参数。

### preprocess.py
对数据进行预处理。
包括重采样，windowing,直方图，（中值滤波），获取有效的slice，将2d图片写入h5文件。

