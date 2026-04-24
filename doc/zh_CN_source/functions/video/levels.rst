级别
======

.. function:: Levels(vnode clip[, float min_in, float max_in, float gamma=1.0, float min_out, float max_out, int[] planes=[0, 1, 2]])
   :module: std

   调整亮度、对比度和伽马值。

   范围 [*min_in*, *max_in*] 被重新映射到 [*min_out*, *max_out*]。注意对于 YUV 浮点格式，范围表现得不太仔细，因为即使对于 UV 平面，指定范围也是 0-1。

   例如，将有限范围YUV转换为全范围（8位）：

      clip = std.Levels(clip, min_in=16, max_in=235, min_out=0, max_out=255, planes=0)
      clip = std.Levels(clip, min_in=16, max_in=240, min_out=0, max_out=255, planes=[1,2])

   *max_in* 和 *max_out* 的默认值分别是格式的最小和最大允许值。注意所有输入都会被钳位到输入范围，以防止超出范围的输出。
   
   .. warning::
      浮点格式的默认范围为 0-1。这可能会对
	  YUV 格式产生不期望的效果。
	  
   *夹子*
      要处理的片段。必须具有 8 到 16 位之间的整数采样类型，或 32 位的浮点采样类型。如果存在其他格式的帧，将返回错误。
      
   *伽玛*
      控制转换的非线性程度。大于 1.0 的值使输出变亮，小于 1.0 的值使其变暗。

   *飞机*
      指定要处理的平面。未处理的平面将被简单复制。
