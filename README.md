# Earthquake Prediction System

This project consists of a server and a frontend application for earthquake prediction.

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/earthquake-pred.git
cd earthquake-pred
```

### 2. Backend (Server)

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. make a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv

   # now activate virtual env
   source venv/bin/activate

   #install dependencies
   pip install <library_name>
   ```

3. Run the server:

   ```bash
   python server.py
   ```

   The server will start at `http://127.0.0.1:8000`.

### 3. Frontend

1. Navigate to the `frontend` directory:

   ```bash
   cd ../frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the frontend:

   ```bash
   npm run dev
   ```

   The frontend will start at `http://localhost:3000`.

## Usage

1. Start the server and frontend as described above.
2. Open your browser and navigate to `http://localhost:3000`.
3. Use the application to interact with the earthquake prediction system.

## Project Structure

```
earthquake-pred/
├── server/       # Backend server code
├── frontend/     # Frontend application code
├── model/        # training model .ipynb files
└── README.md     # Project documentation
```

## License

This project is licensed under the MIT License.
