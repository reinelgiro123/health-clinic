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
4.  **Database Setup**:
    *   The blueprint will automatically create a PostgreSQL database for you.
    *   The `DATABASE_URL` will be automatically linked to your web service.
5.  **Environment Variables**:
    *   The blueprint automatically generates a `SECRET_KEY`.
    *   If you need to customize other settings (like Email), go to the **Web Service** -> **Environment** tab and add the variables from `.env.example`.

## Environment Variables Example

Add these to your Render Web Service environment if needed:

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
