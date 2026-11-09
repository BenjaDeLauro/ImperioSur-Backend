from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.http import require_safe


TIPOS_IMAGEN = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.avif': 'image/avif',
}


@require_safe
def foto_producto(request, nombre):
    """Expone únicamente las fotos del catálogo de la instancia de demostración."""
    tipo = TIPOS_IMAGEN.get(Path(nombre).suffix.lower())
    if not tipo or Path(nombre).name != nombre:
        raise Http404
    directorio = (settings.MEDIA_ROOT / 'productos').resolve()
    archivo = (directorio / nombre).resolve()
    if archivo.parent != directorio:
        raise Http404
    try:
        return FileResponse(archivo.open('rb'), content_type=tipo)
    except (FileNotFoundError, IsADirectoryError):
        raise Http404 from None
