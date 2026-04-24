差异化
========

.. function::   MakeDiff(vnode clipa, vnode clipb[, int[] planes])
   :module: std

   计算 *clipa* 和 *clipb* 之间的差异并钳位结果。默认情况下处理所有 *planes*。此函数通常与 *MergeDiff* 一起使用，晚上可用于将差异加回。

   亮度反锐化蒙版：

      blur_clip = core.std.Convolution(clip, matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=[0])
      diff_clip = core.std.MakeDiff(clip, blur_clip, planes=[0])
      sharpened_clip = core.std.MergeDiff(clip, diff_clip, planes=[0])
      
