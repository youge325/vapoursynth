普鲁伊特/索贝尔
===================

.. function:: Prewitt(vnode clip[, int[] planes=[0, 1, 2], float scale=1])
   :module: std

   使用 Prewitt 算子创建边缘蒙版。

.. function:: Sobel(vnode clip[, int[] planes=[0, 1, 2], float scale=1])
   :module: std

   使用 Sobel 算子创建边缘蒙版。

   *夹子*
      要处理的片段。必须具有 8 到 16 位之间的整数采样类型，或 32 位的浮点采样类型。如果存在其他格式的帧，将返回错误。

   *飞机*
      指定要处理的平面。未处理的平面将被简单复制。

   *规模*
      输出之前将所有像素乘以比例。这可用于增加或减少输出中边缘的强度。
