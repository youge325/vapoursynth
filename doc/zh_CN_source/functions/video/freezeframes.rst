冻结帧
============

.. function:: FreezeFrames(vnode clip, int[] first, int[] last, int[] replacement)
   :module: std

   FreezeFrames 将 [*first*,\ *last*] 范围（含）内的所有帧替换为 *replacement*。

   一次 FreezeFrames 调用可以冻结任意数量的范围：

      core.std.FreezeFrames(输入, 第一个=[0, 100, 231], 最后=[15, 112, 300], 替换=[8, 50, 2])

   这将 [0,15] 替换为第 8 帧，[100,112] 替换为第 50 帧，[231,300] 替换为第 2 帧（原始第 2 帧，不是第一个范围替换后的第 2 帧）。

   帧范围不得重叠。
