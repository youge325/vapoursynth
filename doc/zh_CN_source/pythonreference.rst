.. _pythonreference:

Python 参考
================

VapourSynth 分为核心库和 Python 模块。本节解释核心库如何通过 Python 暴露，以及 Python 脚本特有的一些特殊功能，如切片和输出。

.. note::

   通过 vsscript API 执行的任何脚本（即 vspipe、avfs、vsvfw 或其他 API 用户）的 __name__ 将设置为 "__vapoursynth__"，不同于通常为 "__main__" 的普通 Python 脚本。

VapourSynth 结构
#####################

VapourSynth 库中的大多数操作都通过单例核心对象执行。此核心可以加载插件，每个插件都有自己的单元或命名空间，以避免所含函数的命名冲突。因此你可以通过 *core.unit.Function()* 调用插件函数。

所有函数参数名都是小写的，所有函数名都是驼峰命名。单元名也是小写的且通常较短。作为一般规则，记住这一点很有用。

语法
#######

切片和其他语法糖
*********************************

视频Node 和 音频Node 类（实践中总称为"片段"）支持 Python 中完整的索引和切片操作。如果对片段执行切片操作，你将得到一个含有所需帧的新片段。以下是一些示例。

.. csv-table::
   :header: "操作", "描述", "等价形式"
   :widths: 28, 34, 38

   "``clip = clip[5]``", "创建仅包含第 5 帧的单帧片段", "``clip = core.std.Trim(clip, first=5, last=5)``"
   "``clip = clip[5:11]``", "创建包含第 5 到第 10 帧的片段 [#f1]_", "``clip = core.std.Trim(clip, first=5, last=10)`` / ``clip = core.std.AudioTrim(clip, first=5, last=10)``"
   "``clip = clip[::2]``", "选择偶数编号帧", "``clip = core.std.SelectEvery(clip, cycle=2, offsets=0)``"
   "``clip = clip[1::2]``", "选择奇数编号帧", "``clip = core.std.SelectEvery(clip, cycle=2, offsets=1)``"
   "``clip = clip[::-1]``", "反转片段", "``clip = core.std.Reverse(clip)`` / ``clip = core.std.AudioReverse(clip)``"
   "``clip = clip1 + clip2``", "加法运算符可用于拼接片段", "``clip = core.std.Splice([clip1, clip2], mismatch=False)`` / ``clip = core.std.AudioSplice([clip1, clip2])``"
   "``clip = clip * 10``", "乘法运算符可用于循环片段 [#f2]_", "``clip = core.std.Loop(clip, times=10)`` / ``clip = core.std.AudioLoop(clip, times=10)``"

