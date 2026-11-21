import zlib, struct
from pathlib import Path

def write_png(filename, width, height, pixels):
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)
        for x in range(width):
            r, g, b = pixels(x, y, width, height)
            raw_data.extend((r, g, b))
    
    def chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)

    png_bytes = b'\x89PNG\r\n\x1a\n'
    png_bytes += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png_bytes += chunk(b'IDAT', zlib.compress(bytes(raw_data), level=9))
    png_bytes += chunk(b'IEND', b'')
    
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(png_bytes)

def news_art(x, y, w, h):
    ny = y / h
    nx = x / w
    # Header bar
    if ny < 0.12:
        return (18, 26, 42)
    # Infographic circular globe motif
    dx = nx - 0.5
    dy = ny - 0.55
    dist = (dx*dx + dy*dy)**0.5
    if dist < 0.35:
        # Latitude bands
        lat = int((ny * 30)) % 2
        return (40 + lat*15, 85 + lat*20, 140 + lat*30)
    # Outer dark neutral
    r = int(245 - 20 * ny)
    g = int(247 - 18 * ny)
    b = int(250 - 15 * ny)
    return (r, g, b)

write_png('/output/entry.png', 1024, 1024, news_art)
print('News 20 infographic generated.')
