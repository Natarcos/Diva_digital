#!/bin/bash
# Script para copiar imágenes al repositorio GitHub

echo "🚀 COPIANDO IMÁGENES AL REPOSITORIO GITHUB"
echo "=========================================="

# Directorio de origen (donde están tus imágenes actuales)
ORIGEN="/Users/n.arcos89/Desktop/Bootcamp_Data/DIVA_DIGITAL_Proyecto Final/imagenes_descargadas"

# Directorio de destino en GitHub
DESTINO="/Users/n.arcos89/Documents/GitHub/Diva_digital/imagenes"

# Verificar si el directorio origen existe
if [ ! -d "$ORIGEN" ]; then
    echo "❌ Directorio origen no encontrado: $ORIGEN"
    echo "📝 Modifica la variable ORIGEN en este script con la ruta correcta"
    exit 1
fi

# Copiar cada imagen
total=0
copiadas=0

echo "📂 Copiando desde: $ORIGEN"
echo "📂 Hacia: $DESTINO"
echo ""


if [ -f "$ORIGEN/IMG_1.jpg" ]; then
    cp "$ORIGEN/IMG_1.jpg" "$DESTINO/IMG_1.jpg"
    echo "✅ IMG_1.jpg"
    ((copiadas++))
else
    echo "❌ IMG_1.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_10.jpg" ]; then
    cp "$ORIGEN/IMG_10.jpg" "$DESTINO/IMG_10.jpg"
    echo "✅ IMG_10.jpg"
    ((copiadas++))
else
    echo "❌ IMG_10.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_100.jpg" ]; then
    cp "$ORIGEN/IMG_100.jpg" "$DESTINO/IMG_100.jpg"
    echo "✅ IMG_100.jpg"
    ((copiadas++))
else
    echo "❌ IMG_100.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_101.jpg" ]; then
    cp "$ORIGEN/IMG_101.jpg" "$DESTINO/IMG_101.jpg"
    echo "✅ IMG_101.jpg"
    ((copiadas++))
else
    echo "❌ IMG_101.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_102.jpg" ]; then
    cp "$ORIGEN/IMG_102.jpg" "$DESTINO/IMG_102.jpg"
    echo "✅ IMG_102.jpg"
    ((copiadas++))
else
    echo "❌ IMG_102.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_103.jpg" ]; then
    cp "$ORIGEN/IMG_103.jpg" "$DESTINO/IMG_103.jpg"
    echo "✅ IMG_103.jpg"
    ((copiadas++))
else
    echo "❌ IMG_103.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_104.jpg" ]; then
    cp "$ORIGEN/IMG_104.jpg" "$DESTINO/IMG_104.jpg"
    echo "✅ IMG_104.jpg"
    ((copiadas++))
else
    echo "❌ IMG_104.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_105.jpg" ]; then
    cp "$ORIGEN/IMG_105.jpg" "$DESTINO/IMG_105.jpg"
    echo "✅ IMG_105.jpg"
    ((copiadas++))
else
    echo "❌ IMG_105.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_106.jpg" ]; then
    cp "$ORIGEN/IMG_106.jpg" "$DESTINO/IMG_106.jpg"
    echo "✅ IMG_106.jpg"
    ((copiadas++))
else
    echo "❌ IMG_106.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_107.jpg" ]; then
    cp "$ORIGEN/IMG_107.jpg" "$DESTINO/IMG_107.jpg"
    echo "✅ IMG_107.jpg"
    ((copiadas++))
else
    echo "❌ IMG_107.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_108.jpg" ]; then
    cp "$ORIGEN/IMG_108.jpg" "$DESTINO/IMG_108.jpg"
    echo "✅ IMG_108.jpg"
    ((copiadas++))
else
    echo "❌ IMG_108.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_109.jpg" ]; then
    cp "$ORIGEN/IMG_109.jpg" "$DESTINO/IMG_109.jpg"
    echo "✅ IMG_109.jpg"
    ((copiadas++))
else
    echo "❌ IMG_109.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_11.jpg" ]; then
    cp "$ORIGEN/IMG_11.jpg" "$DESTINO/IMG_11.jpg"
    echo "✅ IMG_11.jpg"
    ((copiadas++))
else
    echo "❌ IMG_11.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_110.jpg" ]; then
    cp "$ORIGEN/IMG_110.jpg" "$DESTINO/IMG_110.jpg"
    echo "✅ IMG_110.jpg"
    ((copiadas++))
else
    echo "❌ IMG_110.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_111.jpg" ]; then
    cp "$ORIGEN/IMG_111.jpg" "$DESTINO/IMG_111.jpg"
    echo "✅ IMG_111.jpg"
    ((copiadas++))
else
    echo "❌ IMG_111.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_112.jpg" ]; then
    cp "$ORIGEN/IMG_112.jpg" "$DESTINO/IMG_112.jpg"
    echo "✅ IMG_112.jpg"
    ((copiadas++))
else
    echo "❌ IMG_112.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_113.jpg" ]; then
    cp "$ORIGEN/IMG_113.jpg" "$DESTINO/IMG_113.jpg"
    echo "✅ IMG_113.jpg"
    ((copiadas++))
else
    echo "❌ IMG_113.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_114.jpg" ]; then
    cp "$ORIGEN/IMG_114.jpg" "$DESTINO/IMG_114.jpg"
    echo "✅ IMG_114.jpg"
    ((copiadas++))
else
    echo "❌ IMG_114.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_115.jpg" ]; then
    cp "$ORIGEN/IMG_115.jpg" "$DESTINO/IMG_115.jpg"
    echo "✅ IMG_115.jpg"
    ((copiadas++))
else
    echo "❌ IMG_115.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_116.jpg" ]; then
    cp "$ORIGEN/IMG_116.jpg" "$DESTINO/IMG_116.jpg"
    echo "✅ IMG_116.jpg"
    ((copiadas++))
else
    echo "❌ IMG_116.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_117.jpg" ]; then
    cp "$ORIGEN/IMG_117.jpg" "$DESTINO/IMG_117.jpg"
    echo "✅ IMG_117.jpg"
    ((copiadas++))
else
    echo "❌ IMG_117.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_118.jpg" ]; then
    cp "$ORIGEN/IMG_118.jpg" "$DESTINO/IMG_118.jpg"
    echo "✅ IMG_118.jpg"
    ((copiadas++))
