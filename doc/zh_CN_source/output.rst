输出
======

VS管道
######

概要
********

**vspipe** <脚本> <输出文件> [选项]

vspipe 的主要用途是执行 VapourSynth 脚本到输出文件。

如果 *outfile* 是连字符 (``-``)，vspipe 将写入标准输出。

如果 *outfile* 是双连字符 (``--``)，vspipe 将常执行所有操作，但不会将视频帧写入任何位置。


选项
*******

``-a, --arg key=value``
    传递给脚本环境的参数，将在全局字典中设置一个具有该名称和值（字符串类型）的键

``-s, --start N``
    设置输出帧范围（第一帧）
  
``-e, --end N``
    设置输出帧范围（最后一帧）

``-o, --outputindex N``
    选择输出索引

``-r, --requests N``
    设置并发帧请求数

``-c, --container <y4m/wav/w64>``
    为输出添加指定格式的头信息

``-t, --timecodes FILE``
    写入时间码 v2 文件

``-p, --progress``
    将文档打印到 stderr
    
``--filter-time``
    记录每个滤镜的耗时，并在处理结束时打印。

``-i, --info``
    显示视频信息并退出

``-g, --graph <simple/full>``
    将输出节点的过滤图以dot格式打印到输出文件并退出

``-v, --version``
    显示版本信息并退出


示例
********

显示脚本信息：
    ``vspipe --info script.vpy -``

写入标准输出：
    ``vspipe [options] script.vpy -``

写入管道（仅限Windows）：
    ``vspipe [options] script.vpy "\\\\.\\pipe\\<pipename>"``

请求所有帧但不输出：
    ``vspipe [options] script.vpy --``

将第 5-100 帧写入文件：
    ``vspipe --start 5 --end 100 script.vpy output.raw``

管道传输到 x264 并写入时间码文件：
    ``vspipe script.vpy - -c y4m --timecodes timecodes.txt | x264 --demuxer y4m -o script.mkv -``

向脚本传递值：
    ``vspipe --arg deinterlace=yes --arg "message=fluffy kittens" script.vpy output.raw``

AVFS（虚拟文件系统输出）
########################

AV FileSystem总是基于`AVFS <https://turtlewar.org/avfs/>`_，共享大部分源和功能。这个集合有多种用途。它可以让脚本文件看起来像一个真实的未压缩的avi文件，从而使任何应用程序随时打开。它还可以用于弥合32/64位差距，因为普通文件可以被读取。

使用方法很简单，只需在 ``core32`` 或 ``core64`` 目录中运行 ``avfs``，以脚本名作为参数。这将在 ``C:\Volumes`` 中创建一个虚拟文件。

*set_output* 的 *alt_output* 参数会受到尊重，可用于获得与专业应用程序的额外兼容性。

Avisynth 支持
****************

请注意，此 AVFS 版本也与 Avisynth 2.6 和 Avisynth+ 兼容。使用 Avisynth+ 时还支持更高位深的输出。获取最新版本的最简单方法是从 VapourSynth 便携式归档中提取 ``avfs.exe``。

视觉FW
###

在Windows上，您可以将视频输出到基于VFW的程序。

如果通过安装程序安装VapourSynth，VSVFW.dll 已经注册

否则，您可以手动注册，使用下面的注册文件或使用 `theChaosCoder 的批处理脚本 <https://github.com/theChaosCoder/vapoursynth-portable-FATPACK/blob/master/VapourSynth64Portable/extras/enable_vfw_support.bat>`_。

::

    Windows Registry Editor Version 5.00

    [HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{58F74CA0-BD0E-4664-A49B-8D10E6F0C131}]
    @="VapourSynth"

    [HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{58F74CA0-BD0E-4664-A49B-8D10E6F0C131}\InProcServer32]
    @="<your VSVFW.dll directory>\\VSVFW.dll"
    "ThreadingModel"="Apartment"

    [HKEY_LOCAL_MACHINE\SOFTWARE\Classes\AVIFile\Extensions\VPY]
    @="{58F74CA0-BD0E-4664-A49B-8D10E6F0C131}"
