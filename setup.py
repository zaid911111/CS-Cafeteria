from setuptools import setup, find_packages

setup(
    name="college-cafeteria",
    version="0.1.0",
    description="A web application for ordering food from a college cafeteria",
    author="College Cafeteria Team",
    author_email="cafeteria@college.edu",
    url="https://github.com/college/cafeteria",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.1",
        "python-dotenv>=0.19.0",
        "SQLAlchemy>=1.4.0",
        "Flask-SQLAlchemy>=2.5.0",
        "Flask-WTF>=1.0.0",
    ],
    package_data={
        "": ["templates/*.html", "static/css/*.css", "static/js/*.js", "static/images/*"],
    },
    entry_points={
        "console_scripts": [
            "college-cafeteria=app:run_app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    keywords="college, cafeteria, food ordering",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/college/cafeteria/issues",
        "Documentation": "https://college-cafeteria.readthedocs.io/",
        "Source Code": "https://github.com/college/cafeteria",
    },
)