else
    echo "❌ IMG_118.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_119.jpg" ]; then
    cp "$ORIGEN/IMG_119.jpg" "$DESTINO/IMG_119.jpg"
    echo "✅ IMG_119.jpg"
    ((copiadas++))
else
    echo "❌ IMG_119.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_12.jpg" ]; then
    cp "$ORIGEN/IMG_12.jpg" "$DESTINO/IMG_12.jpg"
    echo "✅ IMG_12.jpg"
    ((copiadas++))
else
    echo "❌ IMG_12.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_120.jpg" ]; then
    cp "$ORIGEN/IMG_120.jpg" "$DESTINO/IMG_120.jpg"
    echo "✅ IMG_120.jpg"
    ((copiadas++))
else
    echo "❌ IMG_120.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_121.jpg" ]; then
    cp "$ORIGEN/IMG_121.jpg" "$DESTINO/IMG_121.jpg"
    echo "✅ IMG_121.jpg"
    ((copiadas++))
else
    echo "❌ IMG_121.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_122.jpg" ]; then
    cp "$ORIGEN/IMG_122.jpg" "$DESTINO/IMG_122.jpg"
    echo "✅ IMG_122.jpg"
    ((copiadas++))
else
    echo "❌ IMG_122.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_123.jpg" ]; then
    cp "$ORIGEN/IMG_123.jpg" "$DESTINO/IMG_123.jpg"
    echo "✅ IMG_123.jpg"
    ((copiadas++))
else
    echo "❌ IMG_123.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_124.jpg" ]; then
    cp "$ORIGEN/IMG_124.jpg" "$DESTINO/IMG_124.jpg"
    echo "✅ IMG_124.jpg"
    ((copiadas++))
else
    echo "❌ IMG_124.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_125.jpg" ]; then
    cp "$ORIGEN/IMG_125.jpg" "$DESTINO/IMG_125.jpg"
    echo "✅ IMG_125.jpg"
    ((copiadas++))
else
    echo "❌ IMG_125.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_126.jpg" ]; then
    cp "$ORIGEN/IMG_126.jpg" "$DESTINO/IMG_126.jpg"
    echo "✅ IMG_126.jpg"
    ((copiadas++))
else
    echo "❌ IMG_126.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_127.jpg" ]; then
    cp "$ORIGEN/IMG_127.jpg" "$DESTINO/IMG_127.jpg"
    echo "✅ IMG_127.jpg"
    ((copiadas++))
else
    echo "❌ IMG_127.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_128.jpg" ]; then
    cp "$ORIGEN/IMG_128.jpg" "$DESTINO/IMG_128.jpg"
    echo "✅ IMG_128.jpg"
    ((copiadas++))
else
    echo "❌ IMG_128.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_129.jpg" ]; then
    cp "$ORIGEN/IMG_129.jpg" "$DESTINO/IMG_129.jpg"
    echo "✅ IMG_129.jpg"
    ((copiadas++))
else
    echo "❌ IMG_129.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_13.jpg" ]; then
    cp "$ORIGEN/IMG_13.jpg" "$DESTINO/IMG_13.jpg"
    echo "✅ IMG_13.jpg"
    ((copiadas++))
else
    echo "❌ IMG_13.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_130.jpg" ]; then
    cp "$ORIGEN/IMG_130.jpg" "$DESTINO/IMG_130.jpg"
    echo "✅ IMG_130.jpg"
    ((copiadas++))
else
    echo "❌ IMG_130.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_131.jpg" ]; then
    cp "$ORIGEN/IMG_131.jpg" "$DESTINO/IMG_131.jpg"
    echo "✅ IMG_131.jpg"
    ((copiadas++))
else
    echo "❌ IMG_131.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_132.jpg" ]; then
    cp "$ORIGEN/IMG_132.jpg" "$DESTINO/IMG_132.jpg"
    echo "✅ IMG_132.jpg"
    ((copiadas++))
else
    echo "❌ IMG_132.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_133.jpg" ]; then
    cp "$ORIGEN/IMG_133.jpg" "$DESTINO/IMG_133.jpg"
    echo "✅ IMG_133.jpg"
    ((copiadas++))
else
    echo "❌ IMG_133.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_134.jpg" ]; then
    cp "$ORIGEN/IMG_134.jpg" "$DESTINO/IMG_134.jpg"
    echo "✅ IMG_134.jpg"
    ((copiadas++))
else
    echo "❌ IMG_134.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_135.jpg" ]; then
    cp "$ORIGEN/IMG_135.jpg" "$DESTINO/IMG_135.jpg"
    echo "✅ IMG_135.jpg"
    ((copiadas++))
else
    echo "❌ IMG_135.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_136.jpg" ]; then
    cp "$ORIGEN/IMG_136.jpg" "$DESTINO/IMG_136.jpg"
    echo "✅ IMG_136.jpg"
    ((copiadas++))
else
    echo "❌ IMG_136.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_137.jpg" ]; then
    cp "$ORIGEN/IMG_137.jpg" "$DESTINO/IMG_137.jpg"
    echo "✅ IMG_137.jpg"
    ((copiadas++))
else
    echo "❌ IMG_137.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_138.jpg" ]; then
    cp "$ORIGEN/IMG_138.jpg" "$DESTINO/IMG_138.jpg"
    echo "✅ IMG_138.jpg"
    ((copiadas++))
else
    echo "❌ IMG_138.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_139.jpg" ]; then
    cp "$ORIGEN/IMG_139.jpg" "$DESTINO/IMG_139.jpg"
    echo "✅ IMG_139.jpg"
    ((copiadas++))
else
    echo "❌ IMG_139.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_14.jpg" ]; then
    cp "$ORIGEN/IMG_14.jpg" "$DESTINO/IMG_14.jpg"
    echo "✅ IMG_14.jpg"
    ((copiadas++))
else
    echo "❌ IMG_14.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_140.jpg" ]; then
    cp "$ORIGEN/IMG_140.jpg" "$DESTINO/IMG_140.jpg"
    echo "✅ IMG_140.jpg"
    ((copiadas++))
else
    echo "❌ IMG_140.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_141.jpg" ]; then
    cp "$ORIGEN/IMG_141.jpg" "$DESTINO/IMG_141.jpg"
    echo "✅ IMG_141.jpg"
    ((copiadas++))
