双输入查找表
============

.. function:: Lut2(vnode clipa, vnode clipb[, int[] planes, int[] lut, float[] lutf, func function, int bits, bint floatout])
   :module: std

   应用一个考虑两个剪辑像素值的查找表。*lut* 需要包含 2^(clip1.bits_per_sample + clip2.bits_per_sample) 个条目，并将应用于 *planes* 中列出的平面。也可以使用接受 *x* 和 *y* 作为参数的 *function* 来创建查找表。其他平面将不改变地传递。默认情况下处理所有 *planes*。

   Lut2 还接受一个可选的位深参数 *bits*，默认为第一个输入剪辑的位深，用于指定输出剪辑的位深。用户需要自行理解位深转换的影响，特别是从高位深到低位深的转换，因为不会应用缩放或钳位。
   
   如果设置了 *floatout*，则输出将是浮点格式，并且需要设置 *lutf* 或 *function* 始终需要返回浮点值。

   对两个片段求平均的示例：

   .. code-block:: python

      lut = []
      for y in range(2 ** clipy.format.bits_per_sample):
         for x in range(2 ** clipx.format.bits_per_sample):
            lut.append((x + y)//2)
      Lut2(clipa=clipa, clipb=clipb, lut=lut)

   对两个片段求平均并输出 10 位结果的示例：

   .. code-block:: python

      def f(x, y):
         return (x*4 + y)//2
      Lut2(clipa=clipa8bit, clipb=clipb10bit, function=f, bits=10)
