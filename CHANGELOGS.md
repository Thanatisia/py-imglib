# CHANGELOGS

## Table of Contents
+ [2024-06-18](#2024-06-18)

## Logs
### 2024-06-18
#### 1731H
+ Version: v0.1.0

- Version Changes
    + Initial Commit

- New
    + Added new document '.gitignore'
    + Added new document 'CHANGELOGS.md'
    + Added new document 'README.md'
    + Added new document 'pyproject.toml'
    + Added new document 'requirements.txt'
    - Added new directory 'src/' for the package's Source Codes
        - Added new directory 'app' for built-in CLI utility implementations utilising the core libraries
            + Added new module 'main.py' : The main entry point for the CLI utility
            + Added new module 'main-test.py' : Test entry point (to be removed)
            + Added new module 'test-lambda-transparency.py' : Testing converting of black background to transparent using lambda (To be removed)
        - Added new directory 'tests' for unit test files
            + Added new unit test 'test-core.py' for testing the core libraries
        - Added new directory 'imglib' for the ImgLib package libraries
            - Added new directory 'core' for the ImgLib core library modules
                - Added new directory 'images' for Images-related modules
                    + Added new module 'information.py' for Image information and metadata functions
                    + Added new module 'io.py' for Image I/O Processing Handling functions
                    + Added new module 'pixels.py' for Pixel-related functions
                    + Added new module 'translation.py' for Image Manipulation and Transformation functionalities

#### 1913H
+ Version: v0.1.1

- Version Changes
    - Updated pyproject.toml package configuration specifications
        + Changed package name
        + Added dependencies 'pillow'
        + Set 'main-test.py' in 'src/' as the main entry point temporarily

- Updates
    - Updated package configuration specifications document 'pyproject.toml'
        + Updated package version to v0.1.1
        + Changed package name
        + Added dependencies 'pillow'
        + Set 'main-test.py' in 'src/' as the main entry point temporarily

#### 1923H
- Updates
    - Updated package configuration specifications document 'pyproject.toml'
        + Renamed 'main-test' => 'main_test'
    - Renamed 'main-test.py' => 'main_test.py' in 'src/'
        + To be usable in a package

#### 2126H
+ Version: v0.1.2

- Version Changes
    - Updated pyproject.toml package configuration specifications
        + Updated package version to 'v0.1.2'

- Updates
    - Updated document 'README.md'
        + Added package version 'v0.1.2'
        + Converted document format from DOS to UNIX
    - Updated package configuration specifications document 'pyproject.toml'
        + Updated package version to 'v0.1.2'
    - Updated module 'main_test.py' in 'src/app'
        + Moved functions to the respective libraries
        + Added importing of package modules/libraries
    - Updated module 'information.py' in 'src/imglib/core/images/'
        + Added new functions
    - Updated module 'pixels.py' in 'src/imglib/core/images/'
        + Added new functions
        + Added RGBA color mode check
    - Updated module 'translation.py' in 'src/imglib/core/images/'
        + Added new functions
        + Added RGBA color mode check

