# Flaskerino Fun App 🚀

A tiny Flask server that demonstrates how environment variables can tweak runtime behaviour.

## Environment Variables

| Variable       | Purpose                                         | Default |
| -------------- | ----------------------------------------------- | ------- |
| `DESIRED_PATH` | Path the server listens on (e.g. `/hello`)      | `/`     |
| `PORT`         | Port Flask binds to inside the container         | `80`    |
| `NUMBER`       | Arbitrary number displayed in the greeting       | `0`     |

## Local run (Debian/Ubuntu)

```bash
# Clone the repo
git clone http://github.com/professordiogodev/devops.flaskerino
cd devops.flaskerino

# install venv on ubuntu if not available
sudo apt update
sudo apt install python3.12-venv -y

# Create a python virtual environment and activate it
python3 -m venv venv
source ./venv/bin/activate

# Install the packages
pip install -r requirements.txt

# Define variables
export DESIRED_PATH="/"
export PORT=4444
export NUMBER=50

# Run the server
python3 app.py
```
