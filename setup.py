from setuptools import setup, find_packages

setup(
    name="CucumberGPT",
    version="0.0.1",
    author="Aylex Riom",
    author_email="p4rlx-news@pm.me",
    description="A test automation framework integrating Cucumber feature file generation with GPT models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-github/CucumberGPT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        "fastapi>=0.70.0",
        "pydantic>=1.8.2",
        "streamlit>=1.0.0",
        "qdrant-client>=0.1.0",
        # Include any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "cucumbergpt=cucumbergpt.__main__:main",
        ],
    },
)
