from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class LibmmsConan(ConanFile):
    name = "libmms"
    version = "0.6.4"
    description = "libmms is a library for downloading (streaming) media files using the mmst and mmsh protocols."
    url = "https://github.com/conan-multimedia/libmms"
    homepage = "https://sourceforge.net/projects/libmms/"
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        tools.get('http://sourceforge.net/projects/libmms/files/{name}/{version}/{name}-{version}.tar.gz'.format(name=self.name,version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            _args = ["--prefix=%s/builddir"%(os.getcwd())]
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                excludes="*.a" if self.options.shared else  "*.so*"
                self.copy("*", src="%s/builddir"%(os.getcwd()), excludes=excludes)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

