# OrgVisualisation
Interactive D3.js circle-packing visualisation of Porsche Digital org chart, backed by a Python script that converts HR-style employee data into a hierarchy.
This Repository is to explore the feasibility of visualising the Organisation using the Data from Leapsome



## 1. Prerequisites

- Python 3.6 or newer (for the script and local server) 
- pip (Python package manager, usually included with Python) 

Check your Python version:

```bash
python --version
```

If your system uses `python3` instead, run:

```bash
python3 --version
```

## 2. Project structure

Place these files in the root directory:

```text
  employees_hris.json        # flat HR-style employee data
```

## 3. Install Python dependencies

Only `pandas` is required.

```bash
pip install pandas
```

If your system uses `pip3`:

```bash
pip3 install pandas
```

This installs pandas from PyPI. 

## 4. Prepare the data

1. The `employees_hris.json`  should have the following structure for each Employee and follow HRIS.
{
    "employee_id": "1000",
    "first_name": "Alice",
    "last_name": "Schmidt",
    "work_email": "alice.schmidt@example.com",
    "work_phone": "+49-30-100001",
    "location": "Berlin",
    "manager_id": null,
    "department": "Corporate",
    "job_title": "CEO"
  }

2. Run the Python script to build the hierarchical JSON:

   ```bash
   python build_from_hris.py
   ```

   or, if needed:

   ```bash
   python3 build_from_hris.py
   ```

   This creates / overwrites `employees_hierarchy.json`, which is what D3 loads.

## 5. Start a local web server

Use Python’s built-in HTTP server to serve `index.html` and the JSON files. 

From the root directory of the project:

```bash
python -m http.server 8000
```

(Use `python3 -m http.server 8000` if `python` is Python 2 on your machine.)

You should see something like:

```text
Serving HTTP on :: port 8000 (http://0.0.0.0:8000/) ...
```

## 6. View the visualisation

1. Open your browser and go to:

   ```text
   http://localhost:8000/index.html
   ```

2. Interactions:

   - Click a circle to zoom into that manager’s team.
   - Click the background to zoom back out to the CEO level.
   - Hover over any circle to see a tooltip with:
     - Employee name
     - Role
     - Email
     - Phone number

## 7. Stopping the server

When you are done, return to the terminal where `python -m http.server` is running and press:

```text
Ctrl + C
```

This stops the local server. 
