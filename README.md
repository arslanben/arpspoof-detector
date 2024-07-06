# Arslan's Detector

<img src="https://i.imgur.com/bFk5qjc.jpg" width="300" height="200">  <img src="https://i.imgur.com/Oq62icW.jpg" width="300" height="200">  <img src="https://i.imgur.com/T8QEuWd.jpg" width="300" height="200">

This project warns you about arp spoof attacks on your Windows system.

## Requirements

You can run the relevant file to check the necessary requirements. It will automatically check the requirements for you and if anything is missing, you will be able to indicate this and direct it to download it if you wish.

## Installation

1. Clone the project:

    ```sh
    git clone https://github.com/arslanben/arpspoof-detector.git
    cd arpspoof-detector
    ```

2. As mentioned in the description, we run the file directly and provide checks.
   
    ```console
    .\requirements.bat
    ```

## Usage

After starting your Windows system, run this file directly.  This ensures that the original version of your ARP table is saved.

To run the Python file:

```sh
python3 .\arp-detecter.py
```
