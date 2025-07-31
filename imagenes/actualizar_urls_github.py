#!/usr/bin/env python3
"""
Script para actualizar automáticamente las URLs del CSV publicaciones_pixabay_ok.csv
para que apunten a las imágenes en GitHub.
"""

import pandas as pd
import os

def actualizar_urls_github():
    """
    Actualiza todas las URLs del CSV para que apunten a GitHub
    """
    # Rutas
    csv_path = "Data/publicaciones_pixabay_ok.csv"
    backup_path = "Data/publicaciones_pixabay_ok_backup.csv"
    
    # URL base de GitHub
    github_base_url = "https://raw.githubusercontent.com/Natarcos/Diva_digital/main/imagenes/"
    
    try:
        print("🔄 Cargando CSV actual...")
        df = pd.read_csv(csv_path)
        
        # Crear backup
        print("💾 Creando backup del archivo original...")
        df.to_csv(backup_path, index=False)
        
        print(f"📊 Filas totales en el CSV: {len(df)}")
        
        # Verificar columnas necesarias
        if 'Imagen' not in df.columns:
            print("❌ Error: No se encontró la columna 'Imagen'")
            return
            
        if 'URL_Publica' not in df.columns:
            print("❌ Error: No se encontró la columna 'URL_Publica'")
            return
        
        # Actualizar URLs
        print("🔧 Generando nuevas URLs de GitHub...")
        urls_actualizadas = 0
        
        for index, row in df.iterrows():
            imagen_nombre = row['Imagen']
            if pd.notna(imagen_nombre) and imagen_nombre.strip():
                # Generar nueva URL de GitHub
                nueva_url = f"{github_base_url}{imagen_nombre}"
                df.at[index, 'URL_Publica'] = nueva_url
                urls_actualizadas += 1
        
        print(f"✅ URLs actualizadas: {urls_actualizadas}")
        
        # Guardar CSV actualizado
        print("💾 Guardando CSV actualizado...")
        df.to_csv(csv_path, index=False)
        
        # Mostrar algunas URLs de ejemplo
        print("\n📋 Ejemplos de URLs actualizadas:")
        for i in range(min(5, len(df))):
            imagen = df.iloc[i]['Imagen']
            url = df.iloc[i]['URL_Publica']
            print(f"   • {imagen} → {url}")
        
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        print(f"✅ Archivo actualizado: {csv_path}")
        print(f"💾 Backup guardado en: {backup_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el proceso: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando actualización de URLs de GitHub...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("Data/publicaciones_pixabay_ok.csv"):
        print("❌ Error: No se encontró el archivo Data/publicaciones_pixabay_ok.csv")
        print("   Asegúrate de ejecutar este script desde la carpeta raíz del proyecto Diva_digital")
        exit(1)
    
    # Ejecutar actualización
    success = actualizar_urls_github()
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("1. Verifica que las URLs se generaron correctamente")
        print("2. Prueba la aplicación para confirmar que las imágenes cargan")
        print("3. Si todo funciona, puedes eliminar el archivo backup")
    else:
        print("\n🔄 Si algo salió mal, restaura desde el backup:")
        print("   cp Data/publicaciones_pixabay_ok_backup.csv Data/publicaciones_pixabay_ok.csv")
