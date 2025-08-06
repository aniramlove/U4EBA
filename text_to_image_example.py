#!/usr/bin/env python3
"""
Пример генерации изображений из текста с помощью Stable Diffusion
"""

import torch
from diffusers import StableDiffusionPipeline

def generate_image(prompt, output_path="generated_image.png"):
    """
    Генерирует изображение по текстовому описанию
    
    Args:
        prompt (str): Текстовое описание изображения
        output_path (str): Путь для сохранения изображения
    """
    
    # Определяем устройство (GPU если доступен, иначе CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Используется устройство: {device}")
    
    # Загружаем модель Stable Diffusion
    print("Загружаем модель Stable Diffusion...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    # Настройки для экономии памяти
    if device == "cuda":
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    
    print(f"Генерируем изображение для промпта: '{prompt}'")
    
    # Генерируем изображение
    with torch.autocast(device):
        image = pipe(
            prompt,
            num_inference_steps=20,  # Количество шагов диффузии
            guidance_scale=7.5,      # Сила следования промпту
            height=512,              # Высота изображения
            width=512               # Ширина изображения
        ).images[0]
    
    # Сохраняем изображение
    image.save(output_path)
    print(f"Изображение сохранено: {output_path}")
    
    return image

def main():
    # Примеры промптов для генерации
    prompts = [
        "Красивый закат над горами, фотореалистично",
        "Космический корабль в стиле киберпанк",
        "Милый котенок играет с клубком пряжи",
        "Волшебный лес с светящимися грибами"
    ]
    
    print("=== Генерация изображений с помощью Stable Diffusion ===\n")
    
    # Генерируем изображения для каждого промпта
    for i, prompt in enumerate(prompts):
        try:
            output_path = f"image_{i+1}.png"
            generate_image(prompt, output_path)
            print(f"✅ Успешно сгенерировано изображение {i+1}\n")
        except Exception as e:
            print(f"❌ Ошибка при генерации изображения {i+1}: {e}\n")

if __name__ == "__main__":
    main()