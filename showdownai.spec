# -*- mode: python -*-
a = Analysis(['server/showdownbot.py'],
             pathex=['/home/vasu/Work/pokemon_ai'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='showdownbot',
          debug=False,
          strip=None,
          upx=True,
          console=True )
dict_tree = Tree("data/", prefix="data")
static_tree = Tree("server/static/", prefix="static")
template_tree = Tree("server/templates/", prefix="templates")
selenium_tree = Tree("/Users/labuser/anaconda3/lib/python3.6/site-packages/selenium-2.47.1-py3.6.egg", prefix="selenium")
teams_tree = Tree("teams/", prefix="teams")
lib_tree = Tree("lib/", prefix="lib")
coll = COLLECT(exe,
               a.binaries,
               dict_tree,
               static_tree,
               template_tree,
               selenium_tree,
               lib_tree,
               teams_tree,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='showdownai')
