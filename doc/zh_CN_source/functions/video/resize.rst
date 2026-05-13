调整大小
============

.. function::   Bilinear(vnode clip[, int width, int height, int format, enum matrix, enum transfer, enum primaries, enum range, enum chromaloc, enum matrix_in, enum transfer_in, enum primaries_in, enum range_in, enum chromaloc_in, float filter_param_a, float filter_param_b, string resample_filter_uv, float filter_param_a_uv, float filter_param_b_uv, string dither_type="none", string cpu_type, float src_left, float src_top, float src_width, float src_height, float nominal_luminance, bint approximate_gamma=True])
                Bicubic(vnode clip[, ...])
                Point(vnode clip[, ...])
                Lanczos(vnode clip[, ...])
                Spline16(vnode clip[, ...])
                Spline36(vnode clip[, ...])
                Spline64(vnode clip[, ...])
                Bob(vnode clip, string filter="bicubic", bint tff[, ...])
   :module: resize
   
   在 VapourSynth 中，缩放器具有多种功能。除了缩放外，它们还进行色彩空间转换以及与兼容格式之间的转换。Resize 将已知或未知格式的剪辑转换为另一个已知或未知格式的剪辑，仅更改用户指定的参数。缩放滤镜可以处理不同尺寸和格式的输入剪辑，并将其转换为固定格式的剪辑。

   如果你不知道选择哪个调整大小器，试试 Bicubic。它通常是一个很好的中性默认选择。

   *Bob* 可用作基本的去隔行器。

   类型标记为 *enum* 的参数可以通过数字索引（参见 ITU-T H.273，视频代码点）或名称指定。通过名称指定的枚举，其参数名称以 "_s" 为后缀。例如，BT 709 的目标矩阵可以用 ``matrix=1`` 或 ``matrix_s="709"`` 指定。

   注意在转换为 YUV 时 *matrix* 不是可选参数。另外注意，如果输入 YUV 帧的属性中未指定矩阵，则还需要设置 *matrix_in*。
   
   如果不遵守子采样限制，函数将返回错误。  

   如果出现如下错误::

      Resize error 3074: no path between colorspaces (2/2/2 => 1/1/1).
      May need to specify additional colorspace parameters.

   这通常表示 matrix/transfer/primaries 未知，你需要手动指定输入色彩空间参数。
   注意：按照 ITU-T 建议，数值 2 表示“未指定（unspecified）”。

   对于隔行图像，如 *_FieldBased* 帧属性所示，缩放是按场执行的。源滤镜有时可能将逐行视频标记为隔行，这可能导致非最优的重采样质量，除非清除 *_FieldBased*。

   clip（输入片段）:
   
      接受所有类型的输入。

   width、height（输出宽高）:
   
      输出图像尺寸。

   filter（去隔行缩放器）:

      去隔行的缩放方法。参见 *resample_filter_uv* 了解可接受的值。

   tff（顶场优先标记）:

      去隔行的场顺序。当未设置 *_FieldBased* 属性时使用。

   format（输出格式）:
   
      输出格式 ID。

   matrix、transfer、primaries（输出色彩参数）:

      输出色彩空间规范。如果未提供，将选择输入剪辑的对应属性，但 YCoCg 和 RGB 色彩族除外，它们默认设置对应的矩阵。

   range（输出像素范围）:

      输出像素范围。对于整数格式，这允许选择合法的代码值。即使设置了，也可能生成超出范围的值 (BTB/WTW)。如果输入格式属于不同的色彩族，YUV 的默认范围是 studio/limited，RGB 为 full-range。

   chromaloc（输出色度位置）:
   
      输出色度位置。对于子采样格式，用于指定色度采样位置。
      如果输入格式是 4:4:4 或 RGB 且输出为子采样格式，默认位置按 MPEG 规则为左对齐。
      可用色度位置（ITU-T H.273 图 10）包括：
      left、center、top_left、top、bottom_left、bottom 等位置。
      
   matrix_in、transfer_in、primaries_in、range_in、chromaloc_in（输入色彩参数）:
   
      输入色彩空间/格式规范。如果对应的帧属性设置为非「未指定」的值，则使用帧属性而非此参数。某些色彩族设有默认值。有关更多信息，请参阅等效的输出参数。

   filter_param_a、filter_param_b（Y/RGB 参数）:
   
      用于 RGB 和 Y 通道的缩放器参数。对于双三次滤波器，filter_param_a/b 表示 "b" 和 "c" 参数。对于 lanczos 滤波器，filter_param_a 表示抽头数。

   resample_filter_uv（UV 缩放器）:
   
      UV 通道的缩放方法。默认与 Y 通道一致。
      resample_filter_uv 可用值包括：point、bilinear、bicubic、
      spline16、spline36、lanczos 等方法。

   filter_param_a_uv、filter_param_b_uv（UV 参数）:

      用于 UV 通道的缩放器参数。

   dither_type（抖动类型）:
   
      抖动方法。抖动仅在转换结果为整数格式时使用。
      可用抖动方法有：none、ordered、random、error_diffusion。
      
   cpu_type（CPU 类型）:
   
      仅用于测试。
      
   src_left、src_top、src_width、src_height（源区域）:
   
      用于选择要使用的输入源区域。也可用于偏移图像。默认为整个图像。
      
   nominal_luminance（标称亮度）:
   
      确定值 1.0 的物理亮度。单位为 cd/m^2。
      
   approximate_gamma（近似 gamma）:

      使用 LUT 评估传输函数。默认为 True。
      
   转换到 YV12 的示例::

      Bicubic(clip=clip, format=vs.YUV420P8, matrix_s="709")

   将带有色彩信息帧属性的 YUV 调整大小并转换为平面 RGB::

      Bicubic(clip=clip, width=1920, height=1080, format=vs.RGB24)

   将不带色彩信息帧属性的 YUV 调整大小并转换为平面 RGB::

      Bicubic(clip=clip, width=1920, height=1080, format=vs.RGB24, matrix_in_s="709")

   以下表格列出了选定色彩空间枚举的值及其缩写名称。（数值在括号中。）有关所有可能的值，请参见 ITU-T H.273。

      Matrix coefficients (ITU-T H.273 Table 4)::
        
        rgb (0)        Identity
                       The identity matrix.
                       Typically used for GBR (often referred to as RGB);
                       however, may also be used for YZX (often referred to as
                       XYZ);
        709 (1)        KR = 0.2126; KB = 0.0722
                       ITU-R Rec. BT.709-6
        unspec (2)     Unspecified
                       Image characteristics are unknown or are determined by the
                       application.
        fcc (4)        KR = 0.30; KB = 0.11
        470bg (5)      KR = 0.299; KB = 0.114
                       ITU-R Rec. BT.470-6 System B, G (historical)
                       (functionally the same as the value 6 (170m))
        170m (6)       KR = 0.299; KB = 0.114
                       SMPTE ST 170
                       (functionally the same as the value 5 (470bg))
        240m (7)       KR = 0.212; KB = 0.087
                       SMPTE ST 240
        ycgco (8)      YCgCo
        2020ncl (9)    KR = 0.2627; KB = 0.0593
                       Rec. ITU-R BT.2020 non-constant luminance system
        2020cl (10)    KR = 0.2627; KB = 0.0593
                       Rec. ITU-R BT.2020 constant luminance system
        chromancl (12) Chromaticity derived non-constant luminance system
        chromacl (13)  Chromaticity derived constant luminance system
        ictcp (14)     Rec. ITU-R BT.2100-2 ICtCp

      Transfer characteristics (ITU-T H.273 Table 3)::
        
        709 (1)        V = a * Lc0.45 - ( a - 1 ) for 1 >= Lc >= b
                       V = 4.500 * Lc for b > Lc >= 0
                       Rec. ITU-R BT.709-6
                       (functionally the same as the values 6 (601),
                       14 (2020_10) and 15 (2020_12))
        unspec (2)     Unspecified
                       Image characteristics are unknown or are determined by the
                       application.
        470m (4)       ITU-R Rec. BT.470-6 System M (historical)
        470bg (5)      ITU-R Rec. BT.470-6 System B, G (historical)
        601 (6)        V = a * Lc0.45 - ( a - 1 ) for 1 >= Lc >= b
                       V = 4.500 * Lc for b > Lc >= 0
                       Rec. ITU-R BT.601-7 525 or 625
                       (functionally the same as the values 1 (709),
                       14 (2020_10) and 15 (2020_12))
        240m (7)       SMPTE ST 240
        linear (8)     V = Lc for all values of Lc
                       Linear transfer characteristics
        log100 (9)     Log 1:100 contrast
        log316 (10)    Log 1:316 contrast
        xvycc (11)     IEC 61966-2-4
        srgb (13)      IEC 61966-2-1
        2020_10 (14)   V = a * Lc0.45 - ( a - 1 ) for 1 >= Lc >= b
                       V = 4.500 * Lc for b > Lc >= 0
                       Rec. ITU-R BT.2020
                       (functionally the same as the values 1 (709),
                       6 (601) and 15 (2020_12))
        2020_12 (15)   V = a * Lc0.45 - ( a - 1 ) for 1 >= Lc >= b
                       V = 4.500 * Lc for b > Lc >= 0
                       Rec. ITU-R BT.2020
                       (functionally the same as the values 1 (709),
                       6 (601) and 14 (2020_10))
        st2084 (16)    SMPTE ST 2084
        st428 (17)     SMPTE ST 428-1
        std-b67 (18)   ARIB std-b67

      Color primaries (ITU-T H.273 Table 2)::
      
        709 (1)        primary x y
                       green 0.300 0.600
                       blue 0.150 0.060
                       red 0.640 0.330
                       white D65 0.3127 0.3290
                       Rec. ITU-R BT.709-6
        unspec (2)     Unspecified
                       Image characteristics are unknown or are determined by the
                       application.
        470m (4)       ITU-R Rec. BT.470-6 System M
        470bg (5)      ITU-R Rec. BT.470-6 System B, G (historical)
        170m (6)       primary x y
                       green 0.310 0.595
                       blue 0.155 0.070
                       red 0.630 0.340
                       white D65 0.3127 0.3290
                       SMPTE ST 170
                       (functionally the same as the value 7 (240m))
        240m (7)       primary x y
                       green 0.310 0.595
                       blue 0.155 0.070
                       red 0.630 0.340
                       white D65 0.3127 0.3290
                       SMPTE ST 240
                       (functionally the same as the value 6 (170m))
        film (8)
        2020 (9)       primary x y
                       green 0.170 0.797
                       blue 0.131 0.046
                       red 0.708 0.292
                       white D65 0.3127 0.3290
                       Rec. ITU-R BT.2020
        st428 (10)     Commonly known as xyz
        xyz (10)       Alias for st428
        st431-2 (11)   DCI-P3 with traditional white point
        st432-1 (12)   DCI-P3
        jedec-p22 (22) E.B.U. STANDARD FOR CHROMATICITY TOLERANCES FOR STUDIO MONITORS (3213-E)
                       Also known as JEDEC P22

      Pixel range (ITU-T H.273 equations for matrix coefficients)::
      
        limited (0) Studio (TV) legal range, 16-235 in 8 bits.
                    Y = Clip1Y( Round( ( 1 << ( BitDepthY - 8 ) ) *
                                              ( 219 * E′Y + 16 ) ) )
                    Cb = Clip1C( Round( ( 1 << ( BitDepthC - 8 ) ) *
                                               ( 224 * E′PB + 128 ) ) )
                    Cr = Clip1C( Round( ( 1 << ( BitDepthC - 8 ) ) *
                                               ( 224 * E′PR + 128 ) ) )

                    R = Clip1Y( ( 1 << ( BitDepthY - 8 ) ) *
                                       ( 219 * E′R + 16 ) )
                    G = Clip1Y( ( 1 << ( BitDepthY - 8 ) ) *
                                       ( 219 * E′G + 16 ) )
                    B = Clip1Y( ( 1 << ( BitDepthY - 8 ) ) *
                                       ( 219 * E′B + 16 ) )
        full (1)    Full (PC) dynamic range, 0-255 in 8 bits.
                    Y = Clip1Y( Round( ( ( 1 << BitDepthY ) - 1 ) * E′Y ) )
                    Cb = Clip1C( Round( ( ( 1 << BitDepthC ) - 1 ) * E′PB +
                                          ( 1 << ( BitDepthC - 1 ) ) ) )
                    Cr = Clip1C( Round( ( ( 1 << BitDepthC ) - 1 ) * E′PR +
                                          ( 1 << ( BitDepthC - 1 ) ) ) )

                    R = Clip1Y( ( ( 1 << BitDepthY ) - 1 ) * E′R )
                    G = Clip1Y( ( ( 1 << BitDepthY ) - 1 ) * E′G )
                    B = Clip1Y( ( ( 1 << BitDepthY ) - 1 ) * E′B )




