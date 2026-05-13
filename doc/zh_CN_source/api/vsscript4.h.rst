VSScript4.h（脚本接口头文件）
===============================

目录
#################

简介_


结构体_
    VSScript_（脚本环境）
   
    VSScriptAPI_（API 结构体）
   
   
函数_
    getVSScriptAPI_（获取 API 入口）

    getApiVersion_（获取 API 版本）
      
    getVSAPI_（获取 VSAPI）
      
    createScript_（创建脚本环境）
      
    getCore_（获取核心）
      
    evaluateBuffer_（评估脚本字符串）
      
    evaluateFile_（评估脚本文件）
      
    getError_（获取错误信息）
      
    getExitCode_（获取退出码）
   
    getVariable_（读取变量）
     
    setVariables_（设置变量）
      
    getOutputNode_（获取输出节点）
      
    getOutputAlphaNode_（获取输出 Alpha 节点）
      
    getAltOutputMode_（获取替代输出模式）
      
    freeScript_（释放脚本环境）
      
    evalSetWorkingDir_（设置评估工作目录）


简介
############

VSScript 为 VapourSynth 的脚本接口提供了一个便捷的封装，允许评估 VapourSynth 脚本和获取输出剪辑。

目前，VapourSynth 脚本只能使用 Python（版本 3）编写。

以下是一些使用 VSScript 库的项目：

    * 工具 vspipe：`vspipe <https://github.com/vapoursynth/vapoursynth/blob/master/src/vspipe/vspipe.cpp>`_

    * 工具 vsvfw：`vsvfw <https://github.com/vapoursynth/vapoursynth/blob/master/src/vfw/vsvfw.cpp>`_

    * 示例程序：`vsscript_example.c <https://github.com/vapoursynth/vapoursynth/blob/master/sdk/vsscript_example.c>`_

    * 视频播放器：`mpv <https://github.com/mpv-player/mpv/blob/master/video/filter/vf_vapoursynth.c>`_

.. note::
    如果使用 dlopen() 加载 libvsscript，必须使用 RTLD_GLOBAL 标志。否则 Python 将无法导入二进制模块。这是 Python 设计导致的限制。


结构体
#######

VSScript
--------

脚本环境。与评估脚本的所有评估和通信都通过 VSScript 对象进行。


VSScriptAPI
-----------

此结构体是访问 VSScript 公共 API 的方式。


函数
#########

getVSScriptAPI
--------------

.. c:function:: const VSSCRIPTAPI *getVSScriptAPI(int version)

    返回包含 API 函数指针的结构体。如果不支持指定的 *version* 则返回 NULL。
    
    建议始终传递 *VSSCRIPT_API_VERSION*。
    

getApiVersion
-------------

.. c:function:: int getApiVersion()

    返回 vsscript 提供的 API 版本。

    
getVSAPI
--------

.. c:function:: const VSAPI *getVSAPI(int version)

    获取 VSAPI 结构体。主要是为了方便，这样就不必显式加载 vapoursynth 模块。

    如果 VapourSynth 库不提供请求的版本，这可能返回 NULL。


createScript
------------

.. c:function:: VSScript *createScript(VSCore *core)

    创建一个可用于评估脚本的空脚本环境。传递预创建的 *core* 可用于自定义核心创建标志、日志回调或预加载插件。传递 NULL 将自动使用默认设置创建新核心。
    
    无论成功或失败都接管 *core* 的所有权。出错时返回 NULL。


getCore
-------

.. c:function:: VSCore *getCore(VSScript *handle)

    获取在脚本环境中创建的 VapourSynth 核心。如果尚未创建 VapourSynth 核心，将使用默认选项创建（参见 :doc:`../pythonreference`）。
    
    VSScript 保留返回的核心对象的所有权。

    出错时返回 NULL。




evaluateBuffer
--------------

