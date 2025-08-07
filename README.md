# My Streamlit App

This project is a Streamlit application that demonstrates the use of clickable widgets. It provides an interactive interface for users to engage with various features.

## Project Structure

```
my-streamlit-app
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   └── widgets
│       └── clickable.py # Contains functions for creating clickable widgets
├── requirements.txt    # Lists the required Python packages
└── README.md           # Documentation for the project
```

## Prerequisites

Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd my-streamlit-app
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Running the App

To run the Streamlit application, execute the following command:

```
streamlit run src/app.py
```

This will start the Streamlit server and open the app in your default web browser.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.