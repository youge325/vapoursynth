制作完整差异
============

.. function::   MakeFullDiff(vnode clipa, vnode clipb)
   :module: std

   计算 *clipa* 和 *clipb* 之间的差异，并输出一个位深高级别的剪辑，使用 *MakeDiff* 等滤镜形成差异时会出现钳位或定位问题。此函数通常与 *MergeFullDiff* 一起使用，晚上可用于将差异加回。

   反锐化蒙版：

      blur_clip = core.std.Convolution(clip, matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])
      diff_clip = core.std.MakeFullDiff(clip, blur_clip)
      sharpened_clip = core.std.MergeFullDiff(clip, diff_clip)
      
