from checkpoint import load_checkpoint
from workflow import planner, data_fetcher, synthesis, formatter

workflow_id = "A101"

checkpoint = load_checkpoint(workflow_id)

if checkpoint is None:

    print("Starting New Workflow")

    planner(workflow_id)
    data_fetcher(workflow_id)
    synthesis(workflow_id)
    formatter(workflow_id)

else:

    print("Recovering Previous Workflow...")

    step = checkpoint["current_step"]

    if step == 1:
        print("Resuming from Data Fetcher")
        data_fetcher(workflow_id)
        synthesis(workflow_id)
        formatter(workflow_id)

    elif step == 2:
        print("Resuming from Synthesis")
        synthesis(workflow_id)
        formatter(workflow_id)

    elif step == 3:
        print("Resuming from Formatter")
        formatter(workflow_id)

    elif step == 4:
        print("Workflow Already Completed")