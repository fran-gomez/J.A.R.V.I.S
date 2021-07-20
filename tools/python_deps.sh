pip install pyttsx3
pip install speechrecognition pyaudio
pip install wikipedia
pip install pyautogui
pip install psutil

if [ $HOST == "m1 mac" ]; then
    brew uninstall portaudio
    brew install portaudio --HEAD
    cd $(brew --prefix portaudio)

    # Links the headers to /usr/local/include
    for f in $PWD/include/*.h; do ln -sfv $f /usr/local/include/${f##*/}; done

    # Links the static libs to /usr/local/lib
    for f in $PWD/lib/*.a; do ln -sfv $f /usr/local/lib/${f##*/}; done

    # Links the dynamic libs to /usr/local/lib
    for f in $PWD/lib/*.dylib; do ln -sfv $f /usr/local/lib/${f##*/}; done

    pip3 install pyaudio
fi