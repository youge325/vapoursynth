VapourSynth4.h（核心 API 头文件）
===================================

目录
#################

简介_


宏_
   VS_CC_

   VS_EXTERNAL_API_

   VAPOURSYNTH_API_MAJOR_

   VAPOURSYNTH_API_MINOR_

   VAPOURSYNTH_API_VERSION_
   
   VS_AUDIO_FRAME_SAMPLES_
   
   VS_MAKE_VERSION_
   

枚举_
   VSColorFamily_

   VSSampleType_

   VSPresetVideoFormat_

   VSFilterMode_

   VSMediaType_
   
   VSAudioChannels_

   VSPropertyType_

   VSMapPropertyError_

   VSMapAppendMode_

   VSActivationReason_

   VSMessageType_

   VSCoreCreationFlags_
   
   VSPluginConfigFlags_
   
   VSDataTypeHint_
   
   VSRequestPattern_
   
   VSCacheMode_
   

结构体_
   VSFrame_

   VSNode_

   VSCore_

   VSPlugin_
   
   VSPluginFunction_

   VSFunction_

   VSMap_
   
   VSLogHandle_

   VSFrameContext_

   VSVideoFormat_

   VSVideoInfo_
   
   VSAudioFormat_
   
   VSAudioInfo_

   VSCoreInfo_
   
   VSCoreInfo2_
   
   VSFilterDependency_

   VSPLUGINAPI_

   VSAPI_

      * 处理核心的函数：

          * createCore_

          * freeCore_

          * setMaxCacheSize_
          
          * setThreadCount_
          
          * getCoreInfo_
          
          * getCoreInfo2_
          
          * getAPIVersion_
          
      * 处理日志的函数
          
          * addLogHandler_
          
          * removeLogHandler_

          * logMessage_

      * 处理帧对象的函数：

          * newVideoFrame_

          * newVideoFrame2_
          
          * newAudioFrame_

          * newAudioFrame2_
          
          * freeFrame_
          
          * addFrameRef_
          
          * copyFrame_

          * getFramePropertiesRO_

          * getFramePropertiesRW_

          * getStride_

          * getReadPtr_

          * getWritePtr_

          * getVideoFrameFormat_
          
          * getAudioFrameFormat_
          
          * getFrameType_

          * getFrameWidth_

          * getFrameHeight_

          * getFrameLength_

      * 处理滤镜与节点的函数：
      
          * createVideoFilter_

          * createVideoFilter2_
          
          * createAudioFilter_

          * createAudioFilter2_
          
          * setLinearFilter_
          
          * setCacheMode_
          
          * setCacheOptions_

          * freeNode_
          
          * addNodeRef_
          
          * getNodeType_

          * getVideoInfo_

          * getAudioInfo_    

      * 处理格式对象的函数：
      
          * getVideoFormatName_
          
          * getAudioFormatName_
          
          * queryVideoFormat_
          
          * queryAudioFormat_

          * queryVideoFormatID_

          * getVideoFormatByID_

      * 处理映射表（VSMap）的函数：

          * createMap_

          * freeMap_

          * clearMap_

          * mapGetError_
          
          * mapSetError_

          * mapNumKeys_

          * mapGetKey_

          * mapDeleteKey_

          * mapNumElements_
          
          * mapGetType_
          
          * mapSetEmpty_

          * mapGetInt_
          
          * mapGetIntSaturated_

          * mapGetIntArray_
          
          * mapSetInt_

          * mapSetIntArray_

          * mapGetFloat_
          
          * mapGetFloatSaturated_

          * mapGetFloatArray_
          
          * mapSetFloat_

          * mapSetFloatArray_

          * mapGetData_

          * mapGetDataSize_
          
          * mapGetDataTypeHint_

          * mapSetData_

          * mapGetNode_
          
          * mapSetNode_
          
          * mapConsumeNode_

          * mapGetFrame_
          
          * mapSetFrame_
          
          * mapConsumeFrame_

          * mapGetFunction_

          * mapSetFunction_
          
          * mapConsumeFunction_

      * 处理插件与插件函数的函数：
      
          * registerFunction_

          * getPluginByID_

          * getPluginByNamespace_

          * getNextPlugin_
          
          * getPluginName_
          
          * getPluginID_
          
          * getPluginNamespace_
          
          * getNextPluginFunction_
          
          * getPluginFunctionByName_
          
          * getPluginFunctionName_
          
          * getPluginFunctionArguments_
          
          * getPluginFunctionReturnType_

          * getPluginPath_
          
          * getPluginVersion_
          
          * invoke_

      * 处理外部函数封装的函数：

          * createFunction_
          
          * freeFunction_

          * addFunctionRef_

          * callFunction_

      * 用于取帧及滤镜内部调用的函数：

          * getFrame_

          * getFrameAsync_

          * getFrameFilter_

          * requestFrameFilter_        

          * releaseFrameEarly_
          
          * cacheFrame_
          
          * setFilterError_
          

函数_
   getVapourSynthAPI_


`编写插件`_
   VSInitPlugin_

   VSFilterGetFrame_

   VSFilterFree_


简介
############

这是 VapourSynth 的主头文件。使用该库的插件和应用程序必须包含此文件。

VapourSynth 的公共 API 全部使用 C 语言。


宏
######

VapourSynth4.h 定义了一些使程序员工作更轻松的预处理器宏。相关的宏在下面描述。

VS_CC
-----

``VS_CC`` 宏扩展为 VapourSynth 使用的调用约定。所有由 VapourSynth 调用的函数都必须使用此宏（滤镜的 "init"、"getframe"、"free" 函数等）。

Example:

.. code-block:: c

   static void VS_CC fooInit(...) { ... }


VS_EXTERNAL_API
---------------

``VS_EXTERNAL_API`` 宏扩展为共享库导出函数所需的平台特定代码。它还负责在需要时添加 ``extern "C"`` 和 ``VS_CC``。

This macro must be used for a plugin's entry point, like so:

.. code-block:: c

   VS_EXTERNAL_API(void) VapourSynthPluginInit2(...) { ... }


VAPOURSYNTH_API_MAJOR
---------------------

主 API 版本。


VAPOURSYNTH_API_MINOR
---------------------

次 API 版本。当向 VSAPI_ 添加新函数或核心行为发生明显变化时会递增。


VAPOURSYNTH_API_VERSION
-----------------------

API 版本。高 16 位是 VAPOURSYNTH_API_MAJOR_，低 16 位是 VAPOURSYNTH_API_MINOR_。


VS_AUDIO_FRAME_SAMPLES
----------------------

音频帧中的音频采样数。这是一个静态数字，以便可以计算获取特定采样所需的音频帧。


VS_MAKE_VERSION
---------------

用于创建版本号。第一个参数是主版本号，第二个是次版本号。


枚举
#####

.. _VSColorFamily:

enum VSColorFamily
------------------

   * cfUndefined

   * cfGray

   * cfRGB

   * cfYUV


.. _VSSampleType:

enum VSSampleType
-----------------

   * stInteger

   * stFloat


.. _VSPresetVideoFormat:

enum VSPresetVideoFormat
------------------------

   后缀为 H 和 S 的预设具有浮点采样类型。H 和 S 后缀分别代表半精度和单精度。所有格式均为平面格式。请参阅头文件以了解所有当前定义的视频格式预设。
   
   * pf\*


.. _VSFilterMode:

enum VSFilterMode
-----------------

   控制滤镜的多线程方式（如果有的话）。

   * fmParallel

     完全并行执行。多个线程将调用滤镜的 "getframe" 函数，以并行获取多个帧。

   * fmParallelRequests

     适用于本质上是串行的但可以提前请求一个或多个所需帧的滤镜。滤镜的 "getframe" 函数将同时从多个线程以激活原因 arInitial 被调用，但一次只有一个线程会以激活原因 arAllFramesReady 调用它。

   * fmUnordered

     一次只有一个线程可以调用滤镜的 "getframe" 函数。适用于修改或检查其内部状态以确定请求哪些帧的滤镜。

     虽然 "getframe" 函数一次只在一个线程中运行，但调用可以以任意顺序发生。例如，可以先以原因 arInitial 调用帧 0，然后再以原因 arInitial 调用帧 1，然后以原因 arAllFramesReady 调用帧 0。

   * fmFrameState

     为了与其他滤镜架构兼容。请勿在新滤镜中使用。滤镜的 "getframe" 函数一次只从一个线程被调用。与 fmUnordered 不同，一次只处理一个帧。 


.. _VSMediaType:

enum VSMediaType
----------------

   用于指示 `VSFrame` 或 `VSNode` 对象的类型。

   * mtVideo

   * mtAudio


.. _VSAudioChannels:

enum VSAudioChannels
--------------------

   音频声道位置枚举。在旧版 API 中镜像 FFmpeg 音频声道常量。请参阅头文件以了解所有可用值。
   
   * ac\*
   

.. _VSPropertyType:

