二值化/二值化掩模
=====================

.. function:: Binarize(vnode clip[, float[] threshold, float[] v0, float[] v1, int[] planes=[0, 1, 2]])
              BinarizeMask(vnode clip[, float[] threshold, float[] v0, float[] v1, int[] planes=[0, 1, 2]])
   :module: std

   将图像中的每个像素转换为 *v0*（低于 *threshold* 时）或 *v1*。*BinarizeMask* 版本适用于所有具有相同值范围的蒙版片段，仅在 *v0* 和 *v1* 的默认值上有所不同。

   *夹子*
      要处理的片段。必须具有 8 到 16 位之间的整数采样类型，或 32 位的浮点采样类型。如果存在其他格式的帧，将返回错误。

   *临界点*
      默认为格式允许范围的中点。可以为每个平面单独指定。

   *v0*
      低于 *threshold* 的像素所赋的值。可以为每个平面单独指定。默认为格式的下界。

   *v1*
      大于或等于 *threshold* 的像素所赋的值。默认为格式允许的最大值。可以为每个平面单独指定。默认为格式的上界。

   *飞机*
      指定要处理的平面。未处理的平面将被简单复制。
