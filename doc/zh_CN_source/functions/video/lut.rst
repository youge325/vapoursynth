卢特
===

.. function:: Lut(vnode clip[, int[] planes, int[] lut, float[] lutf, func function, int bits, bint floatout])
   :module: std

   对给定剪辑应用查找表。查找表可以指定 2^bits_per_sample 个值的备份，或者作为具有名为 *x* 的参数的 *function* 来值。必须使用 *lut*、*lutf* 或 *function* 之一。查找表将获取 *planes* 中上市的平面，其他平面将简单地不改变地提交。默认情况下处理所有 *planes*。
   
   如果设置了 *floatout*，则输出将是浮点格式，并且需要设置 *lutf* 或 *function* 始终需要返回浮点值。

   如何限制YUV范围（通过供应量）：

   .. code-block:: python

      luty = []
      for x in range(2**clip.format.bits_per_sample):
         luty.append(max(min(x, 235), 16))
      lutuv = []
      for x in range(2**clip.format.bits_per_sample):
         lutuv.append(max(min(x, 240), 16))
      ret = Lut(clip=clip, planes=0, lut=luty)
      limited_clip = Lut(clip=ret, planes=[1, 2], lut=lutuv)

   如何限制YUV范围（使用函数）：

   .. code-block:: python

      def limity(x):
         return max(min(x, 235), 16)
      def limituv(x):
         return max(min(x, 240), 16)
      ret = Lut(clip=clip, planes=0, function=limity)
      limited_clip = Lut(clip=ret, planes=[1, 2], function=limituv)
