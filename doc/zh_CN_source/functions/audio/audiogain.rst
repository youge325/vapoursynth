音频增益
=========

.. function::   AudioGain(anode clip, float[] gain, bint overflow_error = False)
   :module: std

   AudioGain 可以为每个通道指定单独的 *gain* 来改变各个通道的音量，如果只提供一个 *gain* 值则评价所有通道。
   
   允许负*增益*值。使用过大的增益会导致整数格式中的削波。
   
   如果设置了*overflow_error*，检测到削波时将停止处理并报错。如果为false，则为第一个有削波音频的块打印警告。