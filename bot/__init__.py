from uvloop import install

install()
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import Lock, new_event_loop, set_event_loop
import sys
from logging import (
    getLogger,
    FileHandler,
    StreamHandler,
    INFO,
    basicConfig,
    WARNING,
    ERROR,
    Formatter,
)
from sabnzbdapi import SabnzbdClient
from time import time
from os import cpu_count, path, remove

getLogger("requests").setLevel(WARNING)
getLogger("urllib3").setLevel(WARNING)
getLogger("pyrogram").setLevel(ERROR)
getLogger("httpx").setLevel(WARNING)
getLogger("pymongo").setLevel(WARNING)
getLogger("aiohttp").setLevel(WARNING)

bot_start_time = time()

bot_loop = new_event_loop()
set_event_loop(bot_loop)

err_handler = FileHandler("error.log", delay=True)
err_handler.setLevel(ERROR)
err_handler.setFormatter(
    Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[FileHandler("log.txt"), StreamHandler(), err_handler],
    level=INFO,
)

LOGGER = getLogger(__name__)


def uncaught_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    LOGGER.error("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = uncaught_exception_handler
cpu_no = cpu_count()
threads = max(1, cpu_no // 2)
cores = ",".join(str(i) for i in reversed(range(threads)))

DOWNLOAD_DIR = f"{path.abspath('.')}/downloads/"
intervals = {"status": {}, "qb": "", "jd": "", "nzb": "", "stopAll": False}
qb_torrents = {}
jd_downloads = {}
nzb_jobs = {}
user_data = {}
aria2_options = {}
qbit_options = {}
nzb_options = {}
queued_dl = {}
queued_up = {}
status_dict = {}
task_dict = {}
rss_dict = {}
auth_chats = {}
excluded_extensions = ["aria2", "!qB"]
included_extensions = []
drives_names = []
drives_ids = []
index_urls = []
sudo_users = []
non_queued_dl = set()
non_queued_up = set()
multi_tags = {}
task_dict_lock = Lock()
queue_dict_lock = Lock()
qb_listener_lock = Lock()
nzb_listener_lock = Lock()
jd_listener_lock = Lock()
cpu_eater_lock = Lock()
same_directory_lock = Lock()

sabnzbd_client = SabnzbdClient(
    host="http://localhost",
    api_key="mltb",
    port="8070",
)

scheduler = AsyncIOScheduler(event_loop=bot_loop)
