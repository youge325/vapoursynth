平面重排
=============

.. function::   ShufflePlanes(vnode[] clips, int[] planes, int colorfamily[ vnode prop_src=clips[0]])
   :module: std

   ShufflePlanes 可以以最通用的方式从不同片段中提取和组合平面。这既是优点也是缺点，因为几乎没有错误检查。

   返回片段的大多数属性由给定到 *clips* 的第一个片段隐式确定，但也可以通过使用 *prop_src* 更改。

   *clips* 参数对于具有三个平面的色彩族取一到三个剪辑。在这种情况下 clips=[A] 等同于 clips=[A, A, A]，clips=[A, B] 等同于 clips=[A, B, B]。对于只有一个平面的 GRAY 色彩族，恰好取一个剪辑。

   参数 *planes* 控制使用输入剪辑的哪些平面。从零开始索引。第一个数字指第一个输入剪辑，第二个数字指第二个剪辑，第三个数字指第三个剪辑。

   唯一需要指定的是 *colorfamily*，它控制输出剪辑的色彩族（YUV、RGB、GRAY）。子采样等属性由要组合的给定平面的相对尺寸决定。

   ShufflePlanes 仅在提取单个平面时接受具有可变格式和维度的片段。

   以下是一些有用的操作示例。

   提取索引为 X 的平面。X=0 在 YUV 中表示亮度平面、在 RGB 中表示 R 平面；
   同理，X=1 分别对应 U 与 G 通道::

      ShufflePlanes(clips=clip, planes=X, colorfamily=vs.GRAY)

   Swap U and V in a YUV clip::

      ShufflePlanes(clips=clip, planes=[0, 2, 1], colorfamily=vs.YUV)

   Merge 3 grayscale clips into a YUV clip::

      ShufflePlanes(clips=[Yclip, Uclip, Vclip], planes=[0, 0, 0], colorfamily=vs.YUV)

   Cast a YUV clip to RGB::

      ShufflePlanes(clips=[YUVclip], planes=[0, 1, 2], colorfamily=vs.RGB)