.. c:function:: int evaluateBuffer(VSScript *handle, const char *buffer, const char *scriptFilename)

    评估包含在 C 字符串中的脚本。可以在同一脚本环境上多次调用以逐步添加更多处理。

    handle（脚本环境指针）
        指向脚本环境的指针。

    buffer（脚本文本）
        要评估的完整脚本，作为 C 字符串。

    scriptFilename（脚本名称）
        脚本的名称，将在错误消息中显示。如果为 NULL，将使用名称 "<string>"。
        
        如果此值非 NULL，特殊变量 ``__file__`` 将设置为 *scriptFilename* 的绝对路径。

    出错时返回非零值。可以使用 getError_\ () 获取错误消息。如果脚本调用 *sys.exit(code)*，可以使用 getExitCode_\ () 获取退出码。可以在此函数之前调用 evalSetWorkingDir_\ () 来更改工作目录行为。
    
    
evaluateFile
------------

.. c:function:: int evaluateFile(VSScript **handle, const char *scriptFilename)

    评估文件中包含的脚本。这是一个便捷函数，它为您从文件中读取脚本。它只读取前 16 MiB，这对每个人都应该足够了。

    行为与 evaluateBuffer\ () 相同。


getError
--------

.. c:function:: const char *getError(VSScript *handle)

    返回脚本环境中的错误消息，如果没有错误则返回 NULL。

    传递 NULL 是可以的。
    
    VSScript 保留指针的所有权，并且只保证在对 *handle* 的下一次 vsscript 操作之前有效。


getExitCode
-----------

.. c:function:: int getExitCode(VSScript *handle)

    如果脚本调用 *sys.exit(code)* 则返回退出码，如果脚本因其他原因失败或调用 *sys.exit(0)* 则返回 0。

    传递 NULL 是可以的。


getVariable
-----------

.. c:function:: int getVariable(VSScript *handle, const char *name, VSMap *dst)

    从脚本环境中获取变量。

    如果脚本环境中尚未创建 VapourSynth 核心，将使用默认选项创建一个（参见 :doc:`../pythonreference`）。

    name（变量名）
        要获取的变量名称。

    dst（输出映射）
        变量值将放置的映射表，键为 *name*。

    出错时返回非零值。


setVariables
------------

.. c:function:: int vsscript_setVariable(VSScript *handle, const VSMap *vars)

    在脚本环境中设置变量。

    变量现在可供脚本使用。

    如果脚本环境中尚未创建 VapourSynth 核心，将使用默认选项创建一个（参见 :doc:`../pythonreference`）。

    vars（输入变量映射）
        包含要设置的变量的映射表。

    出错时返回非零值。


getOutputNode
-------------

.. c:function:: VSNode *getOutputNode(VSScript *handle, int index)

    从脚本环境中获取节点。脚本中的节点必须已使用请求的 *index* 标记为输出。

    返回的节点其引用计数增加了一。

    如果请求的索引处没有节点则返回 NULL。

    
getOutputAlphaNode
------------------

.. c:function:: VSNode *getOutputAlphaNode(VSScript *handle, int index)

    从脚本环境中获取 alpha 节点。脚本中具有关联 alpha 的节点必须已使用请求的 *index* 标记为输出。

    返回的节点其引用计数增加了一。

    如果请求的索引处没有 alpha 节点则返回 NULL。


getAltOutputMode
----------------

.. c:function:: int getAltOutputMode(VSScript *handle, int index)

    从脚本中获取替代输出模式设置。此值没有固定含义，但在 vspipe 和 vsvfw 中，它表示在有多种输出格式可用时应使用替代输出格式。由客户端应用程序定义确切含义或完全忽略它。

    如果没有设置替代输出模式则返回 0。


freeScript
----------

.. c:function:: void freeScript(VSScript *handle)

    释放脚本环境。*handle* 不再可用。

    * 取消脚本环境中设置为输出的所有剪辑。

    * 清除脚本环境中设置的所有变量。

    * 清除脚本环境中的错误消息（如果有的话）。

    * 释放脚本环境中使用的 VapourSynth 核心（如果有的话）。

    由于此函数释放 VapourSynth 核心，因此必须在所有帧请求完成且从脚本获取的所有对象（帧、节点等）都已释放后才能调用。

    传递 NULL 是安全的。


evalSetWorkingDir
-----------------

.. c:function:: void evalSetWorkingDir(VSScript *handle, int setCWD)

    设置在调用 evaluateFile 时是否临时将工作目录更改为与脚本文件相同的位置。默认关闭。
