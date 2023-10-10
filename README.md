# Face-Attendance-System BY FAB4

This repository contains the code for the IMG-API project.

## Running the Front-End

To run the front-end of the project, follow these steps:

1. Open Face-Attendance-System directory in Your IDE

2. Navigate to the Client directory :-> `cd Client/`

3. Install the required dependencies by running :-> `npm install`

4. Start the front-end development server :-> `npm start`

This will start the development server and open the project in your default web browser.

## Running the Model and Back-end

1. Create a virtual env :-> `conda create -p venv python -y`
2. Activate venv :-> `conda activate ./venv`
3. Install the requirments.txt file :-> `pip install -r requirements.txt`
4. run app.py on port 2000 :-> `uvicorn app:app --host 0.0.0.0 --port 2000`

This will start models and back-ends api on port 2000

## Ignored Files and Directories

The following files and directories are ignored by Git and should not be pushed to the repository:

- `.vscode/`
- `__pycache__/`
- `venv/`
- `Client/node_modules/`
- `credentials.json`

Make sure to keep these files and directories out of version control.





