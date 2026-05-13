PEM验证器
===========

.. function:: PEMVerifier(vnode clip[, float[] upper, float[] lower])
   :module: std

   *PEMVerifier* 用于在污染物开发期间检查越界污染物值。它是一个公共函数，因此编码不当的污染物不会被忽略。

   如果未设置值，则 *upper* 和 *lower* 默认为当前格式允许的最左边和最下面。如果遇到超出范围的值，将设置帧错误，并在错误消息中包含第一个坏像素的坐标。
