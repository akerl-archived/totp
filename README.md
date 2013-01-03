# Requirements

PyYaml (pip install pyyaml)

# Contents

## generate.py

This script creates the YAML config files for authenticating users. It walks you through the process, and either dumps the results to stdout or a file.

## totp.py

This handles the config file reading, key manipulation, and code validation. General practice is to instantiate a totp.Config(file) object, get your code, then call Config().authenticate(code) to check it.

## pam.py

This is designed to work with pam_exec. It handles reading from and writing to the tty to get the code, and returns 0 or 1 to pam_exec to handle authentication.

## sshd.py

This can be used with ForceCommand in sshd_config, and will os.execl the user's shell if successful.


