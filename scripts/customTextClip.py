import os
from moviepy.video.VideoClip import ImageClip
from moviepy.decorators import convert_path_to_string

class CustomTextClip(ImageClip):
    """Class for autogenerated text clips.

    Creates an ImageClip originating from a script-generated text image.
    Requires ImageMagick.

    Parameters
    ----------

    text
      A string of the text to write. Can be replaced by argument
      ``filename``.

    filename
      The name of a file in which there is the text to write,
      as a string or a path-like object.
      Can be provided instead of argument ``txt``

    size
      Size of the picture in pixels. Can be auto-set if
      method='label', but mandatory if method='caption'.
      the height can be None, it will then be auto-determined.

    bg_color
      Color of the background. See ``TextClip.list('color')``
      for a list of acceptable names.

    color
      Color of the text. See ``TextClip.list('color')`` for a
      list of acceptable names.

    font
      Name of the font to use. See ``TextClip.list('font')`` for
      the list of fonts you can use on your computer.

    stroke_color
      Color of the stroke (=contour line) of the text. If ``None``,
      there will be no stroke.

    stroke_width
      Width of the stroke, in pixels. Can be a float, like 1.5.

    method
      Either 'label' (default, the picture will be autosized so as to fit
      exactly the size) or 'caption' (the text will be drawn in a picture
      with fixed size provided with the ``size`` argument). If `caption`,
      the text will be wrapped automagically (sometimes it is buggy, not
      my fault, complain to the ImageMagick crew) and can be aligned or
      centered (see parameter ``align``).

    kerning
      Changes the default spacing between letters. For
      instance ``kerning=-1`` will make the letters 1 pixel nearer from
      ach other compared to the default spacing.

    align
      center | East | West | South | North . Will only work if ``method``
      is set to ``caption``

    transparent
      ``True`` (default) if you want to take into account the
      transparency in the image.
    """

    @convert_path_to_string("filename")
    def __init__(
        self,
        text=None,
        filename=None,
        size=None,
        color="black",
        bg_color="transparent",
        font_size=None,
        font="Courier",
        stroke_color=None,
        stroke_width=1,
        method="label",
        kerning=None,
        align="center",
        interline=None,
        tempfilename=None,
        temptxt=None,
        transparent=True,
        remove_temp=True,
        print_cmd=False,
        rotate = None
    ):

        if text is not None:
            if temptxt is None:
                temptxt_fd, temptxt = tempfile.mkstemp(suffix=".txt")
                try:  # only in Python3 will this work
                    os.write(temptxt_fd, bytes(text, "UTF8"))
                except TypeError:  # oops, fall back to Python2
                    os.write(temptxt_fd, text)
                os.close(temptxt_fd)
            text = "@" + temptxt
        else:
            # use a file instead of a text.
            text = "@%" + filename

        if size is not None:
            size = (
                "" if size[0] is None else str(size[0]),
                "" if size[1] is None else str(size[1]),
            )

        cmd = [
            IMAGEMAGICK_BINARY,
            "-background",
            bg_color,
            "-fill",
            color,
            "-font",
            font,
        ]

        if font_size is not None:
            cmd += ["-pointsize", "%d" % font_size]
        if kerning is not None:
            cmd += ["-kerning", "%0.1f" % kerning]
        if stroke_color is not None:
            cmd += ["-stroke", stroke_color, "-strokewidth", "%.01f" % stroke_width]
        if size is not None:
            cmd += ["-size", "%sx%s" % (size[0], size[1])]
        if align is not None:
            cmd += ["-gravity", align]
        if interline is not None:
            cmd += ["-interline-spacing", "%d" % interline]
        if rotate is not None:
            cmd += ["-rotate", "%d" % rotate]

        if tempfilename is None:
            tempfile_fd, tempfilename = tempfile.mkstemp(suffix=".png")
            os.close(tempfile_fd)

        cmd += [
            "%s:%s" % (method, text),
            "-type",
            "truecolormatte",
            "PNG32:%s" % tempfilename,
        ]

        if print_cmd:
            print(" ".join(cmd))

        try:
            subprocess_call(cmd, logger=None)
        except (IOError, OSError) as err:
            error = (
                f"MoviePy Error: creation of {filename} failed because of the "
                f"following error:\n\n{err}.\n\n."
                "This error can be due to the fact that ImageMagick "
                "is not installed on your computer, or (for Windows "
                "users) that you didn't specify the path to the "
                "ImageMagick binary. Check the documentation."
            )
            raise IOError(error)

        ImageClip.__init__(self, tempfilename, transparent=transparent)
        self.text = text
        self.color = color
        self.stroke_color = stroke_color

        if remove_temp:
            if tempfilename is not None and os.path.exists(tempfilename):
                os.remove(tempfilename)
            if temptxt is not None and os.path.exists(temptxt):
                os.remove(temptxt)

    @staticmethod
    def list(arg):
        """Returns a list of all valid entries for the ``font`` or ``color`` argument of
        ``TextClip``.
        """
        popen_params = cross_platform_popen_params(
            {"stdout": sp.PIPE, "stderr": sp.DEVNULL, "stdin": sp.DEVNULL}
        )

        process = sp.Popen(
            [IMAGEMAGICK_BINARY, "-list", arg], encoding="utf-8", **popen_params
        )
        result = process.communicate()[0]
        lines = result.splitlines()

        if arg == "font":
            # Slice removes first 8 characters: "  Font: "
            return [line[8:] for line in lines if line.startswith("  Font:")]
        elif arg == "color":
            # Each line is of the format "aqua  srgb(0,255,255)  SVG" so split
            # on space and take the first item to get the color name.
            # The first 5 lines are header information, not colors, so ignore
            return [line.split(" ")[0] for line in lines[5:]]
        else:
            raise Exception("Moviepy Error: Argument must equal 'font' or 'color'")


    @staticmethod
    def search(string, arg):
        """Returns the of all valid entries which contain ``string`` for the
        argument ``arg`` of ``TextClip``, for instance

        >>> # Find all the available fonts which contain "Courier"
        >>> print(TextClip.search('Courier', 'font'))
        """
        string = string.lower()
        names_list = TextClip.list(arg)
        return [name for name in names_list if string in name.lower()]