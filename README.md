# Fine-tune Llama model with MLX

Reproduce the blog post [Fine-tune Llama model with MLX](https://samkuo.me/post/2024/08/fine-tune-llama-31-with-mlx-on-mac/)

## Pre-requisites

1. You need a Hugging Face account
2. Install HF cli `brew install huggingface-cli`
3. Get token in `https://huggingface.co/settings/tokens`
4. Create a conda env `conda create -n mlx-env python=3.10 -y`
5. Activate the env `conda activate mlx-env`
6. Install the dependencies `pip install datasets mlx-lm`

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
./mlx-ft.sh fetch
```

## Begin fine-tuning

```
./mlx-ft.sh train
```

This actually runs `mlx_lm.lora --config lora_config.yaml`

## Fuse the model

```
./mlx-ft.sh fuse
```

Actually runs:

```
mlx_lm.fuse \
      --model ${local_model} \
      --save-path "${fused_model}" \
      --adapter-path ./adapters \
      --de-quantize
```

## Build the Ollama model

This is a time-consuming process. In this case, the dataset from mlx-examples is used instead.

```
./mlx-ft.sh create
```

```
python ./llama.cpp/convert-hf-to-gguf.py --outfile ./models/model.gguf --outtype q8_0 ./models/llama3.1-spk1
```

## Run the fine-tuned model locally with Ollama

```
./mlx-ft.sh create
```

## Run the fine-tuned model with Ollama

```
./mlx-ft.sh run
```
