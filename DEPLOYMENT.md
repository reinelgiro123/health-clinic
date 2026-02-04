# Deployment Instructions for Render

This project is configured to be deployed on [Render](https://render.com/) using a Blueprint (`render.yaml`).

## Prerequisites

1.  A GitHub account with this repository pushed to it.
2.  A Render account.

## Step-by-Step Deployment

1.  **Log in to Render**: Go to [dashboard.render.com](https://dashboard.render.com/).
2.  **Create a New Blueprint**:
    *   Click the **New** button and select **Blueprint**.
    *   Connect your GitHub account and select this repository.
3.  **Configure the Service**:
    *   Render will automatically detect the `render.yaml` file.
    *   Give your blueprint a group name (e.g., `health-clinic-group`).
    *   Click **Apply**.
4.  **Done!**:
    *   Render will build your web service and deploy it.
    *   Since we are using **SQLite**, the database file will be created automatically.
    *   **Note**: On Render's free tier (or without a persistent disk), specific files like the SQLite database will be reset if the service redeploys or restarts. This is fine for testing.

## Environment Variables Example

The `render.yaml` automatically sets up the keys. If you need to override them or add email settings:

| Variable | Description | Default/Example |
| :--- | :--- | :--- |
| `DEBUG` | Set to `False` for production | `False` |
| `ALLOWED_HOSTS` | Your custom domain (if any) | `yourdomain.com` |
| `EMAIL_HOST` | SMTP server for emails | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS for email | `True` |
| `EMAIL_HOST_USER` | Email address | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD`| App password | `your-app-password` |

## Manual Build/Migration (If needed)

The build script `build.sh` handles migrations and static files automatically. If you ever need to run migrations manually, you can use the Render Shell:

```bash
python manage.py migrate
```

## Creating a Superuser

After deployment, you'll need to create a superuser to access the admin panel:

1.  Go to the **Web Service** in your Render dashboard.
2.  Click on the **Shell** tab.
3.  Run the following command:
    ```bash
    python manage.py createsuperuser
    ```
4.  Follow the prompts to set your username and password.
