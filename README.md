Energy Imbalance Report Project
===============================

Overview
--------

This project generates daily reports of system imbalance costs and prices using data from the Elexon Insights API (BMRS). It provides a Flask-based API with endpoints for retrieving daily imbalance statistics, identifying the hour with the highest absolute imbalance volumes, and generating comprehensive PDF reports.

Features
--------

-   Data retrieval from Elexon BMRS API
-   Daily imbalance cost and unit rate calculation
-   Identification of the hour with highest absolute imbalance volumes
-   PDF report generation with data visualisations
-   RESTful API endpoints for accessing processed data and reports

Technology Stack
----------------

-   Python 3.12+
-   Flask and Flask-RESTful for API development
-   Matplotlib for data visualization
-   ReportLab for PDF generation
-   Pytest for unit testing

Installation
------------

1.  Clone the repository:

    `git clone https://github.com/PRJM1999/bmrs-data-report.git`

2.  Create and activate a virtual environment:

    `python -m venv venv
    source venv/bin/activate`
    
    # On Windows, use `venv\Scripts\activate`

3.  Install the required packages:

    `pip install -r requirements.txt`

Usage
-----

To start the Flask server:

`python run.py`

The server will start on `http://localhost:3000` by default.


### API Endpoints

1.  **Daily Imbalance**: `/daily_imbalance`
    -   Returns the total daily imbalance cost and daily imbalance unit rate for the previous day.
2.  **Highest Imbalance Hour**: `/highest_imbalance_hour`
    -   Reports which hour had the highest absolute imbalance volumes for the previous day.
3.  **Energy Report**: `/energy_report`
    -   Generates and returns a PDF report with energy data visualizations.

Testing
-------

Run the unit tests using pytest:

`pytest`

Design Patterns and Architecture
--------------------------------

### Data Retrieval

The project uses the template pattern for data retrieval, implemented through the `EnergyDataFetcher` abstract base class and its concrete implementation `ElexonBrmsFetcher`. This design allows for easy extension to support additional data sources in the future without modifying existing code, adhering to the Open/Closed Principle.

### Data-Oriented vs. Behavior-Oriented Code

The project separates data structures (`data_objects.py`) from behavior (`energy_calc.py`, `report_generation.py`). This separation enhances maintainability and allows for clearer testing and modification of business logic.

### Use of Data Classes

Data classes (`EnergyDataPoint`, `EnergyDataObject`) are used to represent the core data structures. This approach provides a clean, readable way to define data containers with less boilerplate code.

Known Issues
------------

-   On some macOS machines, the ReportLab library may not appear as installed. This is a known issue with certain Python installations on macOS. If encountered, try reinstalling ReportLab or using a different Python environment.

Issues I didn't complete due to time constraints
-------------------

-   Enhance test coverage, particularly for API endpoints using mock objects.
-   Add more sophisticated error handling and retry mechanisms for API requests.
-   Create a web frontend using react for easier interaction with the API and visualization of reports.