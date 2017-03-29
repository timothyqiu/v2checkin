# v2checkin

This project is a Way to Checkin.

## Configuration

Create a config file `~/.v2checkin.config`. Example:

    {
        "v2ex": {
            "username": "v2ex_username",
            "password": "p@55w0rd"
        },
        "xiami": {
            "username": "xiami_username",
            "password": "p@55w0rd"
        },
        "smzdm": {
            "username": "smzdm_username",
            "password": "p@55w0rd"
        }
    }

You can ommit any entry if it is not needed.

## Command line arguments

You can use arguments to override settings from `.v2checkin.config`.

    v2checkin -c path/to/config
