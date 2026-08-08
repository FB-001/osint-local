from pathlib import Path

from osint_local.collectors.image.metadata import analyze_image


image_path = Path("examples/images/202608056.jpg")

metadata = analyze_image(image_path)

print("=" * 60)
print("ANÁLISE DE IMAGEM")
print("=" * 60)
print(f"Arquivo: {metadata.file_path.name}")
print(f"Modelo do aparelho: {metadata.device_model or 'não informado'}")

if metadata.captured_at:
    print(f"Capturada em: {metadata.captured_at:%d/%m/%Y %H:%M:%S}")
else:
    print("Capturada em: não informado")

if metadata.latitude is not None and metadata.longitude is not None:
    print(f"Latitude: {metadata.latitude:.6f}")
    print(f"Longitude: {metadata.longitude:.6f}")
else:
    print("Localização GPS: não informada")

print(f"Dimensões: {metadata.width} x {metadata.height}")
print(f"Tamanho: {metadata.file_size_bytes} bytes")
print(f"SHA-256: {metadata.sha256}")
