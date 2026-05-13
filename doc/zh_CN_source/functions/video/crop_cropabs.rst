作物/作物抗体
===============

.. function::   Crop(vnode clip[, int left=0, int right=0, int top=0, int bottom=0])  
				CropAbs(vnode clip, int width, int height[, int left=0, int top=0])
   :module: std

   裁剪片段中的帧。

   Crop 是其中最简单的。参数指定从每侧处理多少像素。此函数以前称为 CropRel，仍然是它的别名。

   另一方面，CropAbs比较特殊，因为它可以接受可变帧大小的片段并剪出固定大小的区域，从而使其成为固定大小的片段。

   如果整个画面被裁剪掉、裁剪区域超出输入范围或不满足子采样限制，两个函数都会返回错误。
