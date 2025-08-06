#!/usr/bin/env python3
"""
Пример модификации изображений с помощью Stable Diffusion Image-to-Image
"""

import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import requests
from io import BytesIO

def modify_image(input_image_path, prompt, output_path="modified_image.png", strength=0.75):
    """
    Модифицирует существующее изображение согласно текстовому описанию
    
    Args:
        input_image_path (str): Путь к исходному изображению или URL
        prompt (str): Текстовое описание желаемых изменений
        output_path (str): Путь для сохранения результата
        strength (float): Сила модификации (0.0-1.0)
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Используется устройство: {device}")
    
    # Загружаем модель Image-to-Image
    print("Загружаем модель Stable Diffusion Img2Img...")
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    # Настройки для экономии памяти
    if device == "cuda":
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    
    # Загружаем исходное изображение
    try:
        if input_image_path.startswith('http'):
            response = requests.get(input_image_path)
            init_image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            init_image = Image.open(input_image_path).convert("RGB")
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return None
    
    # Изменяем размер изображения для модели
    init_image = init_image.resize((512, 512))
    
    print(f"Модифицируем изображение с промптом: '{prompt}'")
    print(f"Сила модификации: {strength}")
    
    # Генерируем модифицированное изображение
    with torch.autocast(device):
        image = pipe(
            prompt=prompt,
            image=init_image,
            strength=strength,        # Сила модификации
            guidance_scale=7.5,      # Сила следования промпту
            num_inference_steps=20   # Количество шагов
        ).images[0]
    
    # Сохраняем результат
    image.save(output_path)
    print(f"Модифицированное изображение сохранено: {output_path}")
    
    return image

def create_sample_image():
    """Создает простое изображение для демонстрации"""
    from PIL import Image, ImageDraw
    
    # Создаем простое изображение с геометрическими фигурами
    img = Image.new('RGB', (512, 512), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Рисуем простые фигуры
    draw.rectangle([100, 100, 400, 400], fill='white', outline='black', width=3)
    draw.ellipse([150, 150, 350, 350], fill='yellow', outline='orange', width=2)
    
    sample_path = "sample_input.png"
    img.save(sample_path)
    print(f"Создано пробное изображение: {sample_path}")
    return sample_path

def main():
    print("=== Модификация изображений с помощью Stable Diffusion ===\n")
    
    # Создаем пробное изображение если нет собственного
    sample_image = create_sample_image()
    
    # Примеры модификаций
    modifications = [
        {
            "prompt": "Превратить в красивый пейзаж с горами и озером",
            "strength": 0.8,
            "output": "landscape_modification.png"
        },
        {
            "prompt": "Сделать в стиле импрессионистской живописи",
            "strength": 0.6,
            "output": "impressionist_style.png"
        },
        {
            "prompt": "Добавить космическую тематику со звездами",
            "strength": 0.7,
            "output": "space_theme.png"
        }
    ]
    
    # Применяем различные модификации
    for i, mod in enumerate(modifications):
        try:
            print(f"\n--- Модификация {i+1} ---")
            modify_image(
                input_image_path=sample_image,
                prompt=mod["prompt"],
                output_path=mod["output"],
                strength=mod["strength"]
            )
            print(f"✅ Успешно создана модификация {i+1}")
        except Exception as e:
            print(f"❌ Ошибка при модификации {i+1}: {e}")
    
    print("\n=== Все модификации завершены ===")

if __name__ == "__main__":
    main()