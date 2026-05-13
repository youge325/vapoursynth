预乘
===========

.. function::   PreMultiply(vnode clip, vnode alpha)
   :module: std

   PreMultiply 简单插入 *clip* 和 *alpha* 相乘，渡轮更适合后续操作。在缩放时这会产生更好的结果，带有 alpha 通道的剪辑可以将作为 :doc:`MaskedMerge <maskedmerge>` 的输入。*alpha* 剪辑必须是 *clip* 的对照灰度格式。
   
   注意有限范围预乘内容不包括偏移量。例如，对于 8 位输入，亮度 60 和 alpha 128 的计算方式为 ((60 - 16) * 128)/255 + 16，而不是 (60 * 128)/255。