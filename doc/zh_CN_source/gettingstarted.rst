快速入门
===============

现在您已经成功安装了 VapourSynth。下一步做什么？

如果你不了解Python基础，可以先看看这个`教程 <https://learnxinyminutes.com/docs/python3/>`_。

你可以在 Python 解释器中“随意尝试”，但大多数脚本不会这样创建。

示例脚本
##############

从一切 *.vpy* 脚本开始。以下是一个供参考的脚本脚本，假设已安装 `BestSource <https://github.com/vapoursynth/bestsource>`_ 并已 :doc:`自动加载 <installation>`。

.. code-block:: python

   from vapoursynth import core                     # Get an instance of the core
   clip = core.bs.VideoSource(source='filename.mkv')  # Load a video track in mkv file
   clip = core.std.FlipHorizontal(clip)             # Flip the video clip in the horizontal direction
   clip.set_output()                                # Set the video clip to be accessible for output

同样支持音频，使用 `BestSource <https://github.com/vapoursynth/bestsource>`_ 来加载音频文件。

.. code-block:: python

   from vapoursynth import core                     # Get an instance of the core
   clip = core.bs.AudioSource(source='filename.mkv')    # Load an audio track in mkv file
   clip = core.std.AudioGain(clip,gain=2.0)         # Gain all channels 2x
   clip.set_output()                                # Set the audio clip to be accessible for output

你可以在一个脚本中组合 2 个操作。

.. code-block:: python

   from vapoursynth import core
   video = core.bs.VideoSource(source='filename.mkv')
   audio = core.bs.AudioSource(source='filename.mkv')
   video = core.std.FlipHorizontal(video)
   audio = core.std.AudioGain(audio,gain=2.0)
   video.set_output(index=0)
   audio.set_output(index=1)

请记住，Python 中的大多数 VapourSynth 对象都有很好的字符串表示，如果想了解某个实例的更多信息，只需调用 ``print()``。

预览
#######

可以在 `VapourSynth Editor <https://github.com/YomikoR/VapourSynth-Editor>`_ 或 `VirtualDub FilterMod <https://sourceforge.net/projects/vdfiltermod/>`_ 中直接打开脚本进行预览。

使用 VPipe 输出
##################

VSPipe 非常适合将输出管道传输到各种应用程序，例如 x264 和 flac 用于编码。

以下是一些自动传递大多数视频和音频属性的命令行示例。

用于 x264::

   vspipe -c y4m script.vpy - | x264 --demuxer y4m - --output encoded.264

用于 flac::

   vspipe -c wav script.vpy - | flac - -o encoded.flac

用于 FFmpeg::

   vspipe -c y4m script.vpy - | ffmpeg -i - encoded.mkv

用于 mpv::

   vspipe -c y4m script.vpy - | mpv -
   vspipe -c wav script.vpy - | mpv -
