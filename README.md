# Fine-tune Qwen model with MLX

Reproduce the blog post [Fine-tune Qwen2.5 with MLX on Mac](https://samkuo.me/post/2024/08/fine-tune-llama-31-with-mlx-on-mac/)

## Pre-requisites

1. You need a Hugging Face account
2. Install HF cli `brew install huggingface-cli aria2`
3. Get token in `https://huggingface.co/settings/tokens`
4. Create a conda env `conda create -n mlx-env python=3.10 -y`
5. Activate the env `conda activate mlx-env`
6. Install the dependencies `pip install datasets mlx-lm`
7. Using the HF mirror: `export HF_ENDPOINT=https://hf-mirror.com`
8. Install cli tool [htd](https://gist.github.com/padeoe/697678ab8e528b85a2a7bddafea1fa4f)

## Checkout code

```
git clone --recurse-submodules https://github.com/sampot/mlx-llama-finetune.git
```

## Install dependencies

```
./mlx-ft.sh install
```

Using the specific branch of llama.cpp (mentioned in the blog post)

```
cd llama.cpp
git checkout b3418
```

## Prepare training dataset

```
./mlx-ft.sh data
```

## Download the source model

```
mlx_lm.convert --hf-path Qwen/Qwen2.5-7B-Instruct --mlx-path ./models/mlx -q # or ./mlx-ft.sh fetch
```

Also can use `hfd` to download the model first:

```
hfd Qwen/Qwen2.5-7B-Instruct --hf_username xxxx --hf_token hf_xxxxx
mlx_lm.convert --hf-path Qwen/Qwen2.5-7B-Instruct --mlx-path ./models/mlx -q
```

This will download and quantize the Qwen2.5-7B-Instruct model.

## Begin fine-tuning

```
./mlx-ft.sh train
```

This runs `mlx_lm.lora --config lora_config.yaml` to fine-tune the Qwen model.

## Fuse the model

```
./mlx-ft.sh fuse
```

This fuses the LoRA weights with the base model:

```
mlx_lm.fuse \
      --model ${local_model} \
      --save-path "${fused_model}" \
      --adapter-path ./adapters \
      --de-quantize
```

## Build the Ollama model

This converts the model to GGUF format for use with Ollama:

```
./mlx-ft.sh create
```

## Run the fine-tuned model with Ollama

```
./mlx-ft.sh run
```