合并完全差异
=============

.. function::   MergeFullDiff(vnode clipa, vnode clipb)
   :module: std

   将 *clipb* 中的差异合并回 *clipa*。注意 *clipb* 的位深必须比 *clip* 高等级。此函数通常与 *MakeFullDiff* 一起使用，通常用于计算差异。

   反锐化蒙版：

      blur_clip = core.std.Convolution(clip, matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])
      diff_clip = core.std.MakeFullDiff(clip, blur_clip)
      sharpened_clip = core.std.MergeFullDiff(clip, diff_clip)
      
