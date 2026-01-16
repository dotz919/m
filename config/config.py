# Copyright (C) 2024-2025 by TheTeamVivek.
# ZeebMusic Config File

import os as _os
import re as _re
import sys as _sys

import dotenv as _dotenv
from pyrogram import filters as _flt

_dotenv.load_dotenv()


def is_bool(value: str) -> bool:
    return str(value).lower() in ["true", "yes"]


def parse_list(text: str, sep: str = ",") -> list[str]:
    if not text:
        text = ""
    return [v.strip() for v in str(text).strip("'\"").split(sep) if v.strip()]


def getenv(key, default=None):
    value = default
    if v := _os.getenv(key):
        value = v
    return value


# ===========================
# 🔰 REQUIRED VARIABLES
# ===========================

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_DB_URI = getenv("MONGO_DB_URI", None)

COOKIE_LINK = parse_list(getenv("COOKIE_LINK", ""))

CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "300"))

EXTRA_PLUGINS = is_bool(getenv("EXTRA_PLUGINS", "False"))

EXTRA_PLUGINS_REPO = getenv(
    "EXTRA_PLUGINS_REPO",
    "https://github.com/ZeebFly/Extra-Plugin",
)

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "90"))

LOG_GROUP_ID = getenv("LOG_GROUP_ID", "").strip()

OWNER_ID = list(map(int, getenv("OWNER_ID", "1004345600").split()))

HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/ZeebFly/ZeebMusicBot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

GIT_TOKEN = getenv("GIT_TOKEN", "")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dotzstorereall")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/infernalsexhot")

AUTO_LEAVING_ASSISTANT = is_bool(getenv("AUTO_LEAVING_ASSISTANT", "False"))

AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", 5800))

PRIVATE_BOT_MODE = is_bool(getenv("PRIVATE_BOT_MODE", "False"))

YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "3"))
TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", "5"))

GITHUB_REPO = getenv("GITHUB_REPO", "https://github.com/BENDOTZ/JANGANMALING")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "19609edb1b9f4ed7be0c8c1342039362")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "409e31d3ddd64af08cfcc3b0f064fcbe"
)

VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "999"))
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "25"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "1073741824"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))

SET_CMDS = is_bool(getenv("SET_CMDS", "False"))

STRING_SESSIONS = parse_list(getenv("STRING_SESSIONS", ""))

# ====================================================
# 🔥 MUST_JOIN FIX — DITAMBAHKAN DI SINI
# ====================================================

# Channel/group yang wajib user join sebelum menggunakan bot
# Isi dengan username / ID → contoh: "-1001234567890" atau "mychannel"
# Bisa juga dikosongkan None jika tidak digunakan (auto nonaktif)
MUST_JOIN = getenv("MUST_JOIN", None)

# ====================================================
# ⚠️ JANGAN EDIT KODE DI BAWAH INI
# ====================================================

BANNED_USERS = _flt.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "logs.txt"
adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

# Images

START_IMG_URL = getenv("START_IMG_URL", "https://te.legra.ph/file/4ec5ae4381dffb039b4ef.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/91533956c91d0fd7c9f20.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://envs.sh/W_z.jpg")
GLOBAL_IMG_URL = getenv("GLOBAL_IMG_URL", "https://telegra.ph/file/de1db74efac1770b1e8e9.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/4dd9e2c231eaf7c290404.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://envs.sh/npk.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/8d02ff3bde400e465219a.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://envs.sh/nAw.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://envs.sh/nAD.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://envs.sh/npl.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://envs.sh/nA9.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://envs.sh/nps.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/f4edfbd83ec3150284aae.jpg")


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def seconds_to_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if LOG_GROUP_ID.lstrip("-").isdigit():
    LOG_GROUP_ID = int(LOG_GROUP_ID)

# URL validations
checks = {
    "SUPPORT_CHANNEL": SUPPORT_CHANNEL,
    "SUPPORT_GROUP": SUPPORT_GROUP,
    "UPSTREAM_REPO": UPSTREAM_REPO,
    "GITHUB_REPO": GITHUB_REPO,
    "PING_IMG_URL": PING_IMG_URL,
    "PLAYLIST_IMG_URL": PLAYLIST_IMG_URL,
    "GLOBAL_IMG_URL": GLOBAL_IMG_URL,
    "STATS_IMG_URL": STATS_IMG_URL,
    "TELEGRAM_AUDIO_URL": TELEGRAM_AUDIO_URL,
    "STREAM_IMG_URL": STREAM_IMG_URL,
    "SOUNCLOUD_IMG_URL": SOUNCLOUD_IMG_URL,
    "YOUTUBE_IMG_URL": YOUTUBE_IMG_URL,
    "TELEGRAM_VIDEO_URL": TELEGRAM_VIDEO_URL,
}

for k, v in checks.items():
    if v and not _re.match("(?:http|https)://", v):
        print(f"[ERROR] - Your {k} url is wrong. Please ensure that it starts with https://")
        _sys.exit()
