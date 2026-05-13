选择每个
===========

.. function:: SelectEvery(vnode clip, int cycle, int[] offsets[, bint modify_duration=True])
   :module: std

   返回每个 *cycle* 中仅选择部分帧的片段。给定的 *offsets* 必须在 0 到 *cycle* - 1 之间。

   以下是一些有用的操作示例。

   返回偶数编号的帧，从 0 开始：

      SelectEvery(clip=clip, cycle=2, offsets=0)

   返回奇数编号的帧，从 1 开始：

      SelectEvery(clip=clip, cycle=2, offsets=1)

   固定模式 1/5 抽取，每个周期中移除第一帧：

      SelectEvery(clip=clip, cycle=5, offsets=[1, 2, 3, 4])

   复制每第四帧：

      SelectEvery(clip=clip, cycle=4, offsets=[0, 1, 2, 3, 3])

   在Python中，std.SelectEvery也可以通过 :ref:`切片 <pythonreference>` 调用。

   如果设置了*modify_duration*，则剪辑的帧率乘以偏移数量并除以*cycle*。帧时长以相同方式调整。
