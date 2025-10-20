## Requirements: ##
- Python 3.10+ (3.11 recommended)

- macOS/Windows/Linux
- (macOS) Homebrew for PortAudio: brew install portaudio
- OpenAI API key (for GPT/Whisper mode)

## Install & Run ##
- ### Clone the repo ###

```
git clone https://github.com/<your-username>/handfreecooking.git
cd handfreecooking
```

- ### Create & activate a virtual environment ###

```
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# venv\Scripts\Activate.ps1
```

- ### Install dependencies ###

```
pip install --upgrade pip
pip install -r requirements.txt
```
- ### Configure your OpenAI API key ###

    * Temporary (per terminal session):

        * #### macOS / Linux (zsh/bash) ####

            ```
            export OPENAI_API_KEY="sk-xxxxxxxx"
            ```

        * #### Windows (PowerShell) ####

            ```
            setx OPENAI_API_KEY "sk-xxxxxxxx"
            ```

    * Permanent (macOS zsh)
        ```
        echo 'export OPENAI_API_KEY="sk-xxxxxxxx"' >> ~/.zshrc
        source ~/.zshrc
        ```