.. [#f1] 请注意，帧号与 Python 数组一样从 0 开始计数，切片的结束值不包含在内

.. [#f2] 请注意，乘以 0 是一个特殊情况，它将重复片段直到达到最大帧数


Filters can be chained with a dot::

   clip = clip.std.Trim(first=100, last=2000).std.FlipVertical()

Which is equivalent to::

   clip = core.std.FlipVertical(core.std.Trim(clip, first=100, last=2000))
   
Python 中的函数参数、返回类型和属性类型推断
**********************************************************************

VapourSynth 内部使用一个非常简单的键值对映射来向函数传递和从函数接收值。因此，每个键实际上是一个单一类型值的一维数组。Python 绑定尽可能地隐藏这一点以减少不便。例如，仅返回单个键的函数将只返回数组本身，而只包含单个值的数组将只返回该单个值。

类似地，函数参数首先被转换为函数参数字符串指定的适当类型，如果无法转换则失败。然而有一个特殊之处，数据类型的类型提示（utf-8/不可打印的原始数据）是根据传递的是 *str* 还是 *bytes*/*bytearray* 对象来设置的。同样，所有 utf-8 提示的数据将返回 *str* 对象，所有其他类型返回 bytes 对象。

帧属性和「任意」类型的函数参数有更严格的类型要求，因为底层类型必须能够从中推断出来。当使用此类函数（如 SetFrameProps）或属性赋值时，可能需要显式转换为 int、float、str 或 bytes 才能正常工作。

Python 关键字作为滤镜参数
***********************************

如果滤镜的参数恰好是 Python 关键字，你可以在调用滤镜时在参数名称后附加下划线。Python 模块会在将所有滤镜参数传递给滤镜之前去除一个尾部下划线（如果存在）。

::

   clip = core.plugin.Filter(clip, lambda_=1)

Another way to deal with such arguments is to place them in a dictionary::

   kwargs = { "lambda": 1 }
   clip = core.plugin.Filter(clip, **kwargs)

VapourSynth 也将支持 PEP8 中使用单个尾部下划线来防止与 Python 关键字冲突的惯例。

Windows 文件路径
******************

如果字符串包含反斜杠，必须在字符串前加 "r" 前缀，或将每个反斜杠重复一次。原因是反斜杠在 Python 中是转义字符。

使用 `os.path.normcase(path) <https://docs.python.org/3/library/os.path.html#os.path.normcase>`_ 修正不正确的路径字符串。

Correct example::

   "B:/VapourSynth/VapourSynth.dll"
   "B:\\VapourSynth\\VapourSynth.dll"
   r"B:\VapourSynth\VapourSynth.dll"

输出
******

指定要输出的剪辑的标准方式是调用 *clip.set_output()*。所有标准 VapourSynth 组件仅使用输出索引 0，vspipe 除外（可配置但默认为 0）。还有其他变量可以设置来控制格式的输出方式。例如，设置 *alt_output=1* 会将 YUV422P10 格式的打包方式更改为专业软件（如 Adobe 产品）中常见的方式。注意目前 *alt_output* 模式仅对 YUV420P8 (I420, IYUV)、YUV422P8 (YUY2, UYVY) 和 YUV422P10 (v210) 有效。

An example on how to get v210 output::

   some_clip = core.resize.Bicubic(clip, format=vs.YUV422P10)
   some_clip.set_output(alt_output=1)

An example on how to get UYVY output::

   some_clip = core.resize.Bicubic(clip, format=vs.YUV422P8)
   some_clip.set_output(alt_output=2)

原始帧数据访问
************************

视频Frame 和 音频Frame 类包含一个图片/音频块及其所有关联的元数据。可以使用 *get_read_ptr(plane)* 或 *get_write_ptr(plane)* 和 *get_stride(plane)* 配合 ctypes 访问原始数据。

还提供了更 Python 友好的封装，可以使用 *frame[plane/channel]* 将每个平面/通道作为 Python 数组访问。

要获取某一帧，只需在片段上调用 *get_frame(n)*。如果你希望遍历片段中的全部帧，可使用以下代码::

   for frame in clip.frames():
       # Do stuff with your frame
       pass

类和函数
#####################

.. py:attribute:: core

   获取单例 Core 对象。如果是首次调用此函数，将使用默认选项实例化 Core。这是引用核心的推荐方式。
   
.. py:function:: get_include()

   返回 VapourSynth 头文件的完整路径。
   
.. py:function:: get_plugin_dir()

   返回自动加载插件目录的完整路径。
   
.. py:function:: get_vsscript()

   返回 VSScript 库的完整路径。

.. py:function:: get_outputs()

   返回当前节点上所有已注册输出的只读映射。

   当注册新输出时，映射将自动更新。

.. py:function:: get_output([index = 0])

   获取先前设置的输出节点。如果索引未设置则抛出错误。对于视频输出将返回包含 *alpha* 和 *alt_output* 设置的 视频输出Tuple，对于音频返回 音频Node。

.. py:function:: clear_output([index = 0])

   清除先前设置的输出片段。

.. py:function:: clear_outputs()

   清除当前环境中所有设置的输出片段。

.. py:function:: construct_signature(signature[, injected=None])

   根据给定的注册签名创建 *inspect.Signature* 对象。

   如果 *injected* 不为 None，签名的第一个参数的默认值将被 injected 提供的值替换。


.. py:function:: register_on_destroy(callback)

   注册一个在脚本结束时调用的回调。这允许你在脚本结束时释放资源。

   每次运行脚本时都必须注册回调，即使代码在多次脚本运行中被重用。

   当脚本已经在完成过程中时，不能注册新的回调。

.. py:function:: unregister_on_destroy(callback)

   取消注册先前添加的回调。

.. py:class:: Core

   *Core* 类使用单例模式。使用 *core* 属性获取实例。所有已加载的插件都作为核心对象的属性公开。这些属性又包含插件中的函数。使用 *plugins()* 获取你可以通过这种方式调用的所有当前已加载插件的完整列表。

   .. py:attribute:: num_threads

      核心使用的并发线程数。可以设置以更改数目。设置为小于 1 的值将默认为硬件线程数。

   .. py:attribute:: max_cache_size

      设置帧缓冲缓存的上限大小，超过此大小后内存将被主动释放。值以兆字节为单位。

   .. py:attribute:: used_cache_size

      核心当前缓存的大小。值以字节为单位。

   .. py:method:: clear_cache()

      释放内部缓存使用的所有内存。在暂停或在多个核心实例之间切换时很有用。

   .. py:attribute:: core_version

      以 VapourSynthVersion 元组形式返回核心版本。

      .. note::

         如果你正在编写库，并且不是从代理获取此信息，你应该考虑使用 *vapoursynth.__version__*，以避免不必要地获取核心和锁定环境。

   .. py:attribute:: api_version

      以 VapourSynthAPIVersion 元组形式返回 API 版本。

      .. note::

         如果你正在编写库，并且不是从代理获取此信息，你应该考虑使用 *vapoursynth.__api_version__*，以避免不必要地获取核心和锁定环境。

   .. py:method:: plugins()

      包含所有已加载的插件。

   .. py:method:: get_video_format(id)

      检索与指定 id 对应的 格式 对象。如果 *id* 无效则返回 None。

   .. py:method:: query_video_format(color_family, sample_type, bits_per_sample, subsampling_w, subsampling_h)

      检索与格式信息对应的 格式 对象。无效的格式将引发异常。

   .. py:method:: create_video_frame(format, width, height)

      创建一个具有给定尺寸和格式的未初始化平面的新帧。此函数可以在帧回调内安全调用。

   .. py:method:: add_log_handler(handler_func)

      安装一个自定义处理程序来处理 VapourSynth 发出的各种错误消息。消息处理程序目前是全局的，即按进程而非每个 VSCore 实例。返回一个 LogHandle 对象。*handler_func* 是形如 *func(MessageType, message)* 的回调函数。

   .. py:method:: remove_log_handler(handle)

      删除自定义处理器。

   .. py:method:: log_message(message_type, message)

      通过 VapourSynth 的日志框架发送消息。

   .. py:method:: rule6()

      非法行为检测。

.. py:class:: Local

   在内部，可以有多个核心。这通常是预览器应用程序的情况。使用此类来存储依赖于当前活动核心的变量。

   .. code::

        l = Local()
        l.test = 1


.. py:class:: 视频Node

   表示一个视频片段。该类本身支持索引与切片，可执行 trim、reverse 和 selectevery 操作。
   视频Node 还定义了多个运算符：加法用于拼接片段，乘法用于重复片段。
   请注意，切片与索引总是返回新的 视频Node 对象，而不是 视频Frame。

   .. py:attribute:: format

      描述帧数据的 格式 对象。如果格式可以在帧之间变化，此值为 None。

   .. py:attribute:: width

      视频的宽度。如果宽度和高度可以在帧之间变化，此值为 0。

   .. py:attribute:: height

      视频的高度。如果宽度和高度可以在帧之间变化，此值为 0。

   .. py:attribute:: num_frames

      片段中的帧数。

   .. py:attribute:: fps

      以 *Fraction* 表示的帧率。当片段具有可变帧率时为 0/1。

      .. py:attribute:: numerator

         帧率的分子。如果片段具有可变帧率，值为 0。

      .. py:attribute:: denominator

         帧率的分母。如果片段具有可变帧率，值为 0。

   .. py:attribute:: fps_num

      已弃用，请使用 *fps.numerator* 代替

   .. py:attribute:: fps_den

      已弃用，请使用 *fps.denominator* 代替

   .. py:attribute:: flags

      为此片段设置的特殊标志。通常应忽略此属性。

   .. py:method:: get_frame(n)

      从位置 *n* 返回一个 视频Frame。

   .. py:method:: get_frame_async(n)

      返回一个 concurrent.futures.Future 对象，其结果将是一个 视频Frame 实例，或设置渲染帧时抛出的异常。

      *future 将始终处于运行中或已完成状态*

   .. py:method:: get_frame_async(n, cb: callable)
      :noindex:

      在另一个线程中渲染帧。当帧渲染完成时，成功时调用 `cb(Frame, None)`，失败时调用 `cb(None, Exception)`。

      新增：R58

   .. py:method:: set_output(index = 0, alpha = None, alt_output = 0)

      设置剪辑可供输出访问。这是指定要输出的剪辑的标准方式。所有 VapourSynth 工具（vsvfw、vsfs、vspipe）使用索引 *index* 0 的剪辑。可以同时指定一个额外的包含 *alpha* 的剪辑用于输出。目前只有 vspipe 在输出时考虑 *alpha*。*alt_output* 参数用于可选的替代输出模式。目前它控制某些格式在 VFW 风格输出时使用的 FOURCC。

   .. py:method:: output(fileobj[, y4m = False, progress_update = None, prefetch = 0, backlog=-1])

      将整个剪辑写入指定的文件句柄。可以通过指定 *sys.stdout* 作为文件来管道输出到标准输出。当 *y4m* 为 true 时会添加 YUV4MPEG2 头。可以通过将形如 *func(current_frame, total_frames)* 的回调函数传递给 *progress_update* 来报告当前进度。*prefetch* 参数仅用于调试目的，不应更改。*backlog* 参数仅用于调试目的，不应更改。

   .. py:method:: frames([prefetch=None, backlog=None, close=False])

      返回片段中所有 视频Frame 的生成器迭代器。它将并发渲染多个帧。

      *prefetch* 参数定义并发渲染的帧数。仅用于调试目的，不应更改。*backlog* 参数定义 VapourSynth 在停止渲染额外帧之前最多缓冲多少未消费的帧（包括尚未完成渲染的帧）。此参数用于限制此函数存储帧的内存使用。*close* 参数决定每次迭代步骤后是否关闭帧。默认为 false 以保持向后兼容。

   .. py:method:: clear_cache()

      释放此节点内部缓存使用的所有内存。

   .. py:method:: is_inspectable(version=None)
   
      如果你可以使用给定版本的节点检查 API，则返回真值。Python 检查 API 是有版本控制的，因为在撰写本文时底层 API 不稳定。每次 Python API 更改时版本号都会递增。只要 API 被标记为不稳定，就不会尝试保持向后兼容。

      此方法可能永远不返回真值。

      这是当前检查 API 实现中唯一稳定的函数。

      .. note::

         请注意，内省功能必须由后端环境手动启用。不在 vspipe 或其他编辑器内运行的独立 Python 脚本会自动启用内省功能。

      .. warning::

         图检查 API 是不稳定的。因此省略版本参数将始终返回 None。

      当前不稳定的 Python 图检查 API 版本为 0。

      新增：R58

      :param version: 如果为 None，将使用最后一个稳定 API 的版本号。

.. py:class:: 视频输出Tuple

      如果输出是视频，get_output 将返回此类。

      .. py:attribute:: clip

         包含颜色平面的 视频Node 实例。

      .. py:attribute:: alpha

         包含 alpha 平面的 视频Node 实例。

      .. py:attribute:: alt_output

         要使用的替代输出模式的整数。如果没有有意义的映射可能会被忽略。

.. py:class:: 视频Frame

      此类表示一个视频帧及其所有附加的元数据。

   .. py:attribute:: format

      描述帧数据的 格式 对象。

   .. py:attribute:: width

      帧的宽度。

   .. py:attribute:: height

      帧的高度。

   .. py:attribute:: readonly

      如果 *readonly* 为 True，帧数据和属性不能被修改。

   .. py:attribute:: props

      此属性以字典形式保存帧的所有属性。为兼容旧脚本，这些属性也会映射为子属性。
      更多信息请参见：
      参考链接：`API Reference <apireference.html#reserved-frame-properties>`_
      注意：其中包含 matrix、transfer 和 primaries（_Matrix、_Transfer、_Primaries）数据。
      更多信息请参见 `Resize <functions/resize.html>`_。

   .. py:method:: copy()

      返回帧的可写副本。

   .. py:method:: close()

      强制释放帧。释放后，你不能在帧上调用任何函数，也不能使用关联的 FrameProps。

      为避免忘记关闭帧，帧对象实现为上下文管理器，会自动调用该方法：

      .. code::

           with core.std.BlankClip().get_frame(0) as f:
               print(f.props)

   .. py:attribute:: closed

      告诉你帧是否已关闭。如果尚未调用 close() 方法，它将为 False。

   .. py:method:: get_read_ptr(plane)

      返回指向原始帧数据的指针。数据不可修改。注意这是底层 C API 的薄封装，因此调用 *get_write_ptr*（包括 Python 绑定中其他函数内部进行的调用）可能会使之前通过 *get_read_ptr* 获取的帧指针失效。

   .. py:method:: get_write_ptr(plane)

      返回指向原始帧数据的指针。可以使用 ctypes 或其他类似的 Python 包进行修改。注意这是底层 C API 的薄封装，因此调用 *get_write_ptr*（包括 Python 绑定中其他函数内部进行的调用）可能会使之前通过 *get_read_ptr* 获取的帧指针失效。

   .. py:method:: get_stride(plane)

      返回 *plane* 中每行之间的跨度。

   .. py:method:: readchunks()

      此方法通常用于将 视频Frame 的内容转储到磁盘。返回的生成器产生 视频Frame 内存的连续块。

      .. code::
      
         with open('output.raw', 'wb') as file:
            with vs.core.std.BlankClip(color=[25, 50, 60]).get_frame(0) as f:
               for chunk in f.readchunks():
                  file.write(chunk)

      .. note::
         通常，帧内容将保存在连续数组中，此方法将产生 *n_planes* 个数据块，每个包含整个平面。但不要将此视为理所当然，因为这可能不是这种情况，你将改为迭代平面数据的行，这些行保证是连续的。
         
         如果你想安全地读取整个平面，请使用 frame[plane_idx] 获取平面的 memoryview。

.. py:class:: 视频格式

   此类表示描述帧格式所需的所有信息。它保存通用颜色类型、子采样、平面数量等。名称直接映射到 C API，因此请查阅 C API 以获取更详细的信息。

   .. py:attribute:: id

      标识格式的唯一 *id*。

   .. py:attribute:: name

      格式的人类可读名称。

   .. py:attribute:: color_family

      格式描述的色彩空间组。

   .. py:attribute:: sample_type

      格式是基于整数还是浮点数。

   .. py:attribute:: bits_per_sample

      一个平面中存储一个采样使用多少位。

   .. py:attribute:: bytes_per_sample

      为了效率，实际存储被填充到 2^n 字节。

   .. py:attribute:: subsampling_w

      第二和第三平面在水平方向上的子采样。

   .. py:attribute:: subsampling_h

      第二和第三平面在垂直方向上的子采样。

   .. py:attribute:: num_planes

      格式的平面数。

   .. py:method:: replace(core=None, **kwargs)

      返回应用给定修改后的新格式。

      唯一支持替换的属性是 `color_family`、`sample_type`、`bits_per_sample`、`subsampling_w`、`subsampling_h`。

      可选的 `core` 参数定义新格式应在哪个核心上注册。这通常不需要，默认为当前环境的核心。

.. py:class:: 音频Node

   表示一个音频片段。该类本身支持索引与切片，可执行 trim、reverse 和 selectevery 操作。
   音频Node 也定义了多个运算符：加法用于拼接片段，乘法用于重复片段。
   请注意，切片与索引总是返回新的 音频Node 对象，而不是 音频Frame。

   .. py:attribute:: sample_type

      格式是基于整数还是浮点数。

   .. py:attribute:: bits_per_sample

      一个平面中存储一个采样使用多少位。

   .. py:attribute:: bytes_per_sample

      为了效率，实际存储被填充到 2^n 字节。

   .. py:attribute:: channel_layout

      已使用通道的掩码。

   .. py:attribute:: num_channels

      格式的通道数。

   .. py:attribute:: sample_rate

      播放采样率。

   .. py:method:: get_frame(n)

      从位置 *n* 返回一个 音频Frame。

   .. py:method:: get_frame_async(n)

      返回一个 concurrent.futures.Future 对象，其结果将是一个 音频Frame 实例，或设置渲染帧时抛出的异常。

      *future 将始终处于运行中或已完成状态*

   .. py:method:: set_output(index = 0)

      设置片段以供输出。

   .. py:method:: output(fileobj[, wav = False, w64 = False, progress_update = None, prefetch = 0, backlog=-1])

      将整个音频写入指定的文件句柄。可以通过指定 *sys.stdout* 作为文件来管道输出到标准输出。可以通过分别启用 *wav* 或 *w64* 来写入 WAV 或 WAVE64 头；这些选项互斥。可以通过将形如 *func(current_frame, total_frames)* 的回调函数传递给 *progress_update* 来报告当前进度。*prefetch* 参数仅用于调试目的，不应更改。*backlog* 参数仅用于调试目的，不应更改。

      新增：R74

   .. py:method:: frames([prefetch=None, backlog=None, close=False])

      返回片段中所有 音频Frame 的生成器迭代器。它将并发渲染多个帧。

      *prefetch* 参数定义并发渲染帧数，仅用于调试场景，通常无需修改。
      *backlog* 参数定义 VapourSynth 在停止渲染更多帧前最多可缓存多少未消费帧（包括尚未渲染完成的帧），用于限制该函数的内存占用。
      *close* 参数决定每次迭代后是否关闭帧。默认为 false，以保持向后兼容。

   .. py:method:: clear_cache()

      释放此节点内部缓存使用的所有内存。

   .. py:method:: is_inspectable(version=None)
   
      如果给定版本可用于节点检查 API，则返回真值。
      Python inspection API 采用版本化设计，因为在撰写本文时底层 API 仍不稳定。
      每当 Python API 发生变化，版本号都会递增。
      只要该 API 仍标记为不稳定，就不会保证向后兼容。

      此方法可能永远不返回真值。

      这是当前检查 API 实现中唯一稳定的函数。

      .. note::

         请注意，内省功能必须由宿主环境手动启用。
         不在 vspipe 或其他编辑器中运行的独立 Python 脚本会自动启用内省功能。

      .. warning::

         图检查 API 仍不稳定，因此省略版本参数将始终返回 None。

      当前不稳定的 Python 图检查 API 版本为 0。

      新增：R58

      :param version: 如果为 None，将使用最后一个稳定 API 的版本号。


.. py:class:: 音频Frame

      此类表示一个音频帧及其所有附加的元数据。

   .. py:attribute:: sample_type

      格式是基于整数还是浮点数。

   .. py:attribute:: bits_per_sample

      一个平面中存储一个采样使用多少位。

   .. py:attribute:: bytes_per_sample

      为了效率，实际存储被填充到 2^n 字节。

   .. py:attribute:: channel_layout

      已使用通道的掩码。

   .. py:attribute:: num_channels

      格式的通道数。

   .. py:attribute:: readonly

      如果 *readonly* 为 True，帧数据和属性不能被修改。

   .. py:attribute:: props

      此属性以字典形式保存帧的所有属性。注意音频帧属性作为音频的概念相当不合理，因为任意数量的采样被混在一起且很少使用。

   .. py:method:: copy()

      返回帧的可写副本。

   .. py:method:: get_read_ptr(plane)

      返回指向原始帧数据的指针。数据不可修改。

   .. py:method:: get_write_ptr(plane)

      返回指向原始帧数据的指针。可以使用 ctypes 或其他类似的 Python 包进行修改。

   .. py:method:: get_stride(plane)

      返回 *plane* 中每行之间的跨度。

.. py:class:: Plugin

   Plugin 是表示已加载插件及其命名空间的类。

   .. py:attribute:: namespace

      插件的命名空间。

   .. py:attribute:: name

      插件的名称字符串。
      
   .. py:attribute:: version

      以 PluginVersion 元组形式返回的插件版本。
      
   .. py:attribute:: plugin_path

      插件的主库位置。请注意，内部函数没有插件路径，返回 None。

   .. py:attribute:: identifier

   .. py:method:: functions()

      包含插件中的所有函数，你可以通过调用 *core.<命名空间>.functions()* 访问。

.. py:class:: Function

   Function 是 VapourSynth 插件提供的函数的简单封装类。其主要用途就是被调用，仅此而已。

   .. py:attribute:: name

      函数名称。与注册函数时使用的字符串相同。

   .. py:attribute:: plugin

      函数所属的 *Plugin* 对象。

   .. py:attribute:: signature

      原始函数签名字符串。与注册函数时使用的字符串相同。

   .. py:attribute:: return_signature

      原始函数签名字符串。与注册函数时使用的返回类型字符串相同。

.. py:class:: Environment

   此类表示一个环境。

   一些编辑器允许在同一进程内运行多个 vsscript，每个脚本都有独立的 Core 实例和输出集合。
   每个 Core 实例及其对应输出共同构成一个独立环境。

   在任何给定时间，同一上下文中只能有一个环境处于活动状态。此类允许对环境进行内省并允许随意切换。

   .. code::

        env = get_current_environment()
        # sometime later
        with env.use():
          # Do stuff inside this env.

   .. py:function:: is_single()

      若脚本不在 vsscript 环境中运行则返回 True；
      若在 vsscript 环境中运行则返回 False。

   .. py:attribute:: env_id

      如果脚本不在 vsscript 环境中运行，返回 -1。否则返回当前环境 ID。

   .. py:attribute:: single

      参见 is_single()

   .. py:attribute:: alive

      环境是否已被底层应用程序销毁？

   .. py:method:: copy()

      创建环境对象的副本。

      新增：R51

   .. py:method:: use()

      返回一个上下文管理器，在 with 语句包围的代码块中启用给定环境，并在 with 代码块结束后恢复到之前定义的环境。

      .. code::

         env = get_current_environment()
         with env.use():
             with env.use():
                 pass

      新增：R51

.. py:function:: get_current_environment()

   返回一个表示脚本当前运行环境的 Environment 对象。如果在使用 vsscript 时当前不在任何脚本环境中，将抛出错误。

   此函数适用于使用 vsscript 的基于 Python 的编辑器。

   新增：R51

.. py:class:: EnvironmentPolicy

   此类旨在由自定义脚本运行器和编辑器进行子类化。普通用户不需要此类。这里实现的大多数方法在此模块的其他部分都有对应的 API。

   此类的实例控制在当前上下文中激活哪个环境。「上下文」的确切含义由具体的 EnvironmentPolicy 定义。环境由 :class:`EnvironmentData` 对象表示。

   要使用此类，首先创建一个子类，然后使用 :func:`register_policy` 让 VapourSynth 使用你的策略。这必须在首次使用 VapourSynth 之前完成。如果需要，VapourSynth 会自动注册一个内部策略。子类必须是可弱引用的！

   一旦调用了 :meth:`on_policy_registered` 方法，策略就负责创建和管理环境。

   已做出特殊考虑以确保类的函数不会被滥用。你无法自行获取当前运行的策略。"on_policy_registered" 暴露的额外 API 仅在策略已注册时有效。一旦策略被注销，所有对额外 API 的调用都将失败并抛出 RuntimeError。

   新增：R51

   .. py:method:: on_policy_registered(special_api)

      此方法在策略成功注册后调用。它提供了额外的内部方法，这些方法是隐藏的，因为除非你实现自己的策略，否则它们是无用的甚至有害的。

      :param special_api: 这是一个暴露额外 API 的 :class:`EnvironmentPolicyAPI` 对象

   .. py:method:: on_policy_cleared()

      此方法在 Python 进程退出或环境策略调用 unregister_policy 时调用。这允许策略释放所使用的资源。

   .. py:method:: get_current_environment()

      此方法由模块调用以检测当前上下文中正在运行的环境。如果返回 None，表示当前没有活动的环境。

      :returns: 表示当前上下文中当前活动环境的 :class:`EnvironmentData` 对象。

   .. py:method:: set_environment(environment)

      此方法由模块调用以更改当前活动的环境。如果向此函数传递 None，策略可以切换到它选择的另一个环境。

      注意：该函数负责检查环境是否存活。若传入的是已失活环境，应按传入 None 的行为处理，而不应抛出错误。

      :param environment: 要在当前上下文中启用的 :class:`EnvironmentData`。
      :returns: 之前启用的环境。

   .. py:method:: is_alive(environment)

      当前环境是否仍由策略管理并处于活动状态。

      默认实现检查是否已在环境上调用 `EnvironmentPolicyAPI.destroy_environment`。


.. py:class:: EnvironmentPolicyAPI

   此类旨在由自定义脚本运行器和编辑器使用。此类的实例公开了额外的 API。方法绑定到特定的 :class:`EnvironmentPolicy` 实例，仅在策略当前已注册时有效。

   新增：R51

   .. py:method:: wrap_environment(environment)

      创建绑定到传入环境 ID 的新 :class:`Environment` 对象。

      .. warning::

         此函数不检查 id 是否对应于活动环境，因为调用者应该知道哪些环境是活动的。

   .. py:method:: create_environment(flags = 0)

      返回一个 :class:`Environment`，用于 VapourSynth 使用的上下文敏感数据的封装。例如，它保存当前活动的核心对象以及当前注册的输出。

   .. py:method:: set_logger(environment, callback)

      此函数为给定环境设置日志记录器。

      该 logger 是一个回调函数，接收两个参数：Level（vs.MessageType 的实例）以及包含日志消息的字符串。

   .. py:method:: destroy_environment(environment)

      将环境标记为已销毁。不使用此函数的旧环境策略实现仍然有效。

      必须覆盖 EnvironmentPolicy.is_alive 或使用此方法将环境标记为已销毁。

      新增：R52

   .. py:method:: unregister_policy()

      取消注册绑定的策略，并允许注册另一个策略。

   .. py:method:: get_vapoursynth_api(version)

      将 getVapoursynthAPI 暴露给 Python。返回 ctypes.c_void_p。

      此函数的访问权限是临时的，如果滥用可能会被移除。

      新增：R62

   .. py:method:: get_core_ptr(environment)

      返回指向驱动环境的 `Core*` 对象的 ctypes.c_void_p。

      此函数的访问权限是临时的，如果滥用可能会被移除。

      新增：R62

.. py:function:: register_policy(policy)

   此函数旨在由自定义脚本运行器和编辑器使用。它安装你的自定义 :class:`EnvironmentPolicy`。此函数仅在没有安装其他策略时有效。

   如果未安装策略，第一个环境敏感的调用将自动注册一个内部策略。

   新增：R50

   .. note::

      This must be done before VapourSynth is used in any way. Here is a non-exhaustive list that automatically register a policy:

      * 使用 "VSScript.h" 中的 "vsscript_init"
      * 使用 :func:`get_outputs`
      * 使用 :func:`get_output`
      * 使用 :func:`clear_output`
      * 使用 :func:`clear_outputs`
      * 使用 :func:`get_current_environment`
      * 访问 :attr:`core` 的任何属性


.. py:function:: _try_enable_introspection(version=None)

   尝试启用内省。成功则返回 true。

   :param version: 如果不传入将使用最新的稳定内省 API。

   新增：R58

.. py:function:: has_policy()

   此函数旨在由自定义脚本运行器和编辑器使用。此函数检查是否已安装 :class:`EnvironmentPolicy`。

   新增：R50

.. py:class:: EnvironmentData

   存储 VapourSynth 所需的上下文敏感数据的内部类。它是一个不透明对象，你无法直接访问其属性。

   普通用户无法获取此对象的实例。只有在使用 EnvironmentPolicy 时才会遇到 EnvironmentData 对象。

   此对象是可弱引用的，这意味着你可以在环境数据对象实际被释放时获得回调（即没有其他对象持有环境数据的实例）。

   新增：R50

.. py:class:: Func

   Func 是 VapourSynth VSFunc 对象的简单包装类。其主要目的是被调用和管理引用计数。

.. py:exception:: Error

   标准异常类。VapourSynth 中遇到的大多数错误都会抛出此异常。

常量
#########

视频
*****

色彩族
------------

色彩族常量描述了格式组以及其颜色信息存储的基本方式。你应该熟悉所有这些，也许 *YCOCG* 和 *COMPAT* 除外。后者是非平面格式的特殊杂项类别。以下是模块中声明的常量::

   UNDEFINED
   RGB
   YUV
   GRAY

格式
------

格式常量精确描述一种格式。所有常见甚至更不常见的格式都有预定义的便捷常量，因此实际上没有人真正需要注册自己的格式。这些值主要由缩放器用于指定要转换到的格式。命名系统非常简单：首先是色彩族，然后是子采样（只有 YUV 有），最后是一个平面中每个采样的位数。此规则的例外是 RGB，它将所有 3 个平面的位数加在一起。完整的值列表::

   NONE
   GRAY8
   GRAY9
   GRAY10
   GRAY12
   GRAY14
   GRAY16
   GRAY32
   GRAYH
   GRAYS
   YUV420P8
   YUV422P8
   YUV444P8
   YUV410P8
   YUV411P8
   YUV440P8
   YUV420P9
   YUV422P9
   YUV444P9
   YUV420P10
   YUV422P10
   YUV444P10
   YUV420P12
   YUV422P12
   YUV444P12
   YUV420P14
   YUV422P14
   YUV444P14
   YUV420P16
   YUV422P16
   YUV444P16
   YUV444PH
   YUV444PS
   RGB24
   RGB27
   RGB30
   RGB36
   RGB42
   RGB48
   RGBH
   RGBS

色度位置
---------------

::

   CHROMA_LEFT
   CHROMA_CENTER
   CHROMA_TOP_LEFT
   CHROMA_TOP
   CHROMA_BOTTOM_LEFT
   CHROMA_BOTTOM

场模式
-----------

::

   FIELD_PROGRESSIVE
   FIELD_TOP
   FIELD_BOTTOM

范围
-----------

::

   RANGE_FULL
   RANGE_LIMITED

矩阵系数
-------------------

::

   MATRIX_RGB
   MATRIX_BT709
   MATRIX_UNSPECIFIED
   MATRIX_FCC
   MATRIX_BT470_BG
   MATRIX_ST170_M
   MATRIX_ST240_M
   MATRIX_YCGCO
   MATRIX_BT2020_NCL
   MATRIX_BT2020_CL
   MATRIX_CHROMATICITY_DERIVED_NCL
   MATRIX_CHROMATICITY_DERIVED_CL
   MATRIX_ICTCP

传输特性
-----------------------

::

   TRANSFER_BT709
   TRANSFER_UNSPECIFIED
   TRANSFER_BT470_M
   TRANSFER_BT470_BG
   TRANSFER_BT601
   TRANSFER_ST240_M
   TRANSFER_LINEAR
   TRANSFER_LOG_100
   TRANSFER_LOG_316
   TRANSFER_IEC_61966_2_4
   TRANSFER_IEC_61966_2_1
   TRANSFER_BT2020_10
   TRANSFER_BT2020_12
   TRANSFER_ST2084
   TRANSFER_ST428
   TRANSFER_ARIB_B67

色域原色
---------------

::

   PRIMARIES_BT709
   PRIMARIES_UNSPECIFIED
   PRIMARIES_BT470_M
   PRIMARIES_BT470_BG
   PRIMARIES_ST170_M
   PRIMARIES_ST240_M
   PRIMARIES_FILM
   PRIMARIES_BT2020
   PRIMARIES_ST428
   PRIMARIES_ST431_2
   PRIMARIES_ST432_1
   PRIMARIES_EBU3213_E

音频
*****

通道
--------

::

   FRONT_LEFT
   FRONT_RIGHT
   FRONT_CENTER
   LOW_FREQUENCY
   BACK_LEFT
   BACK_RIGHT
   FRONT_LEFT_OF_CENTER
   FRONT_RIGHT_OF_CENTER
   BACK_CENTER
   SIDE_LEFT
   SIDE_RIGHT
   TOP_CENTER
   TOP_FRONT_LEFT
   TOP_FRONT_CENTER
   TOP_FRONT_RIGHT
   TOP_BACK_LEFT
   TOP_BACK_CENTER
   TOP_BACK_RIGHT
   STEREO_LEFT
   STEREO_RIGHT
   WIDE_LEFT
   WIDE_RIGHT
   SURROUND_DIRECT_LEFT
   SURROUND_DIRECT_RIGHT
   LOW_FREQUENCY2

采样类型
***********

::

   INTEGER
   FLOAT
