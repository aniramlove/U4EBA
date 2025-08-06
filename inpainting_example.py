#!/usr/bin/env python3
"""
Пример инпейнтинга (заполнения части изображения) с помощью Stable Diffusion
"""

import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image, ImageDraw
import numpy as np

def create_sample_image_with_mask():
    """Создает пример изображения и маски для демонстрации инпейнтинга"""
    
    # Создаем изображение с простой сценой
    img = Image.new('RGB', (512, 512), color='lightgreen')
    draw = ImageDraw.Draw(img)
    
    # Рисуем небо
    draw.rectangle([0, 0, 512, 200], fill='lightblue')
    
    # Рисуем дом
    draw.rectangle([150, 250, 350, 400], fill='brown', outline='black', width=2)
    
    # Рисуем крышу
    draw.polygon([(150, 250), (250, 150), (350, 250)], fill='red', outline='black')
    
    # Рисуем окно
    draw.rectangle([200, 300, 300, 350], fill='lightblue', outline='black', width=2)
    
    # Рисуем дерево
    draw.rectangle([400, 300, 420, 400], fill='brown')  # ствол
    draw.ellipse([380, 250, 440, 320], fill='green')   # крона
    
    img.save("sample_scene.png")
    print("Создано пробное изображение: sample_scene.png")
    
    # Создаем маску - белые области будут заменены
    mask = Image.new('RGB', (512, 512), color='black')
    mask_draw = ImageDraw.Draw(mask)
    
    # Маска для замены неба (белая область)
    mask_draw.rectangle([0, 0, 512, 200], fill='white')
    
    mask.save("sky_mask.png")
    print("Создана маска для неба: sky_mask.png")
    
    # Создаем маску для замены дерева
    tree_mask = Image.new('RGB', (512, 512), color='black')
    tree_mask_draw = ImageDraw.Draw(tree_mask)
    tree_mask_draw.ellipse([375, 245, 445, 325], fill='white')  # область дерева
    tree_mask_draw.rectangle([395, 295, 425, 405], fill='white')  # ствол
    
    tree_mask.save("tree_mask.png")
    print("Создана маска для дерева: tree_mask.png")
    
    return "sample_scene.png", ["sky_mask.png", "tree_mask.png"]

def inpaint_image(image_path, mask_path, prompt, output_path):
    """
    Выполняет инпейнтинг изображения
    
    Args:
        image_path (str): Путь к исходному изображению
        mask_path (str): Путь к маске (белые области будут заменены)
        prompt (str): Описание того, чем заполнить замаскированную область
        output_path (str): Путь для сохранения результата
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Используется устройство: {device}")
    
    # Загружаем модель для инпейнтинга
    print("Загружаем модель Stable Diffusion Inpainting...")
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    # Настройки для экономии памяти
    if device == "cuda":
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    
    # Загружаем изображение и маску
    try:
        image = Image.open(image_path).convert("RGB")
        mask_image = Image.open(mask_path).convert("RGB")
        
        # Изменяем размер под модель
        image = image.resize((512, 512))
        mask_image = mask_image.resize((512, 512))
        
    except Exception as e:
        print(f"Ошибка загрузки файлов: {e}")
        return None
    
    print(f"Выполняем инпейнтинг с промптом: '{prompt}'")
    
    # Выполняем инпейнтинг
    with torch.autocast(device):
        result = pipe(
            prompt=prompt,
            image=image,
            mask_image=mask_image,
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]
    
    # Сохраняем результат
    result.save(output_path)
    print(f"Результат инпейнтинга сохранен: {output_path}")
    
    return result

def main():
    print("=== Инпейнтинг с помощью Stable Diffusion ===\n")
    
    # Создаем пробные изображения и маски
    image_path, mask_paths = create_sample_image_with_mask()
    
    # Примеры инпейнтинга
    inpainting_tasks = [
        {
            "mask": mask_paths[0],  # маска неба
            "prompt": "Красивое закатное небо с облаками",
            "output": "sunset_sky_inpaint.png",
            "description": "Замена неба на закатное"
        },
        {
            "mask": mask_paths[0],  # маска неба
            "prompt": "Звездное ночное небо с млечным путем",
            "output": "starry_sky_inpaint.png",
            "description": "Замена неба на звездное"
        },
        {
            "mask": mask_paths[1],  # маска дерева
            "prompt": "Большая пальма с кокосами",
            "output": "palm_tree_inpaint.png",
            "description": "Замена дерева на пальму"
        }
    ]
    
    # Выполняем различные инпейнтинги
    for i, task in enumerate(inpainting_tasks):
        try:
            print(f"\n--- {task['description']} ---")
            inpaint_image(
                image_path=image_path,
                mask_path=task["mask"],
                prompt=task["prompt"],
                output_path=task["output"]
            )
            print(f"✅ Успешно выполнен инпейнтинг {i+1}")
        except Exception as e:
            print(f"❌ Ошибка при инпейнтинге {i+1}: {e}")
    
    print("\n=== Все инпейнтинги завершены ===")
    print("\nСозданные файлы:")
    print("- sample_scene.png (исходное изображение)")
    print("- sky_mask.png (маска для неба)")
    print("- tree_mask.png (маска для дерева)")
    print("- sunset_sky_inpaint.png (небо заменено на закатное)")
    print("- starry_sky_inpaint.png (небо заменено на звездное)")
    print("- palm_tree_inpaint.png (дерево заменено на пальму)")

if __name__ == "__main__":
    main()