# Deployment Instructions for Render

This project is configured to be deployed on [Render](https://render.com/) as a **Web Service**.

## Prerequisites

1.  A GitHub account with this repository pushed to it.
2.  A Render account.

## Step-by-Step Deployment

1.  **Log in to Render**: Go to [dashboard.render.com](https://dashboard.render.com/).
2.  **Create a New Web Service**:
    *   Click the **New +** button and select **Web Service**.
    *   Connect your GitHub account and select this repository.
3.  **Configure the Service**:
    *   **Name**: `health-clinic` (or your preferred name).
    *   **Region**: Select the region closest to you.
    *   **Branch**: `main` (or your default branch).
    *   **Root Directory**: Leave blank (unless your project is in a subdirectory).
    *   **Runtime**: **Python 3**.
    *   **Build Command**: `./build.sh`
    *   **Start Command**: `gunicorn health_clinic.wsgi:application`
4.  **Instance Type**:
    *   Select **Free** (or your preferred plan).
5.  **Deploy**:
    *   Click **Create Web Service**.

## Important Note on SQLite

Since we are using **SQLite** (a file-based database) on Render's ephemeral filesystem:
*   **Data Persistence**: If your Web Service restarts or is redeployed, **the database will be reset**, and you will lose all data (users, patients, appointments).
*   **Testing**: This setup is perfect for testing and demos.
*   **Production**: For a real production app, you should provision a managed PostgreSQL database on Render.

## Manual Build/Migration (If needed)

The build script `build.sh` handles migrations and static files automatically. If you ever need to run migrations manually, you can use the Render Shell:

```bash
python manage.py migrate
```

## Creating a Superuser

After deployment, you'll need to create a superuser to access the admin panel:

1.  Go to the **Web Service** dashboard.
2.  Click on the **Shell** tab (available once the service is Live).
3.  Run the following command:
    ```bash
    python manage.py createsuperuser
    ```
4.  Follow the prompts to set your username and password.
