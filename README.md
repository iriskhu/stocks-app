# stocks-app

# Stock Recommendation App
A command-line Python application which processes user inputs and stock market data from the [AlphaVantage API](https://www.alphavantage.co) to provide stock purchase recommendations.

## Installation

First, "fork" this upstream repository under your own control.

Then download your forked version of this repository using the GitHub.com online interface or the Git command-line interface. If you are using command-line Git, you can download it by "cloning" it:

```sh
git clone https://github.com/YOUR_USERNAME/stocks-app-py.git
```

After downloading your forked repository, navigate into its root directory:

```sh
cd stocks-app-py/
```

> NOTE: all commands in this document assume you are running them from this root directory.

Install package dependencies using one of the following commands, depending on how you have installed Python and how you are managing packages:

```sh
# Pipenv on Mac or Windows:
pipenv install -r requirements.txt

# Homebrew-installed Python 3.x on Mac OS:
pip3 install -r requirements.txt

# All others:
pip install -r requirements.txt
```

If you are using Pipenv, enter a new virtual environment (`pipenv shell`) before running any of the commands below.

All commands below assume you are running them from this repository's root directory.

## Setup

### Environment Variables

Obtain an [AlphaVantage API Key](https://www.alphavantage.co/support/#api-key), which the app will supply when issuing requests to the API.

To prevent your secret API Key from being tracked in version control, the application looks for an environment variable named `ALPHAVANTAGE_API_KEY`. To set this environment variable, create a new file in this directory called ".env" and place inside the following contents:

    ALPHAVANTAGE_API_KEY="abc123" # use your own API Key instead of "abc123"

### CSV File

Before running the application for the first time, setup a CSV file to store historical price data:

```sh
# Homebrew-installed Python 3.x on Mac OS:
python3 app/prepare.py

# All others:
python app/prepare.py
```

## Usage

Run the recommendation script:

```sh
# Homebrew-installed Python 3.x on Mac OS:
python3 app/robo_adviser.py

# All others:
python app/robo_adviser.py
```

## Testing

Run tests:

```sh
pytest
```

## [License](LICENSE.md)
