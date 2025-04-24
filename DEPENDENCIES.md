# External Dependencies and Setup Instructions

## ⚙️ Setup Requirements

Before you can run this ETL pipeline, ensure you have the following set up:

### 1. **PostgreSQL**
   - Install PostgreSQL and ensure it's running (locally or on a server).
   - Create a database to store the financial data.

### 2. **Simply Wall St API Access**
   - You need access to the Simply Wall St API (paid subscription required).
   - Obtain your API key from [Simply Wall St](https://simplywall.st/).

### 3. **Environment Variables**
   - Set up a `.env` file or use environment variables for sensitive data such as:
     - Simply Wall St API key
     - PostgreSQL database credentials (username, password, host, port)

   Example `.env` file:
   ```env
   SWS_API_KEY=your_api_key_here
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_db_name

### 4. **Python**
   Recommended: Python 3.10+ to ensure compatibility with dependencies.
