修改帧
===========

.. function:: ModifyFrame(vnode clip, clip[] clips, func selector)
   :module: std

   *selector* 函数对每一帧调用，可以修改从 *clips* 获取的某一帧的属性。额外 *clips* 的属性应该只读不修改，因为只能返回一个修改后的帧。

   你必须先复制输入帧，使其可修改。返回的任意帧都必须与 *clip* 拥有相同格式。
   否则会产生错误。如果在某些条件下无需修改当前帧属性，可直接透传该帧。
   传给 selector 的参数为 n（当前帧号）和 f（当只指定一个片段时是单帧，
   指定多个片段时是帧列表）。

   如果你不需要修改帧属性而只是读取它们，你可能应该使用 *FrameEval* 代替。

   将属性 FrameNumber 设置为当前帧号的示例::

      def set_frame_number(n, f):
         fout = f.copy()
         fout.props['FrameNumber'] = n
         return fout
      ...
      ModifyFrame(clip=clip, clips=clip, selector=set_frame_number)

   删除某个属性的示例::

      def remove_property(n, f):
         fout = f.copy()
         del fout.props['FrameNumber']
         return fout
      ...
      ModifyFrame(clip=clip, clips=clip, selector=remove_property)

   将部分属性从一个片段复制到另一个片段的示例
   （clip1 与 clip2 格式相同）::

      def transfer_property(n, f):
         fout = f[1].copy()
         fout.props['FrameNumber'] = f[0].props['FrameNumber']
         fout.props['_Combed'] = f[0].props['_Combed']
         return fout
      ...
      ModifyFrame(clip=clip1, clips=[clip1, clip2], selector=transfer_property)
