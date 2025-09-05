# check_static.py
import os
import django
from django.conf import settings
from django.contrib.staticfiles import finders

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

# Archivo a buscar
path_to_check = 'customerrors/css/styles.css'

# Buscar en los staticfiles
absolute_path = finders.find(path_to_check)

print(f"Buscando: {path_to_check}")
if absolute_path:
    print(f"✅ Encontrado en: {absolute_path}")
else:
    print("❌ No encontrado. Django devolverá 404 y el navegador verá HTML en vez de CSS.")

# Mostrar todas las ubicaciones donde Django busca estáticos
print("\n📂 Directorios de búsqueda de estáticos:")
for finder in finders.get_finders():
    for path, storage in finder.list([]):
        if path.endswith('styles.css'):
            print(f"- {path} → {storage.location}")
