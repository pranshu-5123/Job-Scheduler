import json
from scheduler import AdvancedJobScheduler
from models import Frequency


def main_menu(scheduler: AdvancedJobScheduler):
    while True:
        print("\nScheduler Menu:")
        print("1. Add a new job")
        print("2. Remove a job")
        print("3. View all jobs")
        print("4. Start the scheduler")
        print("5. Stop the scheduler")
        print("6. View job log history")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            job_id = input("Enter job ID: ").strip()
            script_path = input("Enter script path: ").strip()
            frequency = input("Enter frequency (minutely, hourly, daily): ").strip().lower()
            time_str = input("Enter time (HH:MM) or leave blank: ").strip()

            try:
                freq_enum = Frequency[frequency.upper()]
                scheduler.schedule_job(job_id, script_path, freq_enum, time_str if time_str else None)
                print(f"Job {job_id} scheduled successfully.")
            except KeyError:
                print("[ERROR] Invalid frequency. Please enter one of: minutely, hourly, daily.")
            except Exception as e:
                print(f"[ERROR] {e}")

        elif choice == '2':
            job_id = input("Enter the job ID to remove: ").strip()
            try:
                scheduler.remove_job(job_id)
                print(f"Job {job_id} removed successfully.")
            except Exception as e:
                print(f"[ERROR] {e}")

        elif choice == '3':
            jobs = scheduler.list_jobs()
            if not jobs:
                print("\nNo jobs available.")
            else:
                print("\nScheduled Jobs:")
                for job in jobs:
                    print(json.dumps(job, indent=4))


        elif choice == '4':
            scheduler.start()
            print("Scheduler started.")

        elif choice == '5':
            scheduler.stop()
            print("Scheduler stopped.")

        elif choice == '6':
            job_id = input("Enter the job ID to view history: ").strip()
            try:
                job = scheduler.jobs.get(job_id)
                if not job:
                    print("[ERROR] Job not found.")
                    continue

                print(f"\nHistory for Job ID: {job_id}")
                if not job.history:
                    print("No execution history available.")
                for record in job.history:
                    print(json.dumps(record, indent=4))
            except Exception as e:
                print(f"[ERROR] {e}")

        elif choice == '7':
            scheduler.stop()
            print("Exiting...")
            break

        else:
            print("[ERROR] Invalid choice. Please try again.")


def main():
    scheduler = AdvancedJobScheduler()
    print("Welcome to the Advanced Job Scheduler!")
    main_menu(scheduler)


if __name__ == "__main__":
    main()
