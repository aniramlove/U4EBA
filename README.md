# Руководство по использованию Diffusers

Этот проект содержит примеры использования библиотеки Diffusers от Hugging Face для генерации изображений с помощью ИИ.

## 🚀 Установка

### 1. Создание виртуального окружения
```bash
python3 -m venv diffusers_env
source diffusers_env/bin/activate  # На Linux/Mac
# или
diffusers_env\Scripts\activate     # На Windows
```

### 2. Установка зависимостей
```bash
pip install git+https://github.com/huggingface/diffusers
pip install torch torchvision transformers accelerate
```

## 📁 Файлы проекта

- **`quick_generate.py`** - Быстрая генерация одного изображения
- **`text_to_image_example.py`** - Подробный пример генерации из текста
- **`image_to_image_example.py`** - Модификация существующих изображений
- **`inpainting_example.py`** - Заполнение части изображения

## 🎨 Быстрый старт

### Генерация изображения по описанию:
```bash
python quick_generate.py "красивый пейзаж с горами"
```

### Интерактивная генерация:
```bash
python quick_generate.py
# Введите описание когда появится запрос
```

## 📖 Подробные примеры

### 1. Генерация изображений из текста
```bash
python text_to_image_example.py
```
Создает 4 изображения с разными промптами.

### 2. Модификация изображений
```bash
python image_to_image_example.py
```
Модифицирует существующее изображение согласно новому описанию.

### 3. Инпейнтинг (заполнение части изображения)
```bash
python inpainting_example.py
```
Заменяет выбранные части изображения новым содержимым.

## ⚙️ Настройки генерации

### Основные параметры:

- **`prompt`** - Текстовое описание изображения
- **`num_inference_steps`** - Количество шагов (больше = качественнее, но медленнее)
- **`guidance_scale`** - Сила следования промпту (7.5 - хорошее значение)
- **`height/width`** - Размер изображения (512x512 стандарт)

### Пример настройки:
```python
image = pipe(
    prompt="космический корабль",
    num_inference_steps=50,  # больше шагов для лучшего качества
    guidance_scale=10,       # сильнее следовать промпту
    height=768, width=768    # больше разрешение
).images[0]
```

## 💡 Советы для лучших результатов

### 1. Хорошие промпты:
- **Детальные описания**: "красивая девушка с длинными рыжими волосами в зеленом платье"
- **Стиль**: "в стиле фотореализма", "акварельная живопись", "аниме"
- **Освещение**: "мягкий свет", "закатное освещение", "драматичные тени"
- **Качество**: "высокое качество", "детализированно", "4k", "professional photo"

### 2. Примеры хороших промптов:
```
"портрет красивой женщины, фотореалистично, студийное освещение, высокое качество"
"космический корабль в стиле киберпанк, неоновые огни, детализированно"
"уютный домик в лесу, акварельная живопись, мягкие цвета"
"дракон летит над замком, фэнтези арт, эпично, детализированно"
```

### 3. Негативные промпты (что исключить):
Добавьте `negative_prompt` для лучших результатов:
```python
image = pipe(
    prompt="красивый пейзаж",
    negative_prompt="размытый, плохое качество, искаженный",
    # другие параметры...
).images[0]
```

## 🖥️ Требования к системе

- **CPU**: Работает на любом процессоре (медленно)
- **GPU**: NVIDIA GPU с CUDA для быстрой генерации
- **RAM**: Минимум 8GB, рекомендуется 16GB+
- **Место на диске**: ~10GB для моделей

## 🔧 Оптимизация производительности

### Для экономии памяти:
```python
pipe.enable_attention_slicing()
pipe.enable_model_cpu_offload()
```

### Для GPU:
```python
pipe = pipe.to("cuda")
torch_dtype=torch.float16  # вместо float32
```

## 🎯 Различные задачи

### Text-to-Image (Текст в изображение)
```python
from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
```

### Image-to-Image (Модификация изображения)
```python
from diffusers import StableDiffusionImg2ImgPipeline
pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
```

### Inpainting (Заполнение части изображения)
```python
from diffusers import StableDiffusionInpaintPipeline
pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting")
```

## 🚨 Устранение проблем

### Ошибка памяти:
- Уменьшите размер изображения
- Используйте `enable_attention_slicing()`
- Закройте другие программы

### Медленная генерация:
- Уменьшите `num_inference_steps`
- Используйте GPU вместо CPU
- Используйте `torch.float16`

### Плохое качество:
- Увеличьте `num_inference_steps`
- Улучшите промпт
- Используйте `negative_prompt`

## 📚 Дополнительные ресурсы

- [Документация Diffusers](https://huggingface.co/docs/diffusers)
- [Hugging Face Hub](https://huggingface.co/models?library=diffusers)
- [Stable Diffusion модели](https://huggingface.co/runwayml)

## 🎉 Готово!

Теперь вы можете создавать удивительные изображения с помощью ИИ! Экспериментируйте с различными промптами и настройками для получения лучших результатов.
