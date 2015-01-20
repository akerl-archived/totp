**Inactive Project:** I no longer use this, in favor of adjusting my workflow and using [the google-authenticator PAM project](https://github.com/akerl/google-authenticator)

totp
=========

[![MIT Licensed](http://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://tldrlegal.com/license/mit-license)

This module implements RFC 6238, TOTP authentication.

## Usage

### generate.py

This script creates the YAML config files for authenticating users. It walks you through the process, and either dumps the results to stdout or a file.

### totp.py

This handles the config file reading, key manipulation, and code validation. General practice is to instantiate a totp.Config(file) object, get your code, then call Config().authenticate(code) to check it.

### pam.py

This is designed to work with pam\_exec. It handles reading from and writing to the tty to get the code, and returns 0 or 1 to pam\_exec to handle authentication.

### sshd.py

This can be used with ForceCommand in sshd\_config, and will os.execl the user's shell if successful.

## Requirements

PyYAML

## License

totp is released under the MIT License. See the bundled LICENSE file for details.

