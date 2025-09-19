# Onion URL Finder

Onion URL Finder is a Python script that generates random .onion URLs and checks their accessibility using the Tor network. Accessible URLs are saved to a file.

## Requirements

- Python 3.x
- Tor

## Installation

### Step 1: Clone the repository

```sh
git clone https://github.com/PASSW0RDZ/OnionV3-Link-Generator.git
cd OnionV3-Link-Generator
```

### Step 2: Install Tor

On Ubuntu 22.04, you can install Tor with the following commands:

```sh
sudo apt update
sudo apt install tor -y
sudo systemctl start tor
sudo systemctl enable tor
```

### Step 3: Install Python packages

Make sure you have Python 3 and `pip` installed. Then, install the required Python packages using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Usage

Run the script with optional command-line arguments to control its behavior:

```sh
python3 check_onions_parallel.py --limit 100 --workers 20 --timeout 10
```

- `--limit`: Number of onion URLs to check before stopping (default: unlimited).
- `--workers`: Number of parallel worker threads to use (default: 16).
- `--timeout`: Timeout in seconds for each URL check (default: 5).

The script generates and checks onion URLs based on these parameters. Results are written to `accessible_onions.txt` in a thread-safe manner using UTF-8 encoding.

## Configuration

### Logging

The script prints the status of each URL (whether it is accessible or not) to the console. Accessible URLs are also saved to `accessible_onions.txt`.

## Notes

- Ensure that the Tor service is running before executing the script.
- Random onion generation is unlikely to find real services; it is more effective to provide known onion lists for checking.
- The script may consume significant CPU and network resources depending on the number of threads used.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
