from ursina import *

# 1. Faylın adı (File Name): cat_adventure.py
# 2. Bu hissə pişik üçün şəhər obyektləridir

app = Ursina()

# Şəhər küçəsi
street = Entity(model='cube', color=color.dark_gray, scale=(20, 0.1, 100), z=40)

# Dırmaşmalı binalar
building1 = Entity(model='cube', color=color.orange, scale=(5, 30, 5), x=-8, y=15, collider='box')
building2 = Entity(model='cube', color=color.cyan, scale=(5, 50, 5), x=8, y=25, collider='box')

# Sənin seçdiyin rəngdə Pişik (Sadə model)
cat = Entity(model='sphere', color=color.gray, scale=1, y=1, collider='box')

app.run()
