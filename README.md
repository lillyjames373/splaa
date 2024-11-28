# SPLAA (Simple Prebuilt Local AI Assistant)

SPLAA is an AI assistant framework that utilizes voice recognition, text-to-speech, and tool-calling capabilities to provide a conversational and interactive experience. It uses LLMs available through Ollama and has capabilities for extending functionalities through a modular tool system.

**Navigation:** [Features](#features) | [Installation](#installation) | [Dependencies](#dependencies) | [Usage](#usage) | [Available Tools](#available-tools) | [Configuration](#configuration) | [Voice Cloning](#voice-cloning) | [Adding Tools](#adding-more-tools) | [Contributing](#contributing) | [FAQ](#faq) | [Issues](#issues) | [Acknowledgments](#acknowledgments) 

## Features <a id="features"></a>

* **Voice Input:** Uses Whisper for accurate speech-to-text transcription.
* **Voice Output:** Employs a TTS engine (XTTS v2) to generate natural-sounding speech.
* **Tool Calling:** Integrates with external tools and APIs to perform actions and retrieve information.
* **Customizable:** Configure the assistant's name, system prompt, and model through command-line arguments.

## Installation <a id="installation"></a>

Install with pip:

```bash
pip install git+https://github.com/cp3249/splaa.git
```


## Dependencies <a id="dependencies"></a>

* **Ollama:** Follow the instructions on the [Ollama](https://ollama.com/download) website to install and run Ollama. You'll need a compatible LLM model with tool calling running locally.
* **Python:** (I'm using 3.12, but it may be compatible with earlier versions)

## Usage <a id="usage"></a>

Run SPLAA:

```bash
splaa --options [option] ...
```


Once SPLAA is running, it will listen for your voice. Speak your request or command. Include the assistant's name (Default is Athena) in your request or it won't respond. This is meant to be running in the background. Ex: "Athena, what's the weather like in London?".
![](https://github.com/cp3249/splaa/blob/main/example.gif)

## Available Tools <a id="available-tools"></a>

* `getWeather`: Retrieves the current weather and forecast for a given city.
* `wikipediaSearch`: Searches Wikipedia for a term and returns a summary.
* `getNews`: Retrieves news articles on a specified topic.
* `getStockPrice`: Gets the current stock price for a given ticker symbol.
* `todoList`: Manages a simple to-do list (read, add, remove items).
* `executeCommand`: (**DANGEROUS**) Executes a command in the shell. Disabled by default.
* `viewScreen`: Takes a screenshot of the current view windows and send a description to the assistant.

## Configuration <a id="configuration"></a>

You can customize the SPLAA attributes using command-line arguments:

* `--model`: Specifies the Ollama model to use (default: `qwen2.5:3b`. I recommend this model because it's the best at knowing when not to use tools and it's fast.).
* `--assistant_name`: Sets the assistant's name (default: Athena).
* `--user_name`: Sets the user's name (default: Unknown).
* `--speaker_file`: Path to the speaker WAV file for TTS cloning (should be at least 6 seconds of voice) (default: `splaa/speaker.wav`).
* `--system_prompt`: Provides the initial prompt to guide the assistant's behavior (default: "You are a very concise and to-the-point AI assistant").
* `--command_permission`: Enables/disables command execution (default: `False` because next thing you know it removes system32 :) ). Only use if you know what you're doing…seriously.
* `--enable_vision`: Enables/disables vision capabilities for the model(default: `False` very vram expensive. I recommend only enabling this if you're rich and have a 24 gb 3090/4090)
* `--vision_model`: Specifies the vision model to use. **--enable_vision must be set to True** (default: `minicpm-v` after a little bit of testing this offered the best quality for the best speed.)


## Voice Cloning <a id="voice-cloning"></a>

Here's a quick guide to clone voices from YouTube clips for those who don't already have a speaker file:

1. **Download the [yt-dlp](https://github.com/yt-dlp/yt-dlp) executable:**
2. **Extract audio section:** In the directory containing the executable, open your terminal and execute this command (replace `video_url_here` with the actual URL, and adjust `-ss` and `-t` for start and end times):

```bash
./yt-dlp -f bestaudio --postprocessor-args "-ss 00:00:00 -t 00:00:06" -x --audio-format wav video_url_here
```
   Pick a section of voice at least 6 seconds long for best results, the less background noise the better.


## Adding more tools <a id="adding-more-tools"></a>

You can add your own functions. All functions are located in the `splaa/helperFunctions.py` file.  The structure is as follows:

**Define Your Function:** Inside `helperFunctions.py`, define your function. It should:

* Have a clear purpose.
* Accept necessary input parameters.
* Return a string (or a JSON string for complex data).
* Include error handling for less headaches at runtime.

**Add it to the tools and available_functions:** Follow the format in the file or look at the  documentation for [Ollama Python tools](https://github.com/ollama/ollama-python/blob/main/examples/tools/main.py)

## Contributing <a id="contributing"></a>

Contributors are welcome! Please create a pull request with a clear description of your changes.

## FAQ <a id="faq"></a>

**Question:** Why is splaa running extremely slowly?

**Answer:** This project uses many machine learning models that are slow to run on non-GPU-accelerated hardware. It defaults to CPU. For those with NVIDIA cards, I suggest downloading CUDA drivers from the NVIDIA website [cuda-downloads](https://developer.nvidia.com/cuda-downloads) and installing the corresponding PyTorch version for your CUDA version here [cuda-pytorch](https://pytorch.org/get-started/locally/). If you have an AMD card…sorry, you're out of luck for now.

**Question:** Why is the `splaa` command not being recognized by my terminal after installing?

**Answer:** This is most likely because your Python scripts are not in your system path. This is a common issue for Microsoft Store Python installations. Check this file location (for Windows) `"C:\Users\yournamehere\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts"` and make sure it exists. If it does, add it to your system path using your preferred method. If it doesn't exist…perform a clean installation of Python.

**Question:** Why is splaa talking weirdly (toolspeak) output?

**Answer:** I'm not fully sure why this happens yet, but it can occur from time to time. The best solution is to restart the model, and if that doesn't work, reinstall the package. It's possibly an Ollama bug.

## Issues <a id="issues"></a>

For any issues, please create a request in the issue tab.

## Acknowledgments <a id="acknowledgments"></a>

This project uses a [Coqui TTS fork](https://github.com/idiap/coqui-ai-TTS) for Python 3.12 made by saviors because they haven't updated the main branch for some reason.

