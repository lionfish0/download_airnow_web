# download_airnow_web
This python tool downloads pollutation values from the https://www.airnow.gov/ website. This doesn't use their API. It caches the data locally and just downloads the current month's data (except at month boundaries when it re-downloads everything to keep the cache fresh, this could be improved).
