文本
====

.. function:: 文本(vnode clip, string text[, int alignment=7, int scale=1])
   :module: text

   文本 是一个简单的文字绘制滤镜。它不依赖任何外部绘图库，
   而是使用内置位图字体：Terminus 的非粗体 8×16 版本。
   字体本身未被修改，仅从 PCF 格式转换为字节数组。

   字体覆盖 Windows-1252，它是 ISO-8859-1（又名 latin1）的超集。不可打印字符会转换为下划线。长行以简单方式换行。最终位置过低而无法放入帧中的行将被静默丢弃。

   *alignment* 参数接受 1 到 9 的数字，对应数字小键盘上按键的位置。

   *scale* 参数为位图字体设置整数缩放因子。

   *ClipInfo*、*CoreInfo*、*FrameNum* 和 *FrameProps* 是基于 *文本* 的便捷函数。
