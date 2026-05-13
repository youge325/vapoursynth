音频混合
========

.. function::   AudioMix(anode[] clips, float[] matrix, int[] channels_out, bint overflow_error = False)
   :module: std

   AudioMix 可以以最通用的方式混合和组合不同片段的通道。

   返回片段的大多数属性由给定到 *clips* 的第一个片段隐式确定。

   *clips* 参数接受一个或多个相同格式的片段。如果片段长度不同，将零填充至最长片段的长度。

   *matrix* 参数将系数应用于每个输入片段的每个通道，通道按其通道常量的数值顺序排列。例如，立体声片段的通道将按 FRONT_LEFT 然后 FRONT_RIGHT 的顺序呈现。

   输出通道和顺序由 *channels_out* 数组决定，输入索引和输出通道之间的映射按从最低到最高的输出通道标识符顺序进行。
   
   如果设置了 *overflow_error*，检测到削波时将停止处理并报错。如果为 false，则会为第一个有削波的音频块打印警告。
   
   

   以下是一些有用的操作示例。

   Downmix stereo audio to mono::

      AudioMix(clips=clip, matrix=[0.5, 0.5], channels_out=[vs.FRONT_CENTER])

   Downmix 5.1 audio::

      AudioMix(clips=clip, matrix=[1, 0, 0.7071, 0, 0.7071, 0, 0, 1, 0.7071, 0, 0, 0.7071], channels_out=[vs.FRONT_LEFT, vs.FRONT_RIGHT])
      
   Copy stereo audio to 5.1 and zero the other channels::

      AudioMix(clips=c, matrix=[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], channels_out=[vs.FRONT_LEFT, vs.FRONT_RIGHT, vs.FRONT_CENTER, vs.LOW_FREQUENCY, vs.BACK_LEFT, vs.BACK_RIGHT])
