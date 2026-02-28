# Soccer Facility Lease Finder

An interactive Dash web application for evaluating and comparing potential indoor soccer facility lease locations in the **Baltimore / Timonium, MD** area.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Dash](https://img.shields.io/badge/Dash-2.17%2B-informational)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

| Feature | Description |
|---|---|
| **Interactive Map** | Plotly Scattermapbox centered on Timonium, MD with color-coded, size-scaled markers |
| **Status Colors** | Green = Active · Yellow = Under Review · Red = Rejected · Gray = Pending |
| **Sidebar Filters** | Filter by status, square footage range, monthly rent range, and lease type |
| **CSV Upload** | Load your own location data; app falls back to 10 sample properties |
| **Detail Panel** | Full property card with editable 1–5 scores and a live radar chart |
| **Summary Table** | Sortable DataTable of all filtered locations with the selected row highlighted |
| **Dark Theme** | Dash Bootstrap Components `DARKLY` theme throughout |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/gharding6/Soccer-Facilities.git
cd Soccer-Facilities
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open your browser to **http://127.0.0.1:8050**

---

## CSV Data Format

Upload a CSV with the following columns to replace the sample data:

| Column | Type | Example |
|---|---|---|
| `name` | string | Timonium Commerce Center |
| `address` | string | 2000 W Padonia Rd |
| `city` | string | Timonium |
| `state` | string | MD |
| `zip` | string | 21093 |
| `lat` | float | 39.4523 |
| `lon` | float | -76.6213 |
| `square_footage` | int | 42000 |
| `monthly_rent` | int | 28000 |
| `asking_price` | int | 336000 |
| `lease_type` | string | NNN \| Gross \| Modified |
| `year_built` | int | 1998 |
| `parking_spaces` | int | 180 |
| `ceiling_height_ft` | int | 32 |
| `status` | string | Active \| Under Review \| Rejected \| Pending |

---

## Project Structure

```
Soccer-Facilities/
├── app.py              # Single-file Dash application
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

---

## Deployment

The app exposes `server = app.server` for WSGI deployment. Example with Gunicorn:

```bash
gunicorn app:server -b 0.0.0.0:8050 --workers 2
```

---

## Tech Stack

- **[Dash](https://dash.plotly.com/)** — Python web framework for interactive apps
- **[Plotly](https://plotly.com/python/)** — Interactive charts and maps
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)** — Bootstrap-based UI components
- **[Pandas](https://pandas.pydata.org/)** — Data manipulation

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
