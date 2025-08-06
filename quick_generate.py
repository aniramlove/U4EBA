#!/usr/bin/env python3
"""
Простой скрипт для быстрой генерации изображения по вашему описанию
"""

import torch
from diffusers import StableDiffusionPipeline
import sys

def generate_single_image(prompt, filename="my_image.png"):
    """Генерирует одно изображение по промпту"""
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Используется устройство: {device}")
    
    # Загружаем модель
    print("Загружаем модель...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    # Оптимизация памяти
    if device == "cuda":
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    
    print(f"Генерируем: '{prompt}'")
    
    # Генерация
    with torch.autocast(device):
        image = pipe(
            prompt,
            num_inference_steps=20,
            guidance_scale=7.5,
            height=512,
            width=512
        ).images[0]
    
    # Сохранение
    image.save(filename)
    print(f"✅ Изображение сохранено как: {filename}")
    
    return image

if __name__ == "__main__":
    # Если передан аргумент командной строки, используем его как промпт
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        # Иначе запрашиваем у пользователя
        user_prompt = input("Введите описание изображения: ")
    
    # Создаем имя файла на основе промпта
    safe_filename = "".join(c for c in user_prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_').lower() + ".png"
    
    try:
        generate_single_image(user_prompt, safe_filename)
        print(f"\n🎨 Ваше изображение готово!")
        print(f"📁 Файл: {safe_filename}")
        print(f"📝 Описание: {user_prompt}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")