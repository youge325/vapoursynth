VSHelper4.h（辅助头文件）
===========================

目录
#################

简介_


宏_
   VSH_STD_PLUGIN_ID_（内置 std 插件 ID）
   
   VSH_RESIZE_PLUGIN_ID_（内置 resize 插件 ID）
   
   VSH_TEXT_PLUGIN_ID_（内置 text 插件 ID）

   VS_RESTRICT_（restrict 可移植宏）

   `VSH_ALIGNED_MALLOC <VSH_ALIGNED_MALLOC_c_>`_ （对齐分配宏）

   `VSH_ALIGNED_FREE <VSH_ALIGNED_FREE_c_>`_ （对齐释放宏）

   VSMIN_（取最小值）

   VSMAX_（取最大值）


函数_
   `vsh_aligned_malloc <vsh_aligned_malloc_cpp_>`_ （C++ 对齐分配）

   `vsh_aligned_free <vsh_aligned_free_cpp_>`_ （C++ 对齐释放）

   isConstantVideoFormat_（检查恒定视频格式）

   isSameVideoFormat_（检查视频格式一致）
   
   isSameVideoPresetFormat_（检查与预设格式一致）
   
   isSameVideoInfo_（检查视频信息一致）
   
   isSameAudioFormat_（检查音频格式一致）

   isSameAudioInfo_（检查音频信息一致）

   muldivRational_（有理数乘除并约分）

   addRational_（有理数相加并约分）

   reduceRational_（有理数约分）

   int64ToIntS_（有符号饱和转换）
   
   doubleToFloatS_（double 到 float 转换）

   bitblt_（平面内存复制）

   areValidDimensions_（检查尺寸合法性）


简介
############

这是一组有用的宏和函数。请注意，所有函数（非宏）在 C 模式下以 `vsh_` 为前缀，或在 C++ 中放在 `vsh` 命名空间中。本文档将使用这些函数的 C++ 名称。


宏
######

VSH_STD_PLUGIN_ID
-----------------
定义为内部 std 插件 ID 的宏，为方便而提供。


VSH_RESIZE_PLUGIN_ID
--------------------
定义为内部缩放器插件 ID 的宏，为方便而提供。


VSH_TEXT_PLUGIN_ID
------------------
定义为内部 std 插件 ID 的宏，为方便而提供。


VS_RESTRICT
-----------

尝试提供 C99 ``restrict`` 关键字或其 C++ 对应物的可移植定义。


.. _vsh_aligned_malloc_c:

VSH_ALIGNED_MALLOC
------------------

VSH_ALIGNED_MALLOC(pptr, size, alignment)

在 Windows 上扩展为 _aligned_malloc()，在其他平台上扩展为 posix_memalign()。注意参数风格为 posix_memalign()。

*pptr* 是指向指针的指针。


.. _vsh_aligned_free_c:

VSH_ALIGNED_FREE
----------------

VSH_ALIGNED_FREE(ptr)

在 Windows 上扩展为 _aligned_free()，在其他平台上扩展为 free()。

*ptr* 是一个指针。


VSMIN
-----

VSMIN(a, b)

返回两个数中的较小值。


VSMAX
-----

VSMAX(a, b)

返回两个数中的较大值。


函数
#########

.. _vsh_aligned_malloc_cpp:

vsh_aligned_malloc
------------------

.. cpp:function:: T* vsh::vsh_aligned_malloc(size_t size, size_t alignment)

   C++ 的模板化对齐 malloc。它使用与 `VSH_ALIGNED_MALLOC <VSH_ALIGNED_MALLOC_c_>`_ 宏相同的函数，但更易于使用。


.. _vsh_aligned_free_cpp:

vsh_aligned_free
----------------

.. cpp:function:: void vsh::vsh_aligned_free(void *ptr)

   这只是使用 `VSH_ALIGNED_FREE <VSH_ALIGNED_FREE_c_>`_ 宏。


isConstantVideoFormat
---------------------

.. cpp:function:: static inline bool vsh::isConstantVideoFormat(const VSVideoInfo *vi)

   检查剪辑的格式和尺寸是否已知（因此是恒定的）。


isSameVideoFormat
-----------------

.. cpp:function:: static inline bool vsh::isSameVideoFormat(const VSVideoInfo *v1, const VSVideoInfo *v2)

   检查两个剪辑是否具有相同的视频格式。如果两者的格式都未知，则视为相同。
   
   
isSameVideoPresetFormat
-----------------------

.. cpp:function:: static inline bool vsh::isSameVideoPresetFormat(unsigned presetFormat, const VSVideoFormat *v, VSCore *core, const VSAPI *vsapi)

   检查剪辑是否与预设具有相同的视频格式。
   
   
isSameVideoInfo
---------------

.. cpp:function:: static inline bool vsh::isSameVideoInfo(const VSVideoInfo *v1, const VSVideoInfo *v2)

   检查两个剪辑是否具有相同的视频格式和尺寸。如果两者的格式都未知，则视为相同。尺寸也是如此。比较时不考虑帧率。



isSameAudioFormat
-----------------

.. cpp:function:: static inline bool vsh::isSameAudioFormat(const VSAudioInfo *v1, const VSAudioInfo *v2)

   检查两个剪辑是否具有相同的音频格式。


isSameAudioInfo
---------------

.. cpp:function:: static inline bool vsh::isSameAudioInfo(const VSAudioInfo *v1, const VSAudioInfo *v2)

   检查两个剪辑是否具有相同的音频格式和采样率。


muldivRational
--------------

.. cpp:function:: static inline void vsh::muldivRational(int64_t *num, int64_t *den, int64_t mul, int64_t div)

   将两个有理数相乘并约分结果，即 *num*\ /\ *den* \* *mul*\ /\ *div*。结果存储在 *num* 和 *den* 中。

   调用者必须确保 *div* 不为 0。


reduceRational
--------------

.. cpp:function:: static inline void vsh::reduceRational(int64_t *num, int64_t *den)

   约分有理数。
   

addRational
-----------

.. cpp:function:: static inline void vsh::addRational(int64_t *num, int64_t *den, int64_t addnum, int64_t addden)

   将两个有理数相加并约分结果，即 *num*\ /\ *den* + *addnum*\ /\ *addden*。结果存储在 *num* 和 *den* 中。


int64ToIntS
-----------

.. cpp:function:: static inline int vsh::int64ToIntS(int64_t i)

   使用有符号饱和将 int64_t 转换为 int。在从 VSMap 读取整数属性时有助于消除警告，并避免 int 溢出时的意外行为。


doubleToFloatS
--------------

.. cpp:function:: static inline int vsh::doubleToFloatS(double d)

   将 double 转换为 float。在从 VSMap 读取 double 属性时有助于消除警告，主要是为了与 `int64ToIntS`_ 对称。


bitblt
------

.. cpp:function:: static inline void vsh::bitblt(void *dstp, int dst_stride, const void *srcp, int src_stride, size_t row_size, size_t height)

   从一个平面复制字节到另一个平面。基本上是循环中的 memcpy。

   *row_size* 以字节为单位。


areValidDimensions
------------------

.. cpp:function:: static inline bool vsh::areValidDimensions(const VSFormat *fi, int width, int height)

   检查给定尺寸对于特定格式是否有效，考虑色度子采样。
