import time
import schedule

from updater import update_knowledge_base


# ============================================================
# AUTOMATIC KNOWLEDGE BASE UPDATER
# ============================================================

def run_update():
    print()
    print("==========================================")
    print(" Automatic Knowledge Base Check")
    print("==========================================")

    try:
        update_knowledge_base()

    except Exception as error:
        print()
        print("Update error:")
        print(error)


# ============================================================
# SCHEDULE
# ============================================================

# For testing:
# Check for new information every 1 minute

schedule.every(1).minutes.do(run_update)


# For the final project, you can change it to:
#
# schedule.every(1).hour.do(run_update)
#
# or:
#
# schedule.every(6).hours.do(run_update)


print()
print("==========================================")
print(" Dynamic Knowledge Base Scheduler")
print("==========================================")
print()
print("Automatic update checking is active.")
print("Checking for new information every 1 minute.")
print()
print("Press CTRL + C to stop the scheduler.")
print()


# ============================================================
# RUN CONTINUOUSLY
# ============================================================

# Run once immediately
run_update()


while True:

    schedule.run_pending()

    time.sleep(10)