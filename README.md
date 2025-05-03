# 🕒 Job Scheduler 

A custom-built, Python-based job scheduler that mimics the functionality of Linux's `cron` system. It allows users to schedule and manage scripts to run at regular intervals — **minutely, hourly, or daily** — with CLI interaction and persistent job storage. 
---

## 🚀 Features

- ✅ Add, remove, and list scheduled jobs  
- ⏱️ Supports frequencies: minutely, hourly, and daily (with `HH:MM` time support)  
- 📜 Execution logging with history tracking  
- 🧩 Runs both `.py` and `.sh` scripts  
- 🗂️ Job persistence using JSON file  
- 🐳 Dockerized for cross-platform deployment  
- 🧪 Input validations and structured error handling  
- 📄 Log file output for execution trace  

---

## 🗂️ Project Structure

```
├── main.py # CLI interface for interacting with scheduler
├── models.py # Data models for Job, Frequency, and Status enums
├── scheduler.py # Core logic for scheduling, execution, and logging
├── utilities.py # Utility functions for path/time validation and logging setup
├── jobs.json # Persistent storage for scheduled jobs
├── Dockerfile # Docker container setup
└── README.md # Project documentation
```
---


## ⚙️ How It Works
```
1. Launch the app with: python main.py
2.Use the CLI menu to:
   • Add a new job
   • Remove or view existing jobs
   • Start or stop the scheduler
   • View job execution history
 3.Supported script types:
   • Python: script. py
   • Shell: script. sh
 4.Execution logs are saved to:
   • Console
   • scheduler. log file
   • Individual <job_id>_history.log files
```
---
## 📦 Requirements
- Python 3.7+
- schedule Python package
- Install it using:

```
pip install schedule
```
## 🤝 Contributing
Pull requests and improvements are welcome. Please fork the repository and submit a PR with clear documentation.

## 📄 License
This project is licensed under the MIT License.

