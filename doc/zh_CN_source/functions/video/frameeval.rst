逐帧求值
=========

.. function:: FrameEval(vnode clip, func eval[, vnode[] prop_src, vnode[] clip_src])
   :module: std

   允许在每帧评估任意函数。函数获取帧号 *n* 作为输入，应返回一个可以请求输出帧的片段。

   *clip* 参数仅用于获取输出格式，因为没有可靠的自动推断方式。

   使用参数 *prop_src* 时，函数还会有一个参数 *f*，包含当前帧。这主要是为了可以访问帧属性并用于决策。注意只有提供了多个 *prop_src* 剪辑时，*f* 才会是一个列表。
   
   *clip_src* 参数仅用于提示 *eval* 函数中引用了哪些剪辑，这可以改善缓存和图生成。鼓励使用但不是必需的。

   此函数可用于完成 Avisynth 中的 Animate、ScriptClip 和所有其他条件滤镜能做的事情。请注意，要修改逐帧属性，应使用 *ModifyFrame*。

   将 BlankClip 从白色逐渐过渡到黑色的示例。
   这是不使用 *prop_src* 参数时最简单的用法::

      import vapoursynth as vs
      import functools

      base_clip = vs.core.std.BlankClip(format=vs.YUV420P8, length=1000, color=[255, 128, 128])

      def animator(n, clip):
         if n > 255:
            return clip
         else:
            return vs.core.std.BlankClip(format=vs.YUV420P8, length=1000, color=[n, 128, 128])

      animated_clip = vs.core.std.FrameEval(base_clip, functools.partial(animator, clip=base_clip))
      animated_clip.set_output()

   简单逐帧自动白平衡示例。
   展示如何访问已计算的帧属性并将其用于条件滤镜::

      import vapoursynth as vs
      import functools
      import math

      def GrayWorld1Adjust(n, f, clip, core):
         small_number = 0.000000001
         red   = f[0].props['PlaneStatsAverage']
         green = f[1].props['PlaneStatsAverage']
         blue  = f[2].props['PlaneStatsAverage']
         max_rgb = max(red, green, blue)
         red_corr   = max_rgb/max(red, small_number)
         green_corr = max_rgb/max(green, small_number)
         blue_corr  = max_rgb/max(blue, small_number)
         norm = max(blue, math.sqrt(red_corr*red_corr + green_corr*green_corr + blue_corr*blue_corr) / math.sqrt(3), small_number)
         r_gain = red_corr/norm
         g_gain = green_corr/norm
         b_gain = blue_corr/norm
         return core.std.Expr(clip, expr=['x ' + repr(r_gain) + ' *', 'x ' + repr(g_gain) + ' *', 'x ' + repr(b_gain) + ' *'])

      def GrayWorld1(clip, matrix_s=None):
         rgb_clip = vs.core.resize.Bilinear(clip, format=vs.RGB24)
         r_avg = vs.core.std.PlaneStats(rgb_clip, plane=0)
         g_avg = vs.core.std.PlaneStats(rgb_clip, plane=1)
         b_avg = vs.core.std.PlaneStats(rgb_clip, plane=2)
         adjusted_clip = vs.core.std.FrameEval(rgb_clip, functools.partial(GrayWorld1Adjust, clip=rgb_clip, core=vs.core), prop_src=[r_avg, g_avg, b_avg])
         return vs.core.resize.Bilinear(adjusted_clip, format=clip.format.id, matrix_s=matrix_s)

      vs.core.std.LoadPlugin(path='BestSource.dll')
      main = vs.core.bs.VideoSource(source='...')
      main = GrayWorld1(main)
      main.set_output()
