# Video Renamer

**Disclaimer:** This is a work in progress. Code may be broken, take your cat as hostage or burn your whole house down. Handle with care.

Video Renamer is a tool to rename video files according to their meta data.

## Why?

Simple. I have saved many TED Talks, and wants them to be named neatly. I still download them, hence wanted a better way to rename, since they have nice, full meta data embedded.

Also, because [XKCD](http://www.xkcd.com)!

![Obligatory XKCD](https://imgs.xkcd.com/comics/automation.png)

## Dependencies

- The tool requires `exiftool` to read actual meta data. For Debian and its derivatives, `exiftool` can be installed by installing the `libimage-exiftool-perl` package.
- The code uses and bundles a recent (generally latest) version of smarnach's `pyexiftool` wrapper. See the source [here](https://github.com/smarnach/pyexiftool).
- The code is written to run with `python3` and will not work on **Python 2.x** environments.
