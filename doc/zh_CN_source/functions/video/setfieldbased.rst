基于设置字段
=============

.. function:: SetFieldBased(vnode clip, int value)
   :module: std
   
   这是一个方便的函数。如果要设置其他属性，请参见*SetFrameProps*。
   
   SetFieldBased 将 ``_FieldBased`` 设置为 *value* 并删除 ``_Field`` 帧属性。可能的值：
   
      0 = 基于帧（逐行扫描）
      
      1 = 底场优先
      
      2 = 顶场优先
   
   例如，如果你的源素材是逐行的但已编码为隔行，你可以将其设置为基于帧的（非隔行）处理以提高缩放质量::

      clip = core.bs.VideoSource("rule6.mkv")
      clip = core.std.SetFieldBased(clip, 0)
      clip = clip.resize.Bilinear(clip, width=320, height=240)
