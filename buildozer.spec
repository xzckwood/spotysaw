[app]

title = spotysaw
package.name = spotysaw
package.domain = org.spotysaw

source.dir = .
source.include_exts = py,jpg,jpeg,png,json
source.include_patterns = home_bg.jpg

version = 1.0

requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 23
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