else
    echo "❌ IMG_141.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_142.jpg" ]; then
    cp "$ORIGEN/IMG_142.jpg" "$DESTINO/IMG_142.jpg"
    echo "✅ IMG_142.jpg"
    ((copiadas++))
else
    echo "❌ IMG_142.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_143.jpg" ]; then
    cp "$ORIGEN/IMG_143.jpg" "$DESTINO/IMG_143.jpg"
    echo "✅ IMG_143.jpg"
    ((copiadas++))
else
    echo "❌ IMG_143.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_144.jpg" ]; then
    cp "$ORIGEN/IMG_144.jpg" "$DESTINO/IMG_144.jpg"
    echo "✅ IMG_144.jpg"
    ((copiadas++))
else
    echo "❌ IMG_144.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_145.jpg" ]; then
    cp "$ORIGEN/IMG_145.jpg" "$DESTINO/IMG_145.jpg"
    echo "✅ IMG_145.jpg"
    ((copiadas++))
else
    echo "❌ IMG_145.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_146.jpg" ]; then
    cp "$ORIGEN/IMG_146.jpg" "$DESTINO/IMG_146.jpg"
    echo "✅ IMG_146.jpg"
    ((copiadas++))
else
    echo "❌ IMG_146.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_147.jpg" ]; then
    cp "$ORIGEN/IMG_147.jpg" "$DESTINO/IMG_147.jpg"
    echo "✅ IMG_147.jpg"
    ((copiadas++))
else
    echo "❌ IMG_147.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_148.jpg" ]; then
    cp "$ORIGEN/IMG_148.jpg" "$DESTINO/IMG_148.jpg"
    echo "✅ IMG_148.jpg"
    ((copiadas++))
else
    echo "❌ IMG_148.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_149.jpg" ]; then
    cp "$ORIGEN/IMG_149.jpg" "$DESTINO/IMG_149.jpg"
    echo "✅ IMG_149.jpg"
    ((copiadas++))
else
    echo "❌ IMG_149.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_15.jpg" ]; then
    cp "$ORIGEN/IMG_15.jpg" "$DESTINO/IMG_15.jpg"
    echo "✅ IMG_15.jpg"
    ((copiadas++))
else
    echo "❌ IMG_15.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_150.jpg" ]; then
    cp "$ORIGEN/IMG_150.jpg" "$DESTINO/IMG_150.jpg"
    echo "✅ IMG_150.jpg"
    ((copiadas++))
else
    echo "❌ IMG_150.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_151.jpg" ]; then
    cp "$ORIGEN/IMG_151.jpg" "$DESTINO/IMG_151.jpg"
    echo "✅ IMG_151.jpg"
    ((copiadas++))
else
    echo "❌ IMG_151.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_152.jpg" ]; then
    cp "$ORIGEN/IMG_152.jpg" "$DESTINO/IMG_152.jpg"
    echo "✅ IMG_152.jpg"
    ((copiadas++))
else
    echo "❌ IMG_152.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_153.jpg" ]; then
    cp "$ORIGEN/IMG_153.jpg" "$DESTINO/IMG_153.jpg"
    echo "✅ IMG_153.jpg"
    ((copiadas++))
else
    echo "❌ IMG_153.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_154.jpg" ]; then
    cp "$ORIGEN/IMG_154.jpg" "$DESTINO/IMG_154.jpg"
    echo "✅ IMG_154.jpg"
    ((copiadas++))
else
    echo "❌ IMG_154.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_155.jpg" ]; then
    cp "$ORIGEN/IMG_155.jpg" "$DESTINO/IMG_155.jpg"
    echo "✅ IMG_155.jpg"
    ((copiadas++))
else
    echo "❌ IMG_155.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_156.jpg" ]; then
    cp "$ORIGEN/IMG_156.jpg" "$DESTINO/IMG_156.jpg"
    echo "✅ IMG_156.jpg"
    ((copiadas++))
else
    echo "❌ IMG_156.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_157.jpg" ]; then
    cp "$ORIGEN/IMG_157.jpg" "$DESTINO/IMG_157.jpg"
    echo "✅ IMG_157.jpg"
    ((copiadas++))
else
    echo "❌ IMG_157.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_158.jpg" ]; then
    cp "$ORIGEN/IMG_158.jpg" "$DESTINO/IMG_158.jpg"
    echo "✅ IMG_158.jpg"
    ((copiadas++))
else
    echo "❌ IMG_158.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_159.jpg" ]; then
    cp "$ORIGEN/IMG_159.jpg" "$DESTINO/IMG_159.jpg"
    echo "✅ IMG_159.jpg"
    ((copiadas++))
else
    echo "❌ IMG_159.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_16.jpg" ]; then
    cp "$ORIGEN/IMG_16.jpg" "$DESTINO/IMG_16.jpg"
    echo "✅ IMG_16.jpg"
    ((copiadas++))
else
    echo "❌ IMG_16.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_160.jpg" ]; then
    cp "$ORIGEN/IMG_160.jpg" "$DESTINO/IMG_160.jpg"
    echo "✅ IMG_160.jpg"
    ((copiadas++))
else
    echo "❌ IMG_160.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_161.jpg" ]; then
    cp "$ORIGEN/IMG_161.jpg" "$DESTINO/IMG_161.jpg"
    echo "✅ IMG_161.jpg"
    ((copiadas++))
else
    echo "❌ IMG_161.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_162.jpg" ]; then
    cp "$ORIGEN/IMG_162.jpg" "$DESTINO/IMG_162.jpg"
    echo "✅ IMG_162.jpg"
    ((copiadas++))
else
    echo "❌ IMG_162.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_163.jpg" ]; then
    cp "$ORIGEN/IMG_163.jpg" "$DESTINO/IMG_163.jpg"
    echo "✅ IMG_163.jpg"
    ((copiadas++))
else
    echo "❌ IMG_163.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_164.jpg" ]; then
    cp "$ORIGEN/IMG_164.jpg" "$DESTINO/IMG_164.jpg"
    echo "✅ IMG_164.jpg"
    ((copiadas++))
else
    echo "❌ IMG_164.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_165.jpg" ]; then
    cp "$ORIGEN/IMG_165.jpg" "$DESTINO/IMG_165.jpg"
    echo "✅ IMG_165.jpg"
    ((copiadas++))
else
    echo "❌ IMG_165.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_166.jpg" ]; then
    cp "$ORIGEN/IMG_166.jpg" "$DESTINO/IMG_166.jpg"
    echo "✅ IMG_166.jpg"
    ((copiadas++))
else
    echo "❌ IMG_166.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_167.jpg" ]; then
    cp "$ORIGEN/IMG_167.jpg" "$DESTINO/IMG_167.jpg"
    echo "✅ IMG_167.jpg"
    ((copiadas++))
else
    echo "❌ IMG_167.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_168.jpg" ]; then
    cp "$ORIGEN/IMG_168.jpg" "$DESTINO/IMG_168.jpg"
    echo "✅ IMG_168.jpg"
    ((copiadas++))
else
    echo "❌ IMG_168.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_169.jpg" ]; then
    cp "$ORIGEN/IMG_169.jpg" "$DESTINO/IMG_169.jpg"
    echo "✅ IMG_169.jpg"
    ((copiadas++))
else
    echo "❌ IMG_169.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_17.jpg" ]; then
    cp "$ORIGEN/IMG_17.jpg" "$DESTINO/IMG_17.jpg"
    echo "✅ IMG_17.jpg"
    ((copiadas++))
else
    echo "❌ IMG_17.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_170.jpg" ]; then
    cp "$ORIGEN/IMG_170.jpg" "$DESTINO/IMG_170.jpg"
    echo "✅ IMG_170.jpg"
    ((copiadas++))
else
    echo "❌ IMG_170.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_171.jpg" ]; then
    cp "$ORIGEN/IMG_171.jpg" "$DESTINO/IMG_171.jpg"
    echo "✅ IMG_171.jpg"
    ((copiadas++))
else
    echo "❌ IMG_171.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_172.jpg" ]; then
    cp "$ORIGEN/IMG_172.jpg" "$DESTINO/IMG_172.jpg"
    echo "✅ IMG_172.jpg"
    ((copiadas++))
else
    echo "❌ IMG_172.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_173.jpg" ]; then
    cp "$ORIGEN/IMG_173.jpg" "$DESTINO/IMG_173.jpg"
    echo "✅ IMG_173.jpg"
    ((copiadas++))
else
    echo "❌ IMG_173.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_174.jpg" ]; then
    cp "$ORIGEN/IMG_174.jpg" "$DESTINO/IMG_174.jpg"
    echo "✅ IMG_174.jpg"
    ((copiadas++))
else
    echo "❌ IMG_174.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_175.jpg" ]; then
    cp "$ORIGEN/IMG_175.jpg" "$DESTINO/IMG_175.jpg"
    echo "✅ IMG_175.jpg"
    ((copiadas++))
else
    echo "❌ IMG_175.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_176.jpg" ]; then
    cp "$ORIGEN/IMG_176.jpg" "$DESTINO/IMG_176.jpg"
    echo "✅ IMG_176.jpg"
    ((copiadas++))
else
    echo "❌ IMG_176.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_177.jpg" ]; then
    cp "$ORIGEN/IMG_177.jpg" "$DESTINO/IMG_177.jpg"
    echo "✅ IMG_177.jpg"
    ((copiadas++))
else
    echo "❌ IMG_177.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_178.jpg" ]; then
    cp "$ORIGEN/IMG_178.jpg" "$DESTINO/IMG_178.jpg"
    echo "✅ IMG_178.jpg"
    ((copiadas++))
else
    echo "❌ IMG_178.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_179.jpg" ]; then
    cp "$ORIGEN/IMG_179.jpg" "$DESTINO/IMG_179.jpg"
    echo "✅ IMG_179.jpg"
    ((copiadas++))
else
    echo "❌ IMG_179.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_18.jpg" ]; then
    cp "$ORIGEN/IMG_18.jpg" "$DESTINO/IMG_18.jpg"
    echo "✅ IMG_18.jpg"
    ((copiadas++))
else
    echo "❌ IMG_18.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_180.jpg" ]; then
    cp "$ORIGEN/IMG_180.jpg" "$DESTINO/IMG_180.jpg"
    echo "✅ IMG_180.jpg"
    ((copiadas++))
else
    echo "❌ IMG_180.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_181.jpg" ]; then
    cp "$ORIGEN/IMG_181.jpg" "$DESTINO/IMG_181.jpg"
    echo "✅ IMG_181.jpg"
    ((copiadas++))
else
    echo "❌ IMG_181.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_182.jpg" ]; then
    cp "$ORIGEN/IMG_182.jpg" "$DESTINO/IMG_182.jpg"
    echo "✅ IMG_182.jpg"
    ((copiadas++))
else
    echo "❌ IMG_182.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_183.jpg" ]; then
    cp "$ORIGEN/IMG_183.jpg" "$DESTINO/IMG_183.jpg"
    echo "✅ IMG_183.jpg"
    ((copiadas++))
else
    echo "❌ IMG_183.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_184.jpg" ]; then
    cp "$ORIGEN/IMG_184.jpg" "$DESTINO/IMG_184.jpg"
    echo "✅ IMG_184.jpg"
    ((copiadas++))
else
    echo "❌ IMG_184.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_185.jpg" ]; then
    cp "$ORIGEN/IMG_185.jpg" "$DESTINO/IMG_185.jpg"
    echo "✅ IMG_185.jpg"
    ((copiadas++))
else
    echo "❌ IMG_185.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_186.jpg" ]; then
    cp "$ORIGEN/IMG_186.jpg" "$DESTINO/IMG_186.jpg"
    echo "✅ IMG_186.jpg"
    ((copiadas++))
else
    echo "❌ IMG_186.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_187.jpg" ]; then
    cp "$ORIGEN/IMG_187.jpg" "$DESTINO/IMG_187.jpg"
    echo "✅ IMG_187.jpg"
    ((copiadas++))
else
    echo "❌ IMG_187.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_188.jpg" ]; then
    cp "$ORIGEN/IMG_188.jpg" "$DESTINO/IMG_188.jpg"
    echo "✅ IMG_188.jpg"
    ((copiadas++))
else
    echo "❌ IMG_188.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_189.jpg" ]; then
    cp "$ORIGEN/IMG_189.jpg" "$DESTINO/IMG_189.jpg"
    echo "✅ IMG_189.jpg"
    ((copiadas++))
else
    echo "❌ IMG_189.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_19.jpg" ]; then
    cp "$ORIGEN/IMG_19.jpg" "$DESTINO/IMG_19.jpg"
    echo "✅ IMG_19.jpg"
    ((copiadas++))
else
    echo "❌ IMG_19.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_190.jpg" ]; then
    cp "$ORIGEN/IMG_190.jpg" "$DESTINO/IMG_190.jpg"
    echo "✅ IMG_190.jpg"
    ((copiadas++))
else
    echo "❌ IMG_190.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_191.jpg" ]; then
    cp "$ORIGEN/IMG_191.jpg" "$DESTINO/IMG_191.jpg"
    echo "✅ IMG_191.jpg"
    ((copiadas++))
else
    echo "❌ IMG_191.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_192.jpg" ]; then
    cp "$ORIGEN/IMG_192.jpg" "$DESTINO/IMG_192.jpg"
    echo "✅ IMG_192.jpg"
    ((copiadas++))
else
    echo "❌ IMG_192.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_193.jpg" ]; then
    cp "$ORIGEN/IMG_193.jpg" "$DESTINO/IMG_193.jpg"
    echo "✅ IMG_193.jpg"
    ((copiadas++))
else
    echo "❌ IMG_193.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_194.jpg" ]; then
    cp "$ORIGEN/IMG_194.jpg" "$DESTINO/IMG_194.jpg"
    echo "✅ IMG_194.jpg"
    ((copiadas++))
else
    echo "❌ IMG_194.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_195.jpg" ]; then
    cp "$ORIGEN/IMG_195.jpg" "$DESTINO/IMG_195.jpg"
    echo "✅ IMG_195.jpg"
    ((copiadas++))
else
    echo "❌ IMG_195.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_196.jpg" ]; then
    cp "$ORIGEN/IMG_196.jpg" "$DESTINO/IMG_196.jpg"
    echo "✅ IMG_196.jpg"
    ((copiadas++))
else
    echo "❌ IMG_196.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_197.jpg" ]; then
    cp "$ORIGEN/IMG_197.jpg" "$DESTINO/IMG_197.jpg"
    echo "✅ IMG_197.jpg"
    ((copiadas++))
else
    echo "❌ IMG_197.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_198.jpg" ]; then
    cp "$ORIGEN/IMG_198.jpg" "$DESTINO/IMG_198.jpg"
    echo "✅ IMG_198.jpg"
    ((copiadas++))
else
    echo "❌ IMG_198.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_199.jpg" ]; then
    cp "$ORIGEN/IMG_199.jpg" "$DESTINO/IMG_199.jpg"
    echo "✅ IMG_199.jpg"
    ((copiadas++))
else
    echo "❌ IMG_199.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_2.jpg" ]; then
    cp "$ORIGEN/IMG_2.jpg" "$DESTINO/IMG_2.jpg"
    echo "✅ IMG_2.jpg"
    ((copiadas++))
else
    echo "❌ IMG_2.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_20.jpg" ]; then
    cp "$ORIGEN/IMG_20.jpg" "$DESTINO/IMG_20.jpg"
    echo "✅ IMG_20.jpg"
    ((copiadas++))
else
    echo "❌ IMG_20.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_200.jpg" ]; then
    cp "$ORIGEN/IMG_200.jpg" "$DESTINO/IMG_200.jpg"
    echo "✅ IMG_200.jpg"
    ((copiadas++))
else
    echo "❌ IMG_200.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_21.jpg" ]; then
    cp "$ORIGEN/IMG_21.jpg" "$DESTINO/IMG_21.jpg"
    echo "✅ IMG_21.jpg"
    ((copiadas++))
else
    echo "❌ IMG_21.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_22.jpg" ]; then
    cp "$ORIGEN/IMG_22.jpg" "$DESTINO/IMG_22.jpg"
    echo "✅ IMG_22.jpg"
    ((copiadas++))
else
    echo "❌ IMG_22.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_23.jpg" ]; then
    cp "$ORIGEN/IMG_23.jpg" "$DESTINO/IMG_23.jpg"
    echo "✅ IMG_23.jpg"
    ((copiadas++))
else
    echo "❌ IMG_23.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_24.jpg" ]; then
    cp "$ORIGEN/IMG_24.jpg" "$DESTINO/IMG_24.jpg"
    echo "✅ IMG_24.jpg"
    ((copiadas++))
else
    echo "❌ IMG_24.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_25.jpg" ]; then
    cp "$ORIGEN/IMG_25.jpg" "$DESTINO/IMG_25.jpg"
    echo "✅ IMG_25.jpg"
    ((copiadas++))
else
    echo "❌ IMG_25.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_26.jpg" ]; then
    cp "$ORIGEN/IMG_26.jpg" "$DESTINO/IMG_26.jpg"
    echo "✅ IMG_26.jpg"
    ((copiadas++))
else
    echo "❌ IMG_26.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_27.jpg" ]; then
    cp "$ORIGEN/IMG_27.jpg" "$DESTINO/IMG_27.jpg"
    echo "✅ IMG_27.jpg"
    ((copiadas++))
else
    echo "❌ IMG_27.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_28.jpg" ]; then
    cp "$ORIGEN/IMG_28.jpg" "$DESTINO/IMG_28.jpg"
    echo "✅ IMG_28.jpg"
    ((copiadas++))
else
    echo "❌ IMG_28.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_29.jpg" ]; then
    cp "$ORIGEN/IMG_29.jpg" "$DESTINO/IMG_29.jpg"
    echo "✅ IMG_29.jpg"
    ((copiadas++))
else
    echo "❌ IMG_29.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_3.jpg" ]; then
    cp "$ORIGEN/IMG_3.jpg" "$DESTINO/IMG_3.jpg"
    echo "✅ IMG_3.jpg"
    ((copiadas++))
else
    echo "❌ IMG_3.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_30.jpg" ]; then
    cp "$ORIGEN/IMG_30.jpg" "$DESTINO/IMG_30.jpg"
    echo "✅ IMG_30.jpg"
    ((copiadas++))
else
    echo "❌ IMG_30.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_31.jpg" ]; then
    cp "$ORIGEN/IMG_31.jpg" "$DESTINO/IMG_31.jpg"
    echo "✅ IMG_31.jpg"
    ((copiadas++))
else
    echo "❌ IMG_31.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_32.jpg" ]; then
    cp "$ORIGEN/IMG_32.jpg" "$DESTINO/IMG_32.jpg"
    echo "✅ IMG_32.jpg"
    ((copiadas++))
else
    echo "❌ IMG_32.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_33.jpg" ]; then
    cp "$ORIGEN/IMG_33.jpg" "$DESTINO/IMG_33.jpg"
    echo "✅ IMG_33.jpg"
    ((copiadas++))
else
    echo "❌ IMG_33.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_34.jpg" ]; then
    cp "$ORIGEN/IMG_34.jpg" "$DESTINO/IMG_34.jpg"
    echo "✅ IMG_34.jpg"
    ((copiadas++))
else
    echo "❌ IMG_34.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_35.jpg" ]; then
    cp "$ORIGEN/IMG_35.jpg" "$DESTINO/IMG_35.jpg"
    echo "✅ IMG_35.jpg"
    ((copiadas++))
else
    echo "❌ IMG_35.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_36.jpg" ]; then
    cp "$ORIGEN/IMG_36.jpg" "$DESTINO/IMG_36.jpg"
    echo "✅ IMG_36.jpg"
    ((copiadas++))
else
    echo "❌ IMG_36.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_37.jpg" ]; then
    cp "$ORIGEN/IMG_37.jpg" "$DESTINO/IMG_37.jpg"
    echo "✅ IMG_37.jpg"
    ((copiadas++))
else
    echo "❌ IMG_37.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_38.jpg" ]; then
    cp "$ORIGEN/IMG_38.jpg" "$DESTINO/IMG_38.jpg"
    echo "✅ IMG_38.jpg"
    ((copiadas++))
else
    echo "❌ IMG_38.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_39.jpg" ]; then
    cp "$ORIGEN/IMG_39.jpg" "$DESTINO/IMG_39.jpg"
    echo "✅ IMG_39.jpg"
    ((copiadas++))
else
    echo "❌ IMG_39.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_4.jpg" ]; then
    cp "$ORIGEN/IMG_4.jpg" "$DESTINO/IMG_4.jpg"
    echo "✅ IMG_4.jpg"
    ((copiadas++))
else
    echo "❌ IMG_4.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_40.jpg" ]; then
    cp "$ORIGEN/IMG_40.jpg" "$DESTINO/IMG_40.jpg"
    echo "✅ IMG_40.jpg"
    ((copiadas++))
else
    echo "❌ IMG_40.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_41.jpg" ]; then
    cp "$ORIGEN/IMG_41.jpg" "$DESTINO/IMG_41.jpg"
    echo "✅ IMG_41.jpg"
    ((copiadas++))
else
    echo "❌ IMG_41.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_42.jpg" ]; then
    cp "$ORIGEN/IMG_42.jpg" "$DESTINO/IMG_42.jpg"
    echo "✅ IMG_42.jpg"
    ((copiadas++))
else
    echo "❌ IMG_42.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_43.jpg" ]; then
    cp "$ORIGEN/IMG_43.jpg" "$DESTINO/IMG_43.jpg"
    echo "✅ IMG_43.jpg"
    ((copiadas++))
else
    echo "❌ IMG_43.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_44.jpg" ]; then
    cp "$ORIGEN/IMG_44.jpg" "$DESTINO/IMG_44.jpg"
    echo "✅ IMG_44.jpg"
    ((copiadas++))
else
    echo "❌ IMG_44.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_45.jpg" ]; then
    cp "$ORIGEN/IMG_45.jpg" "$DESTINO/IMG_45.jpg"
    echo "✅ IMG_45.jpg"
    ((copiadas++))
else
    echo "❌ IMG_45.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_46.jpg" ]; then
    cp "$ORIGEN/IMG_46.jpg" "$DESTINO/IMG_46.jpg"
    echo "✅ IMG_46.jpg"
    ((copiadas++))
else
    echo "❌ IMG_46.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_47.jpg" ]; then
    cp "$ORIGEN/IMG_47.jpg" "$DESTINO/IMG_47.jpg"
    echo "✅ IMG_47.jpg"
    ((copiadas++))
else
    echo "❌ IMG_47.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_48.jpg" ]; then
    cp "$ORIGEN/IMG_48.jpg" "$DESTINO/IMG_48.jpg"
    echo "✅ IMG_48.jpg"
    ((copiadas++))
else
    echo "❌ IMG_48.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_49.jpg" ]; then
    cp "$ORIGEN/IMG_49.jpg" "$DESTINO/IMG_49.jpg"
    echo "✅ IMG_49.jpg"
    ((copiadas++))
else
    echo "❌ IMG_49.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_5.jpg" ]; then
    cp "$ORIGEN/IMG_5.jpg" "$DESTINO/IMG_5.jpg"
    echo "✅ IMG_5.jpg"
    ((copiadas++))
else
    echo "❌ IMG_5.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_50.jpg" ]; then
    cp "$ORIGEN/IMG_50.jpg" "$DESTINO/IMG_50.jpg"
    echo "✅ IMG_50.jpg"
    ((copiadas++))
else
    echo "❌ IMG_50.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_51.jpg" ]; then
    cp "$ORIGEN/IMG_51.jpg" "$DESTINO/IMG_51.jpg"
    echo "✅ IMG_51.jpg"
    ((copiadas++))
else
    echo "❌ IMG_51.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_52.jpg" ]; then
    cp "$ORIGEN/IMG_52.jpg" "$DESTINO/IMG_52.jpg"
    echo "✅ IMG_52.jpg"
    ((copiadas++))
else
    echo "❌ IMG_52.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_53.jpg" ]; then
    cp "$ORIGEN/IMG_53.jpg" "$DESTINO/IMG_53.jpg"
    echo "✅ IMG_53.jpg"
    ((copiadas++))
else
    echo "❌ IMG_53.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_54.jpg" ]; then
    cp "$ORIGEN/IMG_54.jpg" "$DESTINO/IMG_54.jpg"
    echo "✅ IMG_54.jpg"
    ((copiadas++))
else
    echo "❌ IMG_54.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_55.jpg" ]; then
    cp "$ORIGEN/IMG_55.jpg" "$DESTINO/IMG_55.jpg"
    echo "✅ IMG_55.jpg"
    ((copiadas++))
else
    echo "❌ IMG_55.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_56.jpg" ]; then
    cp "$ORIGEN/IMG_56.jpg" "$DESTINO/IMG_56.jpg"
    echo "✅ IMG_56.jpg"
    ((copiadas++))
else
    echo "❌ IMG_56.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_57.jpg" ]; then
    cp "$ORIGEN/IMG_57.jpg" "$DESTINO/IMG_57.jpg"
    echo "✅ IMG_57.jpg"
    ((copiadas++))
else
    echo "❌ IMG_57.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_58.jpg" ]; then
    cp "$ORIGEN/IMG_58.jpg" "$DESTINO/IMG_58.jpg"
    echo "✅ IMG_58.jpg"
    ((copiadas++))
else
    echo "❌ IMG_58.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_59.jpg" ]; then
    cp "$ORIGEN/IMG_59.jpg" "$DESTINO/IMG_59.jpg"
    echo "✅ IMG_59.jpg"
    ((copiadas++))
else
    echo "❌ IMG_59.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_6.jpg" ]; then
    cp "$ORIGEN/IMG_6.jpg" "$DESTINO/IMG_6.jpg"
    echo "✅ IMG_6.jpg"
    ((copiadas++))
else
    echo "❌ IMG_6.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_60.jpg" ]; then
    cp "$ORIGEN/IMG_60.jpg" "$DESTINO/IMG_60.jpg"
    echo "✅ IMG_60.jpg"
    ((copiadas++))
else
    echo "❌ IMG_60.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_61.jpg" ]; then
    cp "$ORIGEN/IMG_61.jpg" "$DESTINO/IMG_61.jpg"
    echo "✅ IMG_61.jpg"
    ((copiadas++))
else
    echo "❌ IMG_61.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_62.jpg" ]; then
    cp "$ORIGEN/IMG_62.jpg" "$DESTINO/IMG_62.jpg"
    echo "✅ IMG_62.jpg"
    ((copiadas++))
else
    echo "❌ IMG_62.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_63.jpg" ]; then
    cp "$ORIGEN/IMG_63.jpg" "$DESTINO/IMG_63.jpg"
    echo "✅ IMG_63.jpg"
    ((copiadas++))
else
    echo "❌ IMG_63.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_64.jpg" ]; then
    cp "$ORIGEN/IMG_64.jpg" "$DESTINO/IMG_64.jpg"
    echo "✅ IMG_64.jpg"
    ((copiadas++))
else
    echo "❌ IMG_64.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_65.jpg" ]; then
    cp "$ORIGEN/IMG_65.jpg" "$DESTINO/IMG_65.jpg"
    echo "✅ IMG_65.jpg"
    ((copiadas++))
else
    echo "❌ IMG_65.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_66.jpg" ]; then
    cp "$ORIGEN/IMG_66.jpg" "$DESTINO/IMG_66.jpg"
    echo "✅ IMG_66.jpg"
    ((copiadas++))
else
    echo "❌ IMG_66.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_67.jpg" ]; then
    cp "$ORIGEN/IMG_67.jpg" "$DESTINO/IMG_67.jpg"
    echo "✅ IMG_67.jpg"
    ((copiadas++))
else
    echo "❌ IMG_67.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_68.jpg" ]; then
    cp "$ORIGEN/IMG_68.jpg" "$DESTINO/IMG_68.jpg"
    echo "✅ IMG_68.jpg"
    ((copiadas++))
else
    echo "❌ IMG_68.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_69.jpg" ]; then
    cp "$ORIGEN/IMG_69.jpg" "$DESTINO/IMG_69.jpg"
    echo "✅ IMG_69.jpg"
    ((copiadas++))
else
    echo "❌ IMG_69.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_7.jpg" ]; then
    cp "$ORIGEN/IMG_7.jpg" "$DESTINO/IMG_7.jpg"
    echo "✅ IMG_7.jpg"
    ((copiadas++))
else
    echo "❌ IMG_7.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_70.jpg" ]; then
    cp "$ORIGEN/IMG_70.jpg" "$DESTINO/IMG_70.jpg"
    echo "✅ IMG_70.jpg"
    ((copiadas++))
else
    echo "❌ IMG_70.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_71.jpg" ]; then
    cp "$ORIGEN/IMG_71.jpg" "$DESTINO/IMG_71.jpg"
    echo "✅ IMG_71.jpg"
    ((copiadas++))
else
    echo "❌ IMG_71.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_72.jpg" ]; then
    cp "$ORIGEN/IMG_72.jpg" "$DESTINO/IMG_72.jpg"
    echo "✅ IMG_72.jpg"
    ((copiadas++))
else
    echo "❌ IMG_72.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_73.jpg" ]; then
    cp "$ORIGEN/IMG_73.jpg" "$DESTINO/IMG_73.jpg"
    echo "✅ IMG_73.jpg"
    ((copiadas++))
else
    echo "❌ IMG_73.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_74.jpg" ]; then
    cp "$ORIGEN/IMG_74.jpg" "$DESTINO/IMG_74.jpg"
    echo "✅ IMG_74.jpg"
    ((copiadas++))
else
    echo "❌ IMG_74.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_75.jpg" ]; then
    cp "$ORIGEN/IMG_75.jpg" "$DESTINO/IMG_75.jpg"
    echo "✅ IMG_75.jpg"
    ((copiadas++))
else
    echo "❌ IMG_75.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_76.jpg" ]; then
    cp "$ORIGEN/IMG_76.jpg" "$DESTINO/IMG_76.jpg"
    echo "✅ IMG_76.jpg"
    ((copiadas++))
else
    echo "❌ IMG_76.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_77.jpg" ]; then
    cp "$ORIGEN/IMG_77.jpg" "$DESTINO/IMG_77.jpg"
    echo "✅ IMG_77.jpg"
    ((copiadas++))
else
    echo "❌ IMG_77.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_78.jpg" ]; then
    cp "$ORIGEN/IMG_78.jpg" "$DESTINO/IMG_78.jpg"
    echo "✅ IMG_78.jpg"
    ((copiadas++))
else
    echo "❌ IMG_78.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_79.jpg" ]; then
    cp "$ORIGEN/IMG_79.jpg" "$DESTINO/IMG_79.jpg"
    echo "✅ IMG_79.jpg"
    ((copiadas++))
else
    echo "❌ IMG_79.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_8.jpg" ]; then
    cp "$ORIGEN/IMG_8.jpg" "$DESTINO/IMG_8.jpg"
    echo "✅ IMG_8.jpg"
    ((copiadas++))
else
    echo "❌ IMG_8.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_80.jpg" ]; then
    cp "$ORIGEN/IMG_80.jpg" "$DESTINO/IMG_80.jpg"
    echo "✅ IMG_80.jpg"
    ((copiadas++))
else
    echo "❌ IMG_80.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_81.jpg" ]; then
    cp "$ORIGEN/IMG_81.jpg" "$DESTINO/IMG_81.jpg"
    echo "✅ IMG_81.jpg"
    ((copiadas++))
else
    echo "❌ IMG_81.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_82.jpg" ]; then
    cp "$ORIGEN/IMG_82.jpg" "$DESTINO/IMG_82.jpg"
    echo "✅ IMG_82.jpg"
    ((copiadas++))
else
    echo "❌ IMG_82.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_83.jpg" ]; then
    cp "$ORIGEN/IMG_83.jpg" "$DESTINO/IMG_83.jpg"
    echo "✅ IMG_83.jpg"
    ((copiadas++))
else
    echo "❌ IMG_83.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_84.jpg" ]; then
    cp "$ORIGEN/IMG_84.jpg" "$DESTINO/IMG_84.jpg"
    echo "✅ IMG_84.jpg"
    ((copiadas++))
else
    echo "❌ IMG_84.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_85.jpg" ]; then
    cp "$ORIGEN/IMG_85.jpg" "$DESTINO/IMG_85.jpg"
    echo "✅ IMG_85.jpg"
    ((copiadas++))
else
    echo "❌ IMG_85.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_86.jpg" ]; then
    cp "$ORIGEN/IMG_86.jpg" "$DESTINO/IMG_86.jpg"
    echo "✅ IMG_86.jpg"
    ((copiadas++))
else
    echo "❌ IMG_86.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_87.jpg" ]; then
    cp "$ORIGEN/IMG_87.jpg" "$DESTINO/IMG_87.jpg"
    echo "✅ IMG_87.jpg"
    ((copiadas++))
else
    echo "❌ IMG_87.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_88.jpg" ]; then
    cp "$ORIGEN/IMG_88.jpg" "$DESTINO/IMG_88.jpg"
    echo "✅ IMG_88.jpg"
    ((copiadas++))
else
    echo "❌ IMG_88.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_89.jpg" ]; then
    cp "$ORIGEN/IMG_89.jpg" "$DESTINO/IMG_89.jpg"
    echo "✅ IMG_89.jpg"
    ((copiadas++))
else
    echo "❌ IMG_89.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_9.jpg" ]; then
    cp "$ORIGEN/IMG_9.jpg" "$DESTINO/IMG_9.jpg"
    echo "✅ IMG_9.jpg"
    ((copiadas++))
else
    echo "❌ IMG_9.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_90.jpg" ]; then
    cp "$ORIGEN/IMG_90.jpg" "$DESTINO/IMG_90.jpg"
    echo "✅ IMG_90.jpg"
    ((copiadas++))
else
    echo "❌ IMG_90.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_91.jpg" ]; then
    cp "$ORIGEN/IMG_91.jpg" "$DESTINO/IMG_91.jpg"
    echo "✅ IMG_91.jpg"
    ((copiadas++))
else
    echo "❌ IMG_91.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_92.jpg" ]; then
    cp "$ORIGEN/IMG_92.jpg" "$DESTINO/IMG_92.jpg"
    echo "✅ IMG_92.jpg"
    ((copiadas++))
else
    echo "❌ IMG_92.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_93.jpg" ]; then
    cp "$ORIGEN/IMG_93.jpg" "$DESTINO/IMG_93.jpg"
    echo "✅ IMG_93.jpg"
    ((copiadas++))
else
    echo "❌ IMG_93.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_94.jpg" ]; then
    cp "$ORIGEN/IMG_94.jpg" "$DESTINO/IMG_94.jpg"
    echo "✅ IMG_94.jpg"
    ((copiadas++))
else
    echo "❌ IMG_94.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_95.jpg" ]; then
    cp "$ORIGEN/IMG_95.jpg" "$DESTINO/IMG_95.jpg"
    echo "✅ IMG_95.jpg"
    ((copiadas++))
else
    echo "❌ IMG_95.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_96.jpg" ]; then
    cp "$ORIGEN/IMG_96.jpg" "$DESTINO/IMG_96.jpg"
    echo "✅ IMG_96.jpg"
    ((copiadas++))
else
    echo "❌ IMG_96.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_97.jpg" ]; then
    cp "$ORIGEN/IMG_97.jpg" "$DESTINO/IMG_97.jpg"
    echo "✅ IMG_97.jpg"
    ((copiadas++))
else
    echo "❌ IMG_97.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_98.jpg" ]; then
    cp "$ORIGEN/IMG_98.jpg" "$DESTINO/IMG_98.jpg"
    echo "✅ IMG_98.jpg"
    ((copiadas++))
else
    echo "❌ IMG_98.jpg - NO ENCONTRADA"
fi
((total++))

if [ -f "$ORIGEN/IMG_99.jpg" ]; then
    cp "$ORIGEN/IMG_99.jpg" "$DESTINO/IMG_99.jpg"
    echo "✅ IMG_99.jpg"
    ((copiadas++))
else
    echo "❌ IMG_99.jpg - NO ENCONTRADA"
fi
((total++))

echo ""
echo "📊 RESULTADO: $copiadas/$total imágenes copiadas"
echo ""
echo "🚀 SIGUIENTE PASO:"
echo "cd /Users/n.arcos89/Documents/GitHub/Diva_digital"
echo "git add imagenes/"
echo "git commit -m 'Añadir imágenes para la aplicación'"
echo "git push origin main"
echo ""
echo "✅ Después de hacer push, tu app funcionará con URLs reales de GitHub"
