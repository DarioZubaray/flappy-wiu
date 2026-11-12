import re
from os.path import join

from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.toolchain import current_directory


class PygameCERecipe(CompiledComponentsPythonRecipe):
    """
    Recipe to build apps based on SDL2-based pygame-ce.

    Local recipe (based on kivy/python-for-android PR #2971 and the
    upstream pygame recipe) since pygame-ce is not merged yet.
    """

    version = '2.5.8'
    url = 'https://github.com/pygame-community/pygame-ce/archive/refs/tags/{version}.tar.gz'

    site_packages_name = 'pygame'
    name = 'pygame-ce'

    depends = ['sdl2', 'sdl2_image', 'sdl2_mixer', 'sdl2_ttf', 'setuptools', 'jpeg', 'png']
    hostpython_prerequisites = ['setuptools', 'cython<=3.2.9']
    call_hostpython_via_targetpython = False  # Due to setuptools
    install_in_hostpython = False

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            setup_template = open(join("buildconfig", "Setup.Android.SDL2.in")).read()
            env = self.get_recipe_env(arch)
            env['ANDROID_ROOT'] = join(self.ctx.ndk.sysroot, 'usr')

            png = self.get_recipe('png', self.ctx)
            png_lib_dir = join(png.get_build_dir(arch.arch), '.libs')
            png_inc_dir = png.get_build_dir(arch)

            jpeg = self.get_recipe('jpeg', self.ctx)
            jpeg_inc_dir = jpeg_lib_dir = jpeg.get_build_dir(arch.arch)

            sdl_mixer_includes = ""
            sdl2_mixer_recipe = self.get_recipe('sdl2_mixer', self.ctx)
            for include_dir in sdl2_mixer_recipe.get_include_dirs(arch):
                sdl_mixer_includes += f"-I{include_dir} "

            sdl2_image_includes = ""
            sdl2_image_recipe = self.get_recipe('sdl2_image', self.ctx)
            for include_dir in sdl2_image_recipe.get_include_dirs(arch):
                sdl2_image_includes += f"-I{include_dir} "

            setup_file = setup_template.format(
                sdl_includes=(
                    " -I" + join(self.ctx.bootstrap.build_dir, 'jni', 'SDL', 'include') +
                    " -L" + join(self.ctx.bootstrap.build_dir, "libs", str(arch)) +
                    " -L" + png_lib_dir + " -L" + jpeg_lib_dir + " -L" + arch.ndk_lib_dir_versioned),
                sdl_ttf_includes="-I" + join(self.ctx.bootstrap.build_dir, 'jni', 'SDL2_ttf'),
                sdl_image_includes=sdl2_image_includes,
                sdl_mixer_includes=sdl_mixer_includes,
                jpeg_includes="-I" + jpeg_inc_dir,
                png_includes="-I" + png_inc_dir,
                freetype_includes=""
            )
            open("Setup", "w").write(setup_file)

            # pygame-ce 2.5.x uses the meson-python backend, which cannot
            # cross-compile for Android (its sanity check tries to *run* an
            # arm64 binary). Force the setuptools backend so `pip install .`
            # goes through setup.py instead.
            pyproject = open("pyproject.toml").read()
            pyproject = re.sub(
                r"\[build-system\].*?(?=\n\[|\Z)",
                '[build-system]\n'
                'requires = ["setuptools>=61", "cython<=3.2.9"]\n'
                'build-backend = "setuptools.build_meta"\n\n',
                pyproject,
                count=1,
                flags=re.S,
            )
            open("pyproject.toml", "w").write(pyproject)

            # PEP 517 execs setup.py with sys.path lacking the source dir
            # (so `import buildconfig` fails) and sys.argv[0] pointing at the
            # hook script (so setup.py's chdir(dirname(argv[0])) lands in the
            # wrong dir). Mimic `python setup.py` for both.
            setup_py = open("setup.py").read()
            if "sys.path.insert(0, os.path.dirname" not in setup_py:
                setup_py = (
                    "import os, sys\n"
                    "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
                    "sys.argv[0] = __file__\n"
                    + setup_py
                )
                open("setup.py", "w").write(setup_py)
            elif "sys.argv[0] = __file__" not in setup_py:
                # cached copy from an older recipe revision: add missing line
                setup_py = setup_py.replace(
                    "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n",
                    "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
                    "sys.argv[0] = __file__\n",
                    1,
                )
                open("setup.py", "w").write(setup_py)

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['USE_SDL2'] = '1'
        env["PYGAME_CROSS_COMPILE"] = "TRUE"
        env["PYGAME_ANDROID"] = "TRUE"
        return env


recipe = PygameCERecipe()
