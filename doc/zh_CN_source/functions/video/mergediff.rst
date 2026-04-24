合并差异
=========

.. function::   MergeDiff(vnode clipa, vnode clipb[, int[] planes])
   :module: std

   将 *clipb* 中的差异合并回 *clipa* 并钳位结果。默认情况下处理所有 *planes*。此函数通常与 *MakeDiff* 一起使用，晚上通常用于计算差异。

   亮度反锐化蒙版：

      blur_clip = core.std.Convolution(clip, matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=[0])
      diff_clip = core.std.MakeDiff(clip, blur_clip, planes=[0])
      sharpened_clip = core.std.MergeDiff(clip, diff_clip, planes=[0])
      
