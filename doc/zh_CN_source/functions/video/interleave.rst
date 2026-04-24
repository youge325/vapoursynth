交错合并
==========

.. function::   Interleave(vnode[] clips[, bint extend=0, bint mismatch=0, bint modify_duration=True])
   :module: std

   返回一个帧来自所有 *clips* 交错排列的剪辑。例如，Interleave(clips=[A, B]) 将返回 A.帧 0、B.帧 0、A.帧 1、B.帧...

   *extend* 参数控制是否将所有输入片段视为与最长片段具有相同的长度。

   交错不同格式或维度的片段将被视为错误，除非 *mismatch* 为 true。

   如果设置了 *modify_duration*，则输出剪辑的帧率为第一个输入剪辑的帧率乘以输入剪辑数量。帧时长除以输入剪辑数量。否则使用第一个输入剪辑的帧率。
