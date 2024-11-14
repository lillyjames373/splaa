from setuptools import setup, find_packages

setup(
    name='splaa',
    version='1.0',
    description='A local AI assistant framework with tool calling capabilities, TTS, and voice recognition',
    author='Claude Petit-Frere',
    author_email='cp3249@drexel.edu',
    packages=find_packages(),
    install_requires=[
        'ollama',
        'librosa',
        'torch',
        'openai-whisper',
        'numpy',
        'coqui-tts',
        'sounddevice',
        'python-weather',
        'wikipedia',
        'yfinance',
        'GoogleNews',
    ],
    entry_points={
        'console_scripts': [
            'splaa=splaa.splaacli:main',
        ],
    },
    include_package_data=True,
)