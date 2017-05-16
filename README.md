# gnunigma
[Basic information](#basic-information) | [Compatibility](#compatibility) | [Installation](#installation) | [Requirements](#requirements) | [Platform differences](#features-missing-in-the-ubuntu-version) | [FAQ](#faq) | [License](#license)
## Basic information
* Gnunigma simulates the *enigma encryption machine*, which was used by the Germans in 20th century.
* **Language of choice** - python
* **Graphical library** - tkinter/Tkinter

----
## Compatibility
* Gnunigma was tested on Windows 10 and Ubuntu (16.04, 16.10, 17.04) and should be compatible

### Installation
1. Download the source
2. If you are on Ubuntu and don't have Tkinter installed on python 3, run this command
```bash
sudo apt-get install python3-tk
```
3. Run the ```runtime.py``` file with python 3

### Requirements
1. Python version 3.5 and newer (older python 3 versions might work aswell but were not tested by me!)
   * *tkinter* library is included on Windows by default but must be installed on Ubuntu

### Features missing in the Ubuntu version
1. **Sound** - gnunigma on Windows is using the *winsound* library, which is not available on linux
2. **Icons** - there were some issues with iconbitmaps on
3. **Styling** - The gui does not looks as good as on Windows (scaling, weird colors)

## FAQ
* If you have any questions, visit the wiki first (mostly incomplete!) or PM me.

---
## License
* The project is licensed with [GNU GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License)
