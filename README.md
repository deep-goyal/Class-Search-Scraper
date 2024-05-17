# Open Spot Notifier

## Description

This project aims to automate the process of checking for open spots in
a specific class at Arizona State University. When an open spot is found,
the system instantly sends a notification to a designated discord channel.

## Installation

Clone the repository

```bash
git clone https://github.com/deep-goyal/open-spot-notifier.git
```

## Setup

1. Create a python virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the environment:

   ```bash
   source ./venv/bin/activate
   ```

3. Install the required dependencies by running:

   ```bash
   pip install requests
   pip install discord
   pip install selenium
   pip install webdriver_manager
   ```

4. Update the following constants in the `script.py` file:

   - `TOKEN`: Your Discord bot token
   - `CHANNEL_ID`: ID of the Discord channel to send notifications
   - `TERM_VAL`: Term value for the class (found in URL)
   - `SUBJECT`: First three characters of the class
   - `CLASS_NUM`: Last three numbers of the class

## Usage

To run the script and receive notifications about open spots in the class, execute the `script.py` file by running:

```bash
python script.py
```

## Notes

This project presents two ways to search for open seats.

1. `api_search()` uses ASU's catalog API to retrieve the number of spots, and while it is faster than scraping the webpage DOM, it produces incorrect info for bigger classes.
2. `webpage_search()` scrapes the DOM to get the number of spots, and it is 100% accurate for all classes. The only downside is that the driver setup takes significant time before actually scraping the DOM.

## Contributing

This project is in its rudimentary stage and can really use some help to be perfect. To contribute:

1. Fork the repository.

2. Create a new branch.

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m 'Add new feature'
   ```

4. Push to the branch:

   ```bash
   git push origin feature-name
   ```

5. Submit a pull request.

## License

Distributed under the MIT License. See `License.txt` for more information.
