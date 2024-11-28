from setuptools import setup, find_packages

setup(
    name='splaa',
    version='1.1',
    description='A local AI assistant framework with tool calling capabilities, TTS, and voice recognition',
    author='Claude Petit-Frere',
    author_email='cp3249@drexel.edu',
    packages=find_packages(),
    install_requires=[
        'ollama==0.3.3',
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