enum VSPropertyType
-------------------

   可以存储在 VSMap 中的属性类型。

   * ptUnset

   * ptInt

   * ptFloat

   * ptData
   
   * ptFunction

   * ptVideoNode
   
   * ptAudioNode

   * ptVideoFrame
   
   * ptAudioFrame


.. _VSMapPropertyError:

enum VSMapPropertyError
-----------------------

   当 mapGet* 函数失败时，它会在 *err* 参数中返回以下值之一。

   所有错误都是非零值。
   
   * peSuccess

   * peUnset

     在映射表中未找到请求的键。

   * peType

     使用了错误的函数来获取属性。例如，对 ptFloat 类型的属性使用了 mapGetInt_\ ()。

   * peIndex

     请求的索引超出范围。
     
   * peError
   
     映射表已设置错误状态。


.. _VSMapAppendMode:

enum VSMapAppendMode
---------------------

   控制 mapSetInt_\ () 及相关函数的行为。

   * maReplace

     与该键关联的所有现有值将被新值替换。

   * maAppend

     新值将追加到与该键关联的现有值列表中。


.. _VSActivationReason:

enum VSActivationReason
-----------------------

   参见 VSFilterGetFrame_。

   * arInitial

   * arAllFramesReady

   * arError


.. _VSMessageType:

enum VSMessageType
------------------

   参见 addLogHandler_\ ()。

   * mtDebug
   
   * mtInformation

   * mtWarning

   * mtCritical

   * mtFatal


.. _VSCoreCreationFlags:

enum VSCoreCreationFlags
------------------------

   创建核心时的选项。

   * ccfEnableGraphInspection
   
      使用图检查 API 函数所必需的。由于存储了额外信息，会增加内存使用量。
   
   * ccfDisableAutoLoading
   
      不自动加载任何用户插件。核心插件始终会被加载。
      
   * ccfDisableLibraryUnloading
   
      在核心销毁时不卸载插件库。由于每次加载和卸载库时都会有少量内存泄漏（Windows 特性，不是我的错），这在频繁重新加载脚本的应用程序中可能有帮助。

   * ccfEnableFrameRefDebug
   
      记录帧的分配和释放信息以及由哪个滤镜执行（如果有的话）。消息级别为信息级。有助于调试帧引用泄漏。
   
.. _VSPluginConfigFlags:

enum VSPluginConfigFlags
------------------------

   加载插件时的选项。

   * pcModifiable
   
      允许在插件加载阶段之后向插件对象添加函数。主要用于 Avisynth 兼容性和其他外部插件加载器。
   
   
.. _VSDataTypeHint:

enum VSDataTypeHint
-------------------

   由于数据类型可以包含纯二进制数据和可打印字符串，因此该类型还包含一个提示，指示数据是否可读。通常未知类型应该非常少见，几乎只是作为 API3 兼容性的产物而创建的。

   * dtUnknown
   
   * dtBinary
   
   * dtUtf8


.. _VSRequestPattern:

enum VSRequestPattern
---------------------

   描述滤镜的上游帧请求模式。

   * rpGeneral
   
      任何模式都可以。注意，可能请求超出 VSNode 帧长度（重复最后一帧）的滤镜应使用 *rpGeneral* 而不是其他任何模式。
   
   * rpNoFrameReuse
   
     如果所有输出帧恰好被请求一次，则最多只请求一个输入帧一次。这包括 Trim、Reverse、SelectEvery 等滤镜。
   
   * rpStrictSpatial
   
     仅请求帧 N 来输出帧 N。与 *rpNoFrameReuse* 的主要区别在于请求的帧始终是固定的且提前已知的。滤镜示例：Lut、Expr（有条件地，参见 *rpGeneral* 注释）等。

   * rpFrameReuseLastOnly
   
     类似于 *rpNoFrameReuse*，但最后一帧会被缓存以防多次请求。

   
.. _VSCacheMode:

enum VSCacheMode
----------------

   描述节点输出的缓存方式。

   * cmAuto
   
      根据报告的请求模式和消费者数量启用或禁用缓存。
   
   * cmForceDisable
   
      永不缓存任何内容。
   
   * cmForceEnable

      * 始终使用缓存。


结构体
#######

大多数结构体是不透明的，其内容只能通过 API 中的函数访问。


.. _VSFrame:

struct VSFrame
-----------------

   一个可以保存音频或视频数据的帧。

   帧中每行像素保证至少有 32 字节对齐。具有相同宽度和每样本字节数的两个帧保证具有相同的步幅。
   
   音频数据也保证至少 32 字节对齐。

   可以使用 VSMap_ 将任何数据附加到帧上。


.. _VSNode:

struct VSNode
----------------

   对构建的滤镜图中节点的引用。它的主要用途是作为其他滤镜的参数或从中请求帧。


.. _VSCore:

struct VSCore
-------------

   核心代表 VapourSynth 的一个实例。每个核心独立加载插件并跟踪内存。


.. _VSPlugin:

struct VSPlugin
---------------

   VapourSynth 插件对象。核心内置了几个插件，因此始终可用：基础滤镜（标识符
   ``com.vapoursynth.std``，命名空间 ``std``）、缩放器（标识符
   ``com.vapoursynth.resize``，命名空间 ``resize``），以及在 Windows 上运行时可用的 Avisynth
   兼容模块（标识符 ``com.vapoursynth.avisynth``，命名空间 ``avs``）。

   函数参考描述了如何加载 VapourSynth 和 Avisynth 插件。

   当加载插件（.so / .dylib / .dll）时，核心会构造一个 VSPlugin 实例，并将指针传递给插件的 VapourSynthPluginInit2() 函数。

   一个 VapourSynth 插件可以导出任意数量的滤镜。

   插件具有以下属性：

      - 一个标识符，必须在所有现有的 VapourSynth 插件中唯一，因为核心使用它来确保插件只被加载一次。

      - 一个命名空间，同样唯一。插件导出的滤镜最终位于插件的命名空间中。

      - 一个完整名称，核心在一些错误消息中使用它。
      
      - 插件的版本。

      - 插件所需的 VapourSynth API 版本。

      - 一个文件名。

   你可以对 VSPlugin 执行的操作包括：

      - 使用 getNextPluginFunction_\ () 枚举它导出的所有滤镜。

      - 使用 invoke_\ () 调用其中一个滤镜。

      - 使用 getPluginPath_\ () 获取其在文件系统中的位置。

   所有已加载的插件（包括内置插件）都可以使用 getNextPlugin_\ () 枚举。

   一旦加载，插件只有在 VapourSynth 核心被释放时才会被卸载。
   
   
.. _VSPluginFunction:

struct VSPluginFunction
-----------------------

   属于 VapourSynth 插件的函数。此对象的主要用途是让编辑器可以查询插件的名称、参数列表和返回类型。
   
   一个特殊之处是，插件函数不能使用 `VSPluginFunction` 指针调用，而是使用 invoke_\ ()，它以 `VSPlugin` 和函数名字符串作为参数。


.. _VSFunction:

struct VSFunction
-----------------

   保存对可调用函数的引用。此类型的主要用途是使函数可以在脚本层和核心中的插件之间共享。


.. _VSMap:

struct VSMap
------------

   VSMap 是一个存储（键，值）对的容器。键是字符串，值可以是整数（数组）、浮点数、字节数组、VSNode_、VSFrame_ 或 VSFunction_。

   VSMap 中的键值对按键排序。

   In VapourSynth, VSMaps have several uses:
      - 存储滤镜的参数和返回值

      - 存储用户定义函数的参数和返回值

      - 存储附加到帧的属性

   键中只能使用字母数字字符和下划线。

   可以分别使用 createMap_\ () 和 freeMap_\ () 来创建和销毁映射表。

   可以使用多个以 "map" 为前缀的函数来获取和修改映射表的内容。

   可以使用 clearMap_\ () 清除映射表的内容。


.. _VSLogHandle:

struct VSLogHandle
------------------

   表示已注册的日志记录器的不透明类型。


.. _VSFrameContext:

struct VSFrameContext
---------------------

   表示滤镜中当前帧请求的不透明类型。


.. _VSVideoFormat:

struct VSVideoFormat
--------------------

   描述剪辑的格式。 
   
   使用 queryVideoFormat_\ () 并进行适当的错误检查来填充它。允许手动填写结构体，但不推荐，因为非法的值组合将导致未定义行为。
   
   .. c:member:: int colorFamily

      参见 VSColorFamily_。

   .. c:member:: int VSVideoFormat.sampleType

      参见 VSSampleType_。

   .. c:member:: int VSVideoFormat.bitsPerSample

      有效位数。

   .. c:member:: int VSVideoFormat.bytesPerSample

      每个采样所需的字节数。始终是 2 的幂，且是能容纳每个采样使用的位数的最小值。

   .. c:member:: int subSamplingW
   .. c:member:: int subSamplingH

      log2 subsampling factor, applied to second and third plane.
      Convenient numbers that can be used like so:

      .. code-block:: c

         uv_width = y_width >> subSamplingW;

   .. c:member:: int numPlanes

      平面数。


.. _VSVideoInfo:

struct VSVideoInfo
------------------

   包含关于剪辑的信息。

   .. c:member:: VSVideoFormat format

      剪辑的格式。如果格式可变，*colorFamily* 将设置为 *cfUndefined*。

   .. c:member:: int64_t fpsNum

      剪辑帧率的分子部分。如果帧率可变则为 0。应始终是最简分数。

   .. c:member:: int64_t fpsDen

      剪辑帧率的分母部分。如果帧率可变则为 0。应始终是最简分数。

   .. c:member:: int width

      剪辑的宽度。如果剪辑的尺寸可变，宽度和高度都将为 0。

   .. c:member:: int height

      剪辑的高度。如果剪辑的尺寸可变，宽度和高度都将为 0。

   .. c:member:: int numFrames

      剪辑的长度。   
      
      
.. _VSAudioFormat:

struct VSAudioFormat
--------------------

   描述剪辑的格式。 
   
   使用 queryAudioFormat_\ () 并进行适当的错误检查来填充它。允许手动填写结构体，但不推荐，因为非法的值组合将导致未定义行为。

   .. c:member:: int sampleType

      参见 VSSampleType_。

   .. c:member:: int bitsPerSample

      有效位数。

   .. c:member:: int bytesPerSample

      Number of bytes needed for a sample. This is always a power of 2 and the
      smallest possible that can fit the number of bits used per sample.

   .. c:member:: int numChannels

      音频声道数。

   .. c:member:: uint64_t channelLayout

      使用 VSAudioChannels_ 中的常量左移 1 来表示存在的声道的位掩码。 


.. _VSAudioInfo:

struct VSAudioInfo
------------------

   包含关于剪辑的信息。

   .. c:member:: VSAudioFormat VSAudioInfo.format

      剪辑的格式。与视频不同，音频格式永远不会改变。

   .. c:member:: int sampleRate

      采样率。   
      
   .. c:member:: int64_t numSamples

      剪辑的音频采样长度。   

   .. c:member:: int VSAudioInfo.numFrames

      剪辑的音频帧长度。   
      

.. _VSCoreInfo:

struct VSCoreInfo
-----------------

   包含关于 VSCore_ 实例的信息。

   .. c:member:: const char* VSCoreInfo.versionString

      可打印的字符串，包含库名称、版权声明、核心和 API 版本。

   .. c:member:: int core

      核心版本。

   .. c:member:: int api

      API 版本。

   .. c:member:: int VSCoreInfo.numThreads

      工作线程数。

   .. c:member:: int64_t VSCoreInfo.maxFramebufferSize

      帧缓冲区缓存将被允许增长到此大小（字节）后才会积极回收内存。

   .. c:member:: int64_t VSCoreInfo.usedFramebufferSize

      帧缓冲区缓存的当前大小，以字节为单位。


.. _VSCoreInfo2:

struct VSCoreInfo2
------------------

   包含关于 VSCore_ 实例的信息。

   .. c:member:: const char* versionString

      Printable string containing the name of the library, copyright notice,
      core and API versions.

   .. c:member:: int coreVersion

      核心版本。

   .. c:member:: int apiVersion

      API 版本。
      
   .. c:member:: int creationFlags

      创建核心时传递的标志。

   .. c:member:: int numThreads

      工作线程数。

   .. c:member:: int64_t maxFramebufferSize

      帧缓冲区缓存将被允许增长到此大小（字节）后才会积极回收内存。

   .. c:member:: int64_t usedFramebufferSize

      帧缓冲区缓存的当前大小，以字节为单位。

.. _VSFilterDependency:

struct VSFilterDependency
-------------------------

   包含关于 VSCore_ 实例的信息。

   .. c:member:: VSNode *source

      请求帧的节点。

   .. c:member:: int requestPattern

      VSRequestPattern_ 中的一个值。
      

.. _VSPLUGINAPI:

struct VSPLUGINAPI
------------------
  
   此结构体用于在插件初始加载时访问 VapourSynth 的 API。

----------

   int getAPIVersion()
   
      参见结构体 VSAPI_ 中的 getAPIVersion_\ ()。

----------

   .. _configPlugin:

   int configPlugin(const char \*identifier, const char \*pluginNamespace, const char \*name, int pluginVersion, int apiVersion, int flags, VSPlugin \*plugin)
   
      用于在加载时提供有关插件的信息。必须从 *VapourSynthPluginInit2* 入口点恰好调用一次。建议在提供 *pluginVersion* 时使用 VS_MAKE_VERSION_ 宏。如果您不知道实际需要的特定 *apiVersion*，只需传递 VAPOURSYNTH_API_VERSION_ 以匹配您正在编译的头文件版本。*flags* 由 VSPluginConfigFlags_ 中的值通过 OR 组合而成，但对于大多数插件通常应为 0。
      
      成功时返回非零值。

----------

   int registerFunction(const char \*name, const char \*args, const char \*returnType, VSPublicFunction argsFunc, void \*functionData, VSPlugin \*plugin)
   
      参见结构体 VSAPI_ 中的 registerFunction_\ ()。


.. _VSAPI:

struct VSAPI
------------

   这个巨大的结构体是访问 VapourSynth 公共 API 的方式。

----------

   .. _createCore:

   VSCore_ \*createCore(int flags)

      创建 VapourSynth 处理核心并返回其指针。可以创建多个核心，但在大多数情况下不需要这样做。

      *flags*
         如需要可将 `VSCoreCreationFlags` 通过 OR 组合。传递 0 以使用适合大多数用途的合理默认值。

----------

   .. _freeCore:

   void freeCore(VSCore_ \*core)

      释放核心。只应在所有帧请求完成且属于该核心的所有对象都已释放后执行。

----------

   .. _setMaxCacheSize:

   int64_t setMaxCacheSize(int64_t bytes, VSCore_ \*core)

      设置帧缓冲区缓存的最大大小。返回新的最大大小。

----------

   .. _setThreadCount:

   int setThreadCount(int threads, VSCore_ \*core)

      设置用于处理的线程数。传递 0 以自动检测。返回将用于处理的线程数。

----------

   .. _getCoreInfo:

   void getCoreInfo(VSCore_ \*core, VSCoreInfo_ \*info)

      返回有关 VapourSynth 核心的信息。
      
----------

   .. _getCoreInfo2:

   void getCoreInfo(VSCore_ \*core, VSCoreInfo2_ \*info)

      返回有关 VapourSynth 核心的信息。

----------

   .. _getAPIVersion:

   int getAPIVersion()

      返回库支持的最高 VAPOURSYNTH_API_VERSION_。

----------

   .. _logMessage:

   void logMessage(int msgType, const char \*msg, VSCore \*core)

      通过 VapourSynth 的日志框架发送消息。参见 addLogHandler_。

      *msgType*
         消息类型。VSMessageType_ 中的一个。

         如果 *msgType* 是 mtFatal，VapourSynth 将在传递消息后调用 abort()。

      *msg*
         消息内容。
      
----------

   .. _addLogHandler:

   VSLogHandle \*addLogHandler(VSLogHandler handler, VSLogHandlerFree free, void \*userData, VSCore_ \*core)

      为 VapourSynth 发出的各种错误消息安装自定义处理程序。消息处理程序按 VSCore_ 实例设置。返回唯一句柄。

      如果未安装日志处理程序，最多缓存几百条消息，并在附加日志处理程序后立即传递。此行为的存在主要是为了使自动加载插件（默认行为）时的警告不会消失。

      *handler*
         typedef void (VS_CC \*VSLogHandler)(int msgType, const char \*msg, void \*userdata)

         自定义消息处理程序。如果为 NULL，将恢复默认消息处理程序。

         *msgType*
            消息类型。VSMessageType_ 中的一个。

            如果 *msgType* 是 mtFatal，VapourSynth 将在消息处理程序返回后调用 abort()。

         *msg*
            消息内容。
            
      *free*
         typedef void (VS_CC \*VSLogHandlerFree)(void \*userData)
         
         在处理程序被移除时调用。

      *userData*
         传递给消息处理程序的指针。
                  
----------

   .. _removeLogHandler:

   int removeLogHandler(VSLogHandle \*handle, VSCore \*core)

      移除自定义处理程序。成功时返回非零值，句柄无效时返回零。

      *handle*
         从 addLogHandler_\ () 获取的句柄。

----------

   .. _newVideoFrame:

   VSFrame_ \*newVideoFrame(const VSVideoFormat_ \*format, int width, int height, const VSFrame_ \*propSrc, VSCore_ \*core)

      创建一个新的视频帧，可选择复制附加到另一个帧的属性。向此函数传递无效参数是致命错误。

      新帧包含未初始化的内存。

      *format*
         所需的色彩空间格式。不能为 NULL。

      *width*

      *height*
         帧的所需尺寸，以像素为单位。必须大于 0，且是格式中子采样的合适倍数。

      *propSrc*
         将从中复制属性的帧。可以为 NULL。

      返回指向创建的帧的指针。新帧的所有权转移给调用者。

      另见 newVideoFrame2_\ ()。

----------

   .. _newVideoFrame2:

   VSFrame_ \*newVideoFrame2(const VSVideoFormat_ \*format, int width, int height, const VSFrame_ \**planeSrc, const int \*planes, const VSFrame_ \*propSrc, VSCore_ \*core)

      从现有帧的平面创建新的视频帧，可选择复制附加到另一个帧的属性。向此函数传递无效参数是致命错误。

      *format*
         所需的色彩空间格式。不能为 NULL。

      *width*

      *height*
         帧的所需尺寸，以像素为单位。必须大于 0，且是格式中子采样的合适倍数。

      *planeSrc*
         将从中复制平面的帧数组。如果数组的任何元素为 NULL，新帧中对应的平面将包含未初始化的内存。

      *planes*
         平面编号数组，指示从对应的源帧复制哪个平面。

      *propSrc*
         将从中复制属性的帧。可以为 NULL。

      Returns a pointer to the created frame. Ownership of the new frame is
      transferred to the caller.

      Example (assume *frameA*, *frameB*, *frameC* are existing frames):
      
      .. code-block:: c

         const VSFrame * frames[3] = { frameA, frameB, frameC };
         const int planes[3] = { 1, 0, 2 };
         VSFrame * newFrame = vsapi->newVideoFrame2(f, w, h, frames, planes, frameB, core);
         
      新帧的第一个平面现在是 *frameA* 第二个平面的副本，第二个平面是 *frameB* 第一个平面的副本，第三个平面是 *frameC* 第三个平面的副本，属性从 *frameB* 复制。

----------

   .. _newAudioFrame:

   VSFrame_ \*newAudioFrame(const VSAudioFormat \*format, int numSamples, const VSFrame \*propSrc, VSCore \*core)

      创建一个新的音频帧，可选择复制附加到另一个帧的属性。向此函数传递无效参数是致命错误。

      新帧包含未初始化的内存。

      *format*
         所需的音频格式。不能为 NULL。

      *numSamples*
         帧中的采样数。除了滤镜返回的最后一帧外，所有音频帧必须有 VS_AUDIO_FRAME_SAMPLES_ 个采样。

      *propSrc*
         将从中复制属性的帧。可以为 NULL。

      Returns a pointer to the created frame. Ownership of the new frame is
      transferred to the caller.

      另见 newAudioFrame2_\ ()。
      
----------

   .. _newAudioFrame2:

   VSFrame_ \*newAudioFrame2(const VSAudioFormat_ \*format, int numSamples, const VSFrame_ \*\*channelSrc, const int \*channels, const VSFrame_ \*propSrc, VSCore \*core)

      Creates a new audio frame, optionally copying the properties attached to another
      frame. It is a fatal error to pass invalid arguments to this function.

      新帧包含未初始化的内存。

      *format*
         所需的音频格式。不能为 NULL。

      *numSamples*
         帧中的采样数。除了滤镜返回的最后一帧外，所有音频帧必须有 VS_AUDIO_FRAME_SAMPLES_ 个采样。

      *channelSrc*
         将从中复制声道的帧数组。如果数组的任何元素为 NULL，新帧中对应的平面将包含未初始化的内存。

      *channels*
         声道编号数组，指示从对应的源帧复制哪个声道。注意，编号指的是第 n 个声道，而不是声道名称常量。

      *propSrc*
         将从中复制属性的帧。可以为 NULL。

      Returns a pointer to the created frame. Ownership of the new frame is
      transferred to the caller.

      另见 newVideoFrame2_\ ()。

----------

   .. _freeFrame:

   void freeFrame(const VSFrame_ \*f)

      递减帧的引用计数，当引用计数达到 0 时删除帧。

      传递 NULL 是安全的。
      
----------

   .. _addFrameRef:

   const VSFrame_ \*addFrameRef(const VSFrame_ \*f)

      递增帧的引用计数。为方便起见返回 *f*。

----------

   .. _copyFrame:

   VSFrame_ \*copyFrame(const VSFrame_ \*f, VSCore_ \*core)

      复制帧（而不仅仅是引用）。由于帧缓冲区以写时复制方式共享，帧内容在写操作发生之前不会真正复制。这对用户是透明的。

      返回指向新帧的指针。所有权转移给调用者。

----------

   .. _getFramePropertiesRO:

   const VSMap_ \*getFramePropertiesRO(const VSFrame_ \*f)

      返回帧属性的只读指针。只要帧存在，指针就有效。

----------

   .. _getFramePropertiesRW:

   VSMap_ \*getFramePropertiesRW(VSFrame_ \*f)

      返回帧属性的读写指针。只要帧存在，指针就有效。

----------

   .. _getStride:

   ptrdiff_t getStride(const VSFrame_ \*f, int plane)

      返回视频帧平面中两条连续行之间的字节距离。步幅始终为正。如果请求的 *plane* 不存在或不是视频帧则返回 0。

----------

   .. _getReadPtr:

   const uint8_t \*getReadPtr(const VSFrame_ \*f, int plane)

      返回帧的 *plane* 或声道的只读指针。如果传递了无效的 *plane* 或声道号则返回 NULL。

      .. note::
         不要假设帧的所有三个平面分配在一个连续的内存块中（它们不是）。

----------

   .. _getWritePtr:

   uint8_t \*getWritePtr(VSFrame_ \*f, int plane)

      返回帧的 *plane* 或声道的读写指针。如果传递了无效的 *plane* 或声道号则返回 NULL。

      .. note::
         Don't assume all three planes of a frame are allocated in one
         contiguous chunk (they're not).

----------

   .. _getVideoFrameFormat:

   const VSVideoFormat_ \*getVideoFrameFormat(const VSFrame_ \*f)

      获取视频帧的格式。
      
----------

   .. _getAudioFrameFormat:

   const VSAudioFormat_ \*getAudioFrameFormat(const VSFrame_ \*f)

      获取音频帧的格式。
      
----------

   .. _getFrameType:

   int getFrameType(const VSFrame_ \*f)

      返回 VSMediaType_ 中的值以区分音频和视频帧。

----------

   .. _getFrameWidth:

   int getFrameWidth(const VSFrame_ \*f, int plane)

      返回给定视频帧的 *plane* 的宽度，以像素为单位。由于可能的色度子采样，宽度取决于平面编号。音频帧返回 0。

----------

   .. _getFrameHeight:

   int getFrameHeight(const VSFrame_ \*f, int plane)

      返回给定视频帧的 *plane* 的高度，以像素为单位。由于可能的色度子采样，高度取决于平面编号。音频帧返回 0。
      
----------

   .. _getFrameLength:

   int getFrameLength(const VSFrame_ \*f)

      返回帧中的音频采样数。视频帧始终返回 1。

----------

   .. _createVideoFilter:

   void createVideoFilter(VSMap_ \*out, const char \*name, const VSVideoInfo_ \*vi, VSFilterGetFrame_ getFrame, VSFilterFree_ free, int filterMode, const VSFilterDependency_ \*dependencies, int numDeps, void \*instanceData, VSCore_ \*core)

      创建一个新的视频滤镜节点。

      *out*
         滤镜节点的输出映射表。

      *name*
         实例名称。请使其与滤镜名称相同以便于识别。

      *vi*
         滤镜的输出格式。

      *getFrame*
         滤镜的 "getframe" 函数。不能为 NULL。

      *free*
         滤镜的 "free" 函数。可以为 NULL。

      *filterMode*
         VSFilterMode_ 中的一个。指示滤镜支持的并行级别。

      *dependencies*
         滤镜请求帧的节点数组及访问模式。用于更高效地配置缓存。
         
      *numDeps*
         *dependencies* 数组的长度。

      *instanceData*
         指向滤镜私有数据的指针。此指针将传递给 *getFrame* 和 *free* 函数。应由 *free* 函数释放。

      此函数返回后，*out* 将包含追加到 "clip" 属性的新节点，或者如果出现问题则包含错误。

----------

   .. _createVideoFilter2:

   VSNode_ \*createVideoFilter2(const char \*name, const VSVideoInfo_ \*vi, VSFilterGetFrame_ getFrame, VSFilterFree_ free, int filterMode, const VSFilterDependency_ \*dependencies, int numDeps, void \*instanceData, VSCore_ \*core)

      与 createVideoFilter_ 相同，只是新节点会被返回而不是追加到 *out* 映射表中。出错时返回 NULL。

----------

   .. _createAudioFilter:

   void createAudioFilter(VSMap \*out, const char \*name, const VSAudioInfo \*ai, VSFilterGetFrame getFrame, VSFilterFree free, int filterMode, const VSFilterDependency_ \*dependencies, int numDeps, void \*instanceData, VSCore \*core)

      创建一个新的视频滤镜节点。

      *out*
         滤镜节点的输出映射表。

      *name*
         实例名称。请使其与滤镜名称相同以便于识别。

      *ai*
         滤镜的输出格式。

      *getFrame*
         滤镜的 "getframe" 函数。不能为 NULL。

      *free*
         滤镜的 "free" 函数。可以为 NULL。

      *filterMode*
         One of VSFilterMode_. Indicates the level of parallelism
         supported by the filter.

      *dependencies*
         An array of nodes the filter requests frames from and the access pattern.
         Used to more efficiently configure caches.
         
      *numDeps*
         *dependencies* 数组的长度。

      *instanceData*
         A pointer to the private filter data. This pointer will be passed to
         the *getFrame* and *free* functions. It should be freed by
         the *free* function.

      After this function returns, *out* will contain the new node appended to the
      "clip" property, or an error, if something went wrong.

----------

   .. _createAudioFilter2:

   VSNode \*createAudioFilter2(const char \*name, const VSAudioInfo \*ai, VSFilterGetFrame getFrame, VSFilterFree free, int filterMode, const VSFilterDependency_ \*dependencies, int numDeps, void \*instanceData, VSCore \*core)

      与 createAudioFilter_ 相同，只是新节点会被返回而不是追加到 *out* 映射表中。出错时返回 NULL。

----------

   .. _setLinearFilter:

   int setLinearFilter(VSNode_ \*node)

      必须在音频或视频滤镜创建后立即调用。返回在尝试使请求更线性时传递给 cacheFrame_ 的额外帧数的合理上限。
      
----------

   .. _setCacheMode:

   void setCacheMode(VSNode_ \*node, int mode)

      确定帧缓存策略。传递 VSCacheMode_ 常量。主要用于缓存调试，因为自动模式在几乎所有情况下都能正常工作。对此函数的调用也可能被静默忽略。
      
      调用时将缓存重置为默认选项，丢弃 setCacheOptions_ 更改。
      
----------

   .. _setCacheOptions:

   void setCacheOptions(VSNode_ \*node, int fixedSize, int maxSize, int maxHistorySize)

      在 setCacheMode_ 之后调用，否则更改将被丢弃。设置节点关联缓存的内部细节。对此函数的调用也可能被静默忽略。
      
      *fixedSize*
         设为非零值使缓存始终保持 *maxSize* 个帧。
         
      *maxSize*
         要缓存的最大帧数。请注意，除非设置了 *fixedSize*，否则此值会使用内部算法自动调整。
         
      *maxHistorySize*
         要跟踪多少个最近从缓存中驱逐的帧。用于确定增大或缩小缓存是否有益。设置 *fixedSize* 时无效。
      
----------

   .. _freeNode:

   void freeNode(VSNode_ \*node)

      递减节点的引用计数，当引用计数达到 0 时销毁节点。

      传递 NULL 是安全的。
      
----------

   .. _addNodeRef:

   VSNode_ \*addNodeRef(VSNode_ \*node)

      递增节点的引用计数。为方便起见返回相同的 *node*。

----------

   .. _getNodeType:

   int getNodeType(VSNode_ \*node)

      返回 VSMediaType_。用于确定节点是音频还是视频类型。

----------

   .. _getVideoInfo:

   const VSVideoInfo_ \*getVideoInfo(VSNode_ \*node)

      返回与节点关联的视频信息指针。只要节点存在，指针就有效。传递非视频节点是未定义行为。
      
----------

   .. _getAudioInfo:

   const VSAudioInfo_ \*getAudioInfo(VSNode_ \*node)

      返回与节点关联的音频信息指针。只要节点存在，指针就有效。传递非音频节点是未定义行为。

----------

   .. _getVideoFormatName:

   int getVideoFormatName(const VSVideoFormat \*format, char \*buffer)

      尝试输出视频格式的较易读名称。
      
      *format*
         输入的视频格式。
      
      *buffer*
         目标缓冲区。最多写入 32 字节（包括结尾的 NULL）。
      
      成功时返回非零值。
      
----------

   .. _getAudioFormatName:

   int getAudioFormatName(const VSAudioFormat \*format, char \*buffer)

      尝试输出音频格式的较易读名称。
      
      *format*
         输入的音频格式。
      
      *buffer*
         Destination buffer. At most 32 bytes including terminating NULL
         will be written.
      
      成功时返回非零值。

----------

   .. _queryVideoFormat:

   int queryVideoFormat(VSVideoFormat_ \*format, int colorFamily, int sampleType, int bitsPerSample, int subSamplingW, int subSamplingH, VSCore_ \*core)

      根据提供的参数填充 VSVideoInfo_ 结构体。在填充 *format* 之前验证参数。

      *format*
         要填充的结构体。

      *colorFamily*
         VSColorFamily_ 中的一个。

      *sampleType*
         VSSampleType_ 中的一个。

      *bitsPerSample*
         单个分量的有效位数。有效范围是 8-32。

         对于浮点格式，只允许 16 或 32 位。

      *subSamplingW*
         水平色度子采样的 log2 值。0 == 无子采样。有效范围是 0-4。

      *subSamplingH*
         垂直色度子采样的 log2 值。0 == 无子采样。有效范围是 0-4。

         .. note::
            在 VapourSynth 中不允许对 RGB 格式进行子采样。

      成功时返回非零值。

----------

   .. _queryAudioFormat:

   int queryAudioFormat(VSAudioFormat_ \*format, int sampleType, int bitsPerSample, uint64_t channelLayout, VSCore_ \*core)

      根据提供的参数填充 VSAudioFormat_ 结构体。在填充 *format* 之前验证参数。

      *format*
         要填充的结构体。

      *sampleType*
         VSSampleType_ 中的一个。

      *bitsPerSample*
         Number of meaningful bits for a single component. The valid range is
         8-32.

         对于浮点格式，只允许 32 位。

      *channelLayout*
         由 VSAudioChannels_ 中位移常量构造的位掩码。例如立体声表示为 (1 << acFrontLeft) | (1 << acFrontRight)。

      成功时返回非零值。
          
----------

   .. _queryVideoFormatID:

   uint32_t queryVideoFormatID(int colorFamily, int sampleType, int bitsPerSample, int subSamplingW, int subSamplingH, VSCore_ \*core)

      获取与视频格式关联的 ID。类似于 queryVideoFormat_\ ()，但返回格式 ID 而不是填充 VSVideoInfo_ 结构体。

      *colorFamily*
         VSColorFamily_ 中的一个。

      *sampleType*
         VSSampleType_ 中的一个。

      *bitsPerSample*
         Number of meaningful bits for a single component. The valid range is
         8-32.

         对于浮点格式，只允许 16 或 32 位。

      *subSamplingW*
         水平色度子采样的 log2 值。0 == 无子采样。有效范围是 0-4。

      *subSamplingH*
         垂直色度子采样的 log2 值。0 == 无子采样。有效范围是 0-4。

         .. note::
            在 VapourSynth 中不允许对 RGB 格式进行子采样。

      如果提供的参数有效则返回有效的格式 ID，出错时返回 0。
      
----------
      
   .. _getVideoFormatByID:

   int getVideoFormatByID(VSVideoFormat_ \*format, uint32_t id, VSCore_ \*core)

      根据提供的参数填充传递给 *format* 的 VSVideoFormat_ 结构体
      
      *format*
         要填充的结构体。

      *id*
         The format identifier: one of VSPresetVideoFormat_ or a value gotten from queryVideoFormatID_.

      失败时返回 0，成功时返回非零值。

----------

   .. _createMap:

   VSMap_ \*createMap(void)

      创建一个新的属性映射表。之后必须使用 freeMap_\ () 释放它。

----------

   .. _freeMap:

   void freeMap(VSMap_ \*map)

      释放映射表及其包含的所有对象。

----------

   .. _clearMap:

   void clearMap(VSMap_ \*map)

      删除映射表中的所有键及其关联值，使其为空。

----------

   .. _mapGetError:

   const char \*mapGetError(const VSMap_ \*map)

      返回映射表中包含的错误消息的指针，如果没有设置错误则返回 NULL。指针在下一次修改映射表操作之前有效。

----------

   .. _mapSetError:

   void mapSetError(VSMap_ \*map, const char \*errorMessage)

      向映射表添加错误消息。首先清除映射表。错误消息会被复制。在此状态下，映射表只能被释放、清除或查询错误消息。

      对于在滤镜的 "getframe" 函数中遇到的错误，请使用 setFilterError_。

----------

   .. _mapNumKeys:

   int mapNumKeys(const VSMap_ \*map)

      返回属性映射表中包含的键数。

----------

   .. _mapGetKey:

   const char \*mapGetKey(const VSMap_ \*map, int index)

      返回属性映射表中的第 n 个键。

      传递无效的 *index* 将导致致命错误。

      只要键存在于映射表中，指针就有效。

----------

   .. _mapDeleteKey:

   int mapDeleteKey(VSMap_ \*map, const char \*key)

      移除具有给定键的属性。与该键关联的所有值都将丢失。

      如果键不在映射表中则返回 0。否则返回 1。

----------

   .. _mapNumElements:

   int mapNumElements(const VSMap_ \*map, const char \*key)

      返回属性映射表中与键关联的元素数。如果映射表中没有该键则返回 -1。

----------

   .. _mapGetType:

   int mapGetType(const VSMap_ \*map, const char \*key)

      返回 VSPropertyType_ 中的值，表示给定键中元素的类型。如果映射表中没有该键，返回值为 ptUnset。请注意，使用 mapSetEmpty_ 创建的空数组也是有类型的。
      
----------

   .. _mapSetEmpty:

   int mapSetEmpty(const VSMap_ \*map, const char \*key, int type)

      在 *key* 中创建类型为 *type* 的空数组。如果 *key* 已存在或名称无效则返回非零值表示失败。

----------

   .. _mapGetInt:

   int64_t mapGetInt(const VSMap_ \*map, const char \*key, int index, int \*error)

      从 *map* 中指定的 *key* 获取整数。

      成功时返回数值，出错时返回 0。

      如果映射表设置了错误（即 mapGetError_\ () 返回非 NULL），VapourSynth 将因致命错误而终止。
      
      *index*
         元素的从零开始的索引。

         使用 mapNumElements_\ () 了解与键关联的元素总数。

      *error*
         VSMapPropertyError_ 中的一个，成功时为 peSuccess。

         可以在此处传递 NULL，但之后获取属性时遇到的任何问题都将导致 VapourSynth 因致命错误而终止。

----------

   .. _mapGetIntSaturated:

   int mapGetIntSaturated(const VSMap_ \*map, const char \*key, int index, int \*error)

      工作方式与 mapGetInt_\ () 相同，只是返回值还会使用饱和转换为整数。

----------

   .. _mapGetIntArray:

   const int64_t \*mapGetIntArray(const VSMap_ \*map, const char \*key, int \*error)

      从映射表中获取整数数组。如果与键关联的数值很多，请使用此函数，因为它比在循环中调用 mapGetInt_\ () 更快。

      成功时返回数组第一个元素的指针，出错时返回 NULL。使用 mapNumElements_\ () 了解与键关联的元素总数。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapSetInt:

   int mapSetInt(VSMap_ \*map, const char \*key, int64_t i, int append)

      在映射表中设置指定键的整数值。

      一个键可以关联多个值，但它们必须都是相同类型。

      *key*
         属性名称。可以使用字母数字字符和下划线。

      *i*
         要存储的值。

      *append*
         VSMapAppendMode_ 中的一个。

      成功时返回 0，如果尝试向现有键追加错误类型的属性则返回 1。

----------

   .. _mapSetIntArray:

   int mapSetIntArray(VSMap_ \*map, const char \*key, const int64_t \*i, int size)

      向映射表添加整数数组。如果要添加大量数值，请使用此函数，因为它比在循环中调用 mapSetInt_\ () 更快。

      如果 *map* 已包含此 *key* 的属性，该属性将被覆盖，所有旧值将丢失。

      *key*
         Name of the property. Alphanumeric characters and underscore
         may be used.

      *i*
         指向要存储的数组第一个元素的指针。

      *size*
         要从数组中读取的整数数。可以为 0，在这种情况下不会从数组中读取整数，属性将创建为空。

      成功时返回 0，如果 *size* 为负数则返回 1。

----------

   .. _mapGetFloat:

   double mapGetFloat(const VSMap_ \*map, const char \*key, int index, int \*error)

      从映射表中获取浮点数。

      成功时返回数值，出错时返回 0。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapGetFloatSaturated:

   float mapGetFloatSaturated(const VSMap_ \*map, const char \*key, int index, int \*error)

      工作方式与 mapGetFloat_\ () 相同，只是返回值还会转换为 float。

----------

   .. _mapGetFloatArray:

   const double \*mapGetFloatArray(const VSMap_ \*map, const char \*key, int \*error)
   
      从映射表中获取浮点数数组。如果与键关联的数值很多，请使用此函数，因为它比在循环中调用 mapGetFloat_\ () 更快。

      Returns a pointer to the first element of the array on success, or NULL
      in case of error. Use mapNumElements_\ () to know the total number of
      elements associated with a key.

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapSetFloat:

   int mapSetFloat(VSMap_ \*map, const char \*key, double d, int append)
   
      在映射表中设置指定键的浮点值。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapSetFloatArray:

   int mapSetFloatArray(VSMap_ \*map, const char \*key, const double \*d, int size)

      向映射表添加浮点数数组。如果要添加大量数值，请使用此函数，因为它比在循环中调用 mapSetFloat_\ () 更快。

      If *map* already contains a property with this *key*, that property will
      be overwritten and all old values will be lost.

      *key*
         Name of the property. Alphanumeric characters and underscore
         may be used.

      *d*
         指向要存储的数组第一个元素的指针。

      *size*
         要从数组中读取的浮点数数量。可以为 0，在这种情况下不会从数组中读取数字，属性将创建为空。

      成功时返回 0，如果 *size* 为负数则返回 1。

----------

   .. _mapGetData:

   const char \*mapGetData(const VSMap_ \*map, const char \*key, int index, int \*error)

      从映射表中获取任意二进制数据。检查 mapGetDataTypeHint_\ () 可以提供数据是否可读的提示。

      成功时返回数据的指针，出错时返回 NULL。

      返回的数组保证以 NULL 结尾。NULL 字节不被视为数组的一部分（mapGetDataSize_ 不计算在内）。

      指针在映射表被销毁之前或对应键从映射表中移除或修改之前有效。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapGetDataSize:

   int mapGetDataSize(const VSMap_ \*map, const char \*key, int index, int \*error)

      返回 ptData 类型属性的字节大小（参见 VSPropertyType_），出错时返回 0。mapSetData_\ () 添加的终止 NULL 字节不计算在内。
      
      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapGetDataTypeHint:

   int mapGetDataTypeHint(const VSMap_ \*map, const char \*key, int index, int \*error)

      Returns the size in bytes of a property of type ptData (see
      VSPropertyType_), or 0 in case of error. The terminating NULL byte
      added by mapSetData_\ () is not counted.
      
      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapSetData:

   int mapSetData(VSMap \*map, const char \*key, const char \*data, int size, int type, int append)

      在映射表中设置指定键的二进制数据。

      Multiple values can be associated with one key, but they must all be the
      same type.

      *key*
         属性名称。可以使用字母数字字符和下划线。

      *data*
         要存储的值。

         此函数会复制数据，因此不再需要时应释放指针。复制的数据总是添加终止 NULL，但不包含在总大小中以使字符串处理更容易。

      *size*
         要复制的字节数。如果为负数，则复制直到第一个 NULL 字节的所有内容。
         
      *type*
         VSDataTypeHint_ 中的一个，用于提示数据是否可读。

      *append*
         VSMapAppendMode_ 中的一个。

      成功时返回 0，如果尝试向错误类型的属性追加则返回 1。

----------

   .. _mapGetNode:

   VSNode_ \*mapGetNode(const VSMap_ \*map, const char \*key, int index, int \*error)

      从映射表中获取节点。

      成功时返回节点的指针，出错时返回 NULL。

      此函数增加节点的引用计数，因此当不再需要节点时必须使用 freeNode_\ ()。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。

----------

   .. _mapSetNode:

   int mapSetNode(VSMap_ \*map, const char \*key, VSNode_ \*node, int append)

      在映射表中设置指定键的节点。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapConsumeNode:

   int mapConsumeNode(VSMap_ \*map, const char \*key, VSNode_ \*node, int append)

      在映射表中设置指定键的节点并减少引用计数。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapGetFrame:

   const VSFrame_ \*mapGetFrame(const VSMap_ \*map, const char \*key, int index, int \*error)

      从映射表中获取帧。

      成功时返回帧的指针，出错时返回 NULL。

      此函数增加帧的引用计数，因此当不再需要帧时必须使用 freeFrame_\ ()。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。
      
----------

   .. _mapSetFrame:

   int mapSetFrame(VSMap_ \*map, const char \*key, const VSFrame_ \*f, int append)

      在映射表中设置指定键的帧。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapConsumeFrame:

   int mapConsumeFrame(VSMap_ \*map, const char \*key, const VSFrame_ \*f, int append)

      在映射表中设置指定键的帧并减少引用计数。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapGetFunction:

   VSFunctionRef \*mapGetFunction(const VSMap_ \*map, const char \*key, int index, int \*error)

      从映射表中获取函数。

      成功时返回函数的指针，出错时返回 NULL。

      此函数增加函数的引用计数，因此当不再需要函数时必须使用 freeFunction_\ ()。

      有关参数和一般行为的完整描述，请参阅 mapGetInt_\ ()。
      
----------

   .. _mapSetFunction:

   int mapSetFunction(VSMap_ \*map, const char \*key, VSFunction \*func, int append)

      在映射表中设置指定键的函数对象。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _mapConsumeFunction:

   int mapConsumeFunction(VSMap_ \*map, const char \*key, VSFunction \*func, int append)

      在映射表中设置指定键的函数对象并减少引用计数。

      有关参数和一般行为的完整描述，请参阅 mapSetInt_\ ()。

----------

   .. _getPluginByID:

   VSPlugin_ \*getPluginByID(const char \*identifier, VSCore_ \*core)

      返回具有给定标识符的插件的指针，如果未找到则返回 NULL。

      *identifier*
         唯一标识插件的反向 URL。

----------

   .. _getPluginByNamespace:

   VSPlugin_ \*getPluginByNamespace(const char \*ns, VSCore_ \*core)

      返回具有给定命名空间的插件的指针，如果未找到则返回 NULL。

      getPluginByID_ 通常是更好的选择。

      *ns*
         命名空间。

----------

   .. _getNextPlugin:

   VSPlugin_ \*getNextPlugin(VSPlugin_ \*plugin, VSCore_ \*core)

      用于枚举所有当前加载的插件。顺序是固定的，但不提供其他保证。

      *plugin*
         当前插件。传递 NULL 以获取第一个插件。

      按顺序返回下一个插件的指针，如果已到达最后一个插件则返回 NULL。
      
----------

   .. _getPluginName:

   const char \*getPluginName(VSPlugin_ \*plugin)

      返回传递给 configPlugin_ 的插件名称。

----------

   .. _getPluginID:

   const char \*getPluginID(VSPlugin_ \*plugin)

      返回传递给 configPlugin_ 的插件标识符。

----------

   .. _getPluginNamespace:

   const char \*getPluginNamespace(VSPlugin_ \*plugin)

      返回插件当前加载的命名空间。

----------

   .. _getNextPluginFunction:

   VSPluginFunction_ \*getNextPluginFunction(VSPluginFunction_ \*func, VSPlugin \*plugin)

      用于枚举插件中的所有函数。顺序是固定的，但不提供其他保证。

      *func*
         当前函数。传递 NULL 以获取第一个函数。

      *plugin*
         要枚举函数的插件。

      按顺序返回下一个函数的指针，如果已到达最后一个函数则返回 NULL。

----------

   .. _getPluginFunctionByName:

   VSPluginFunction_ \*getPluginFunctionByName(const char \*name, VSPlugin_ \*plugin)

      通过名称获取属于插件的函数。

----------

   .. _getPluginFunctionName:

   const char \*getPluginFunctionName(VSPluginFunction_ \*func)

      返回传递给 registerFunction_ 的函数名称。

----------

   .. _getPluginFunctionArguments:

   const char \*getPluginFunctionArguments(VSPluginFunction_ \*func)

      返回传递给 registerFunction_ 的函数参数字符串。       

----------

   .. _getPluginFunctionReturnType:

   const char \*getPluginFunctionReturnType(VSPluginFunction_ \*func)

      返回传递给 registerFunction_ 的函数返回类型字符串。       

----------

   .. _getPluginPath:

   const char \*getPluginPath(const VSPlugin_ \*plugin)

      返回插件的绝对路径，包括插件的文件名。这是插件的真实位置，即路径中没有符号链接。

      路径元素始终使用正斜杠分隔。

      VapourSynth 保留返回指针的所有权。

----------

   .. _getPluginVersion:

   int getPluginVersion(const VSPlugin_ \*plugin)

      返回插件的版本。这与传递给 configPlugin_ 的版本号相同。

----------

   .. _invoke:

   VSMap_ \*invoke(VSPlugin_ \*plugin, const char \*name, const VSMap_ \*args)

      调用滤镜。

      invoke() 检查传递给滤镜的 *args* 是否与包含该滤镜的插件注册的参数列表一致，调用滤镜的 "create" 函数，并检查滤镜是否返回声明的类型。如果一切顺利，在 invoke() 返回后滤镜将准备好生成帧。

      *plugin*
         指向滤镜所在插件的指针。不能为 NULL。

         参见 getPluginByID_\ ()。

      *name*
         要调用的滤镜名称。

      *args*
         滤镜的参数。

      返回包含滤镜返回值的映射表。调用者获得映射表的所有权。使用 mapGetError_\ () 检查滤镜是否已成功调用。

      大多数滤镜会设置一个错误，或者一个或多个键为 "clip" 的剪辑。例外情况是函数，例如 LoadPlugin 显然不会返回任何剪辑。

----------

   .. _createFunction:

   VSFunction_ \*createFunction(VSPublicFunction func, void \*userData, VSFreeFunctionData free, VSCore_ \*core)

      *func*
         typedef void (VS_CC \*VSPublicFunction)(const VSMap_ \*in, VSMap_ \*out, void \*userData, VSCore_ \*core, const VSAPI_ \*vsapi)

         可以在任何上下文中调用的用户定义函数。

      *userData*
         传递给 *func* 的指针。

      *free*
         typedef void (VS_CC \*VSFreeFunctionData)(void \*userData)

         负责释放 *userData* 的回调。可以为 NULL。

----------

   .. _freeFunction:

   void freeFunction(VSFunction_ \*f)

      递减函数的引用计数，当引用计数达到 0 时删除函数。

      传递 NULL 是安全的。
      
----------

   .. _addFunctionRef:

   VSFunction_ \*addFunctionRef(VSFunction_ \*f)

      递增函数的引用计数。为方便起见返回 *f*。

----------

   .. _callFunction:

   void callFunction(VSFunction_ \*func, const VSMap_ \*in, VSMap_ \*out)

      调用函数。如果调用失败，*out* 将设置错误。
      
      *func*
         要调用的函数。

      *in*
         传递给 *func* 的参数。
         
      *out*
         从 *func* 返回的值。

----------

   .. _getFrame:

   const VSFrame_ \*getFrame(int n, VSNode_ \*node, char \*errorMsg, int bufSize)

      同步获取帧。函数返回时帧可用。

      此函数适用于将核心用作库的外部应用程序，或者如果在滤镜初始化期间需要帧请求。
      
      线程安全。

      *n*
         帧编号。负值将导致错误。

      *node*
         请求帧的节点。

      *errorMsg*
         指向 *bufSize* 字节缓冲区的指针，用于存储可能的错误消息。如果不需要错误消息则可以为 NULL。
         
      *bufSize*
         错误消息的最大长度，以字节为单位（包括结尾的 ' '）。如果不需要错误消息则可以为 0。

      返回生成帧的引用，失败时返回 NULL。帧的所有权转移给调用者。

      .. warning::
         切勿在滤镜的 "getframe" 函数内使用。

----------

   .. _getFrameAsync:

   void getFrameAsync(int n, VSNode_ \*node, VSFrameDoneCallback callback, void \*userData)

      请求生成帧。当帧准备好时，将调用用户提供的函数。请注意，完成 *callback* 一次只从单个线程调用。
      
      此函数适用于将 VapourSynth 用作库的应用程序。
      
      线程安全。

      *n*
         帧编号。负值将导致错误。

      *node*
         请求帧的节点。

      *callback*
         typedef void (VS_CC \*VSFrameDoneCallback)(void \*userData, const VSFrame_ \*f, int n, VSNode_ \*node, const char \*errorMsg)

         客户端应用程序的函数，在调用 getFrameAsync() 后当请求的帧准备好时由核心调用。

         如果请求了多个帧，它们可以以任意顺序返回。客户端应用程序必须负责重新排序。

         此函数一次只从一个线程调用。

         可以从此函数中调用 getFrameAsync() 来请求更多帧。

         *userData*
            指向客户端应用程序私有数据的指针，即之前传递给 getFrameAsync() 的数据。

         *f*
            包含对生成帧的引用，失败时为 NULL。帧的所有权转移给调用者。

         *n*
            帧编号。

         *node*
            帧所属的节点。

         *errorMsg*
            通常包含帧生成失败时错误消息的字符串。如果没有错误则为 NULL。

      *userData*
         传递给回调的指针。

      .. warning::
         切勿在滤镜的 "getframe" 函数内使用。

----------

   .. _getFrameFilter:

   const VSFrame_ \*getFrameFilter(int n, VSNode_ \*node, VSFrameContext_ \*frameCtx)

      获取之前使用 requestFrameFilter_\ () 请求的帧。

      仅在滤镜的 "getframe" 函数内使用。

      滤镜通常在其激活原因为 arAllFramesReady 或 arFrameReady 时调用此函数。参见 VSActivationReason_。

      多次获取同一帧是安全的，但每个引用都需要释放。

      *n*
         帧编号。

      *node*
         从中获取帧的节点。

      *frameCtx*
         传递给滤镜 "getframe" 函数的上下文。

      返回请求帧的指针，如果请求的帧因任何原因不可用则返回 NULL。帧的所有权转移给调用者。

----------

   .. _requestFrameFilter:

   void requestFrameFilter(int n, VSNode_ \*node, VSFrameContext_ \*frameCtx)

      从节点请求帧并立即返回。

      仅在滤镜的 "getframe" 函数内使用。

      滤镜通常在其激活原因为 arInitial 时调用此函数。然后可以在滤镜的激活原因为 arAllFramesReady 时使用 getFrameFilter_\ () 获取请求的帧。参见 VSActivationReason_。

      最好按升序请求帧，即 n、n+1、n+2 等。

      *n*
         帧编号。负值将导致错误。

      *node*
         请求帧的节点。

      *frameCtx*
         传递给滤镜 "getframe" 函数的上下文。
         
----------

   .. _releaseFrameEarly:

   void releaseFrameEarly(VSNode_ \*node, int n, VSFrameContext_ \*frameCtx)

      默认情况下，所有请求的帧在滤镜的帧请求完成之前都会被引用。在极端情况下，当滤镜需要将 20 多个帧缩减为单个输出帧时，分批请求并增量处理数据可能是有益的。
      
      很少需要使用。

      仅在滤镜的 "getframe" 函数内使用。
      
      *node*
         请求帧的节点。
         
      *n*
         帧编号。无效的帧编号（未缓存或为负数）将被简单忽略。

      *frameCtx*
         传递给滤镜 "getframe" 函数的上下文。

----------

   .. _registerFunction:

   int registerFunction(const char \*name, const char \*args, const char \*returnType, VSPublicFunction argsFunc, void \*functionData, VSPlugin_ \*plugin)

      注册插件导出的滤镜的函数。一个插件可以导出任意数量的滤镜。除非 configPlugin_ 设置了 pcModifiable 标志，否则此函数只能在插件加载阶段调用。

      *name*
         Filter name. The characters allowed are letters, numbers, and the
         underscore. The first character must be a letter. In other words:
         ``^[a-zA-Z][a-zA-Z0-9_]*$``

         滤镜名称 *应该* 使用 PascalCase 风格。

      *args*
         包含滤镜参数列表的字符串。

         参数由分号分隔。每个参数由冒号分隔的几个字段组成。不要插入额外的空白字符，否则 VapourSynth 将崩溃。

         Fields:
            参数名称。
               允许使用与滤镜名称相同的字符。参数名称 *应该* 全部小写，只使用字母和下划线。

            类型。
               "int": int64_t

               "float": double

               "data": const char*

               "anode": const VSNode_\ * (audio type)

               "vnode": const VSNode_\ * (video type)

               "aframe": const VSFrame_\ * (audio type)
               
               "vframe": const VSFrame_\ * (video type)

               "func": const VSFunctionRef\ *

               可以通过在类型后追加 "[]" 来声明数组。

            "opt"
               如果参数是可选的。

            "empty"
               用于允许为空的数组。
               
            "any"
               只能放在最后且后面没有分号。表示所有不匹配的剩余参数也应传递。

         The following example declares the arguments "blah", "moo", and "asdf"::

            blah:vnode;moo:int[]:opt;asdf:float:opt;
            
         The following example declares the arguments "blah" and accepts all other arguments no matter the type::

            blah:vnode;any

      *returnType*
         Specifies works similarly to *args* but instead specifies which keys and what type will be returned. Typically this will be::
         
            clip:vnode; 
            
         用于视频滤镜。重要的是不要简单地为所有滤镜指定 "any"，因为此信息在许多编辑器中用于更好的自动补全。

      *argsFunc*
         typedef void (VS_CC \*VSPublicFunction)(const VSMap_ \*in, VSMap_ \*out, void \*userData, VSCore_ \*core, const VSAPI_ \*vsapi)

         核心调用的用户定义函数，用于创建滤镜实例。此函数通常命名为 ``fooCreate``。

         在此函数中，应获取并验证滤镜的输入参数，初始化滤镜的私有实例数据，并调用 createAudioFilter_\ () 或 createVideoFilter_\ ()。滤镜应在此处执行所需的任何其他初始化。

         如果由于某种原因无法创建滤镜，必须使用 freeNode_\ () 释放任何已创建的节点引用，对 *out* 调用 mapSetError_\ ()，然后返回。

         *in*
            输入参数列表。

            使用 mapGetInt_\ () 及相关函数来获取参数值。

            映射表保证仅在滤镜的 "init" 函数返回之前存在。换句话说，mapGetData_\ () 返回的指针在滤镜的 "getframe" 和 "free" 函数中不可用。

         *out*
            输出参数列表。createAudioFilter_\ () 或 createVideoFilter_\ () 将以键名 "clip" 添加输出节点，如果出现问题则添加错误。

         *userData*
            传递给 registerFunction_\ () 的指针。

      *functionData*
         指向用户数据的指针，在创建滤镜时传递给 *argsFunc*。用于使用单个 *argsFunc* 函数注册多个滤镜。

      *plugin*
         指向核心中插件对象的指针，即传递给 VapourSynthPluginInit2() 的指针。

----------

   .. _cacheFrame:

   void cacheFrame(const VSFrame_ \*frame, int n, VSFrameContext_ \*frameCtx)

      将未请求的帧推入缓存。这对于从完全线性访问和按线性顺序生成所有输出中获益很大的（源）滤镜很有用。
 
      此函数只能在使用 setLinearFilter_ 创建的滤镜中使用。

      仅在滤镜的 "getframe" 函数内使用。
      
----------

   .. _setFilterError:

   void setFilterError(const char \*errorMessage, VSFrameContext_ \*frameCtx)

      向帧上下文添加错误消息，替换现有消息（如果有的话）。

      这是在滤镜的 "getframe" 函数中报告错误的方式。此类错误不一定是致命的，即调用者可以尝试再次请求同一帧。

函数
#########

.. _getVapourSynthAPI:

const VSAPI_\* getVapourSynthAPI(int version)

   返回全局 VSAPI 实例的指针。

   如果不支持请求的 API 版本或系统不满足运行 VapourSynth 的最低要求则返回 NULL。建议传递 VAPOURSYNTH_API_VERSION_。
   

编写插件
###############


A simple VapourSynth plugin which exports one filter will contain five
functions: an entry point (called ``VapourSynthPluginInit2``), a function tasked
with creating a filter instance (often called ``fooCreate``), an "init" function
(often called ``fooInit``), a "getframe" function (often called ``fooGetframe``),
and a "free" function (often called ``fooFree``). These functions are described
below.

滤镜还需要一个对象来存储滤镜实例的私有数据。此对象通常包含滤镜的输入节点（如果有的话）和一个描述滤镜要返回的视频的 VSVideoInfo_ 结构体。

VapourSynth 源代码中的 `sdk <https://github.com/vapoursynth/vapoursynth/tree/master/sdk>`_ 文件夹包含一些示例。

----------

.. _VSInitPlugin:

typedef void (VS_CC \*VSInitPlugin)(VSPlugin_ \*plugin, const VSPLUGINAPI_ \*vspapi)

   插件的入口点。必须命名为 ``VapourSynthPluginInit2``。此函数在核心加载共享库后被调用。其目的是配置插件并注册插件要导出的滤镜。

   *plugin*
      指向要初始化的插件对象的指针。

   *vspapi*
      指向 VSPLUGINAPI_ 结构体的指针，其中包含用于初始化插件的 VapourSynth API 子集。正确的做法是调用 configPlugin_，然后为每个要导出的函数调用 registerFunction_。

----------

.. _VSFilterGetFrame:

typedef const VSFrame_ \*(VS_CC \*VSFilterGetFrame)(int n, int activationReason, void \*instanceData, void \**frameData, VSFrameContext_ \*frameCtx, VSCore_ \*core, const VSAPI_ \*vsapi)

   滤镜的 "getframe" 函数。当核心需要滤镜生成帧时调用它。

   可以分配局部数据，在请求输出帧的多次调用期间持久存在。

   出错时，调用 setFilterError_\ ()，如需要则释放 \*frameData，然后返回 NULL。

   根据为滤镜设置的 VSFilterMode_，可能会同时请求多个输出帧。

   对于同一帧编号，永远不会并发调用。

   *n*
      请求的帧编号。

   *activationReason*
      VSActivationReason_ 中的一个。

      此函数首先以 *activationReason* arInitial 被调用。此时函数应请求所需的输入帧并返回 NULL。当一个或所有请求的帧准备好时，此函数以 arAllFramesReady 再次被调用。函数应仅在以 *activationReason* arAllFramesReady 调用时返回帧。

      如果以 arError 调用函数，所有处理必须中止。

   *instanceData*
      滤镜的私有实例数据。

   *frameData*
      与输出帧编号 *n* 关联的可选私有数据。必须在给定帧的最后一次调用（arAllFramesReady 或 error）之前释放。

      它指向一个可以自由使用的 void \*[4] 内存数组。有关示例，请参阅 Splice 和 Trim 等滤镜。

   当输出帧编号 *n* 准备好时返回其引用，否则返回 NULL。帧的所有权转移给调用者。

----------

.. _VSFilterFree:

typedef void (VS_CC \*VSFilterFree)(void \*instanceData, VSCore_ \*core, const VSAPI_ \*vsapi)

   滤镜的 "free" 函数。

   滤镜应在此处释放其分配的所有内容，包括其实例数据。

   *instanceData*
      滤镜的私有实例数据。
