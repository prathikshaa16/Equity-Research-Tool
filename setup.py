from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="equity-ai-research-tool",
    version="1.0.0",
    author="EquityAI Team",
    author_email="contact@equityai.com",
    description="AI-powered Equity Research Tool using NLP and Generative AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/equityai/research-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "gpu": [
            "torch[cuda]>=2.1.1",
            "transformers[accelerate]>=4.36.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "equityai-backend=backend.run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "backend": ["app/nlp/models/*"],
    },
)
