#!/usr/bin/env python3
"""
Показывает информацию о сгенерированных изображениях
"""

import os
from PIL import Image
import glob

def show_image_info():
    """Показывает информацию о всех PNG файлах в текущей директории"""
    
    print("🎨 " + "="*60)
    print("           СГЕНЕРИРОВАННЫЕ ИЗОБРАЖЕНИЯ")
    print("="*62)
    
    # Описания изображений
    descriptions = {
        "image_1.png": "Красивый закат над горами, фотореалистично",
        "image_2.png": "Космический корабль в стиле киберпанк",
        "image_3.png": "Милый котенок играет с клубком пряжи",
        "image_4.png": "Волшебный лес с светящимися грибами",
        "красивая_девушка_с_длинными_во.png": "Красивая девушка с длинными волосами в лесу"
    }
    
    # Находим все PNG файлы
    png_files = glob.glob("*.png")
    
    if not png_files:
        print("❌ Изображения не найдены!")
        return
    
    for i, filename in enumerate(png_files, 1):
        try:
            # Получаем информацию о файле
            file_size = os.path.getsize(filename)
            
            # Получаем размеры изображения
            with Image.open(filename) as img:
                width, height = img.size
                
            print(f"\n📸 Изображение {i}:")
            print(f"   📁 Файл: {filename}")
            print(f"   📝 Описание: {descriptions.get(filename, 'Пользовательское изображение')}")
            print(f"   📏 Размер: {width}x{height} пикселей")
            print(f"   💾 Размер файла: {file_size/1024:.1f} KB")
            print(f"   🌐 Веб-ссылка: http://localhost:8000/{filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {filename}: {e}")
    
    print("\n" + "="*62)
    print("💡 СПОСОБЫ ПРОСМОТРА:")
    print("1. Откройте http://localhost:8000/view_images.html в браузере")
    print("2. Откройте файлы напрямую в папке /workspace/")
    print("3. Скачайте файлы на свой компьютер")
    print("="*62)

if __name__ == "__main__":
    show_image_info()