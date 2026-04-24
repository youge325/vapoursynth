随机播放频道
===============

.. function::   ShuffleChannels(anode[] clips, int[] channels_in, int[] channels_out)
   :module: std

   ShuffleChannels 可以以最通用的方式从不同的片段中提取和组合通道。

   返回片段的大部分属性由指定到 *clips* 的第一个片段隐式确定。

   *clips* 参数接受一个或多个相同格式的片段。如果片段长度不同，将零填充至最后一个片段的长度。

   *channels_in* 参数控制使用输入片段的哪些通道，接受通道常量参数。指定不存在的通道是错误的。如果指定的 *channels_in* 多于 *clips* 值，则 *clips* 列表中的最后一个片段将被中继重源。除了通道常量之外，还可以使用负数来指定第 n 个通道。

   输出通道映射由 *channels_out* 决定，对应输入通道顺序。*channels_out* 通道数必须与 *channels_in* 通道数相同。指定相同的输出通道两次是错误的。
   
   

   以下是一些有用的操作示例。

   提取左声道（假设存在）：

      ShuffleChannels(clips=clip, channels_in=vs.FRONT_LEFT, channels_out=vs.FRONT_LEFT)

   交换立体声片段中的左右声道：

      ShuffleChannels(clips=clip, channels_in=[vs.FRONT_RIGHT, vs.FRONT_LEFT], channels_out=[vs.FRONT_LEFT, vs.FRONT_RIGHT])
      
   交换立体声片段中的左右声道（参数顺序的替代写法）：

      ShuffleChannels(clips=clip, channels_in=[vs.FRONT_LEFT, vs.FRONT_RIGHT], channels_out=[vs.FRONT_RIGHT, vs.FRONT_LEFT])
      
   交换立体声片段中的左右声道（替代索引方式）：

      ShuffleChannels(clips=clip, channels_in=[-2, -1], channels_out=[vs.FRONT_LEFT, vs.FRONT_RIGHT])

   将 2 个单声道音频片段合并为一个立体声片段：

      ShuffleChannels(clips=[clipa, clipb], channels_in=[vs.FRONT_LEFT, vs.FRONT_LEFT], channels_out=[vs.FRONT_LEFT, vs.FRONT_RIGHT])
