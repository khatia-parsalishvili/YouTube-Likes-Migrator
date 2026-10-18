# YouTube Likes Migrator 🎵

A Python automation script that seamlessly transfers your "Liked Videos" from one YouTube account to another. 

Since YouTube removed the native "Add all to..." feature for the automatically generated, private "Liked videos" playlist, migrating liked music or videos between accounts manually is extremely tedious. This script uses the **YouTube Data API v3** to automate the process by reading the liked videos from a source account and automatically populating them into a new, private playlist on a destination account.

## Features
* **Automated Migration:** Fetches all liked videos from the source account (handling API pagination automatically).
* **Cross-Account Transfer:** Creates a brand new, private playlist on the destination (e.g., Premium) account.
* **Order Preservation:** Reverses the fetched list so that the oldest liked videos are added first, preserving your original chronological order.
* **Error Handling:** Gracefully skips videos that might have been deleted or made private by their original uploaders.

## Prerequisites
* Python 3.x installed on your machine.
* A Google Cloud Console account to generate OAuth 2.0 credentials.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YouTube-Likes-Migrator.git
   cd YouTube-Likes-Migrator
   ```

2. **Install required libraries:**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

3. **Get YouTube Data API Credentials:**
   * Go to the [Google Cloud Console](https://console.cloud.google.com/).
   * Create a New Project and enable the **YouTube Data API v3**.
   * Configure the **OAuth consent screen** (Set to "External", give it a generic app name, and add your YouTube email addresses to the "Test users" section to avoid 403 errors).
   * Go to **Credentials** -> Create Credentials -> **OAuth client ID**.
   * Choose **Desktop app** as the application type.
   * Download the generated JSON file, rename it to exactly `client_secret.json`, and place it in the same directory as the script.

## Usage

Run the script from your terminal:

```bash
python transfer_likes.py
```

1. A browser window will open. Log in with your **Source Account** (the old account where your likes currently reside) and grant permission.
2. The script will fetch all your liked videos.
3. Another browser window will open (or you will be prompted). Log in with your **Destination Account** (the new/Premium account) and grant permission.
4. The script will create a new private playlist named "My Transferred Likes" on the destination account and add all your videos to it.

## Security Warning ⚠️
**Never share or commit your `client_secret.json` or generated `token_old.json` / `token_new.json` files!** 
These files contain your private authorization tokens. This repository includes them in the `.gitignore` file to prevent accidental uploads.

## Technologies Used
* Python
* YouTube Data API v3
* Google OAuth 2.0