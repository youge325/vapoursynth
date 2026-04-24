音频循环
=========

.. function::   AudioLoop(anode clip[, int times=0])
   :module: std

   返回帧或采样重复播放的片段。如果 *times* 小于 1，片段将重复直到最大片段长度，否则将重复 *times* 次。

   在Python中，std.AudioLoop也可以通过 :ref:`乘法运算符 <pythonreference>` 调用。
