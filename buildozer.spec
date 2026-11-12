[buildozer]
log_level = 2
warn_on_root = 0

[app]
title = Flappy Wiu
package.name = flappywiu
package.domain = org.flappywiu
source.dir = .
source.include_exts = py,png,jpg,gif,ogg
source.exclude_exts = apk,log,pyc,pyo
source.exclude_patterns = assets/demo.gif,tests/*,.venv/*,.git/*,.github/*,p4a-recipes/*,bin/*,.buildozer/*
version = 0.1.0
requirements = python3,pygame-ce,Pillow
orientation = portrait
fullscreen = 1
android.permissions =
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.debug_artifact = apk
android.accept_sdk_license = True
p4a.local_recipes = ./p4a-recipes
p4a.branch = v2026.05.09
icon.filename = %(source.dir)s/assets/sprites/flappi-wiu-icon.png
android.allow_backup = 0
