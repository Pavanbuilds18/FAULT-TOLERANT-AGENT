from checkpoint import (
    load_checkpoint,
    create_workflow,
    get_workflow_history,
    get_checkpoint_history,
    get_workflow
)

from workflow import planner, data_fetcher, synthesis, formatter

def start_new_workflow(workflow_id):

    print("\nStarting New Workflow...")

    planner(workflow_id)
    data_fetcher(workflow_id)
    synthesis(workflow_id)
    formatter(workflow_id)


def resume_workflow(workflow_id):

    checkpoint = load_checkpoint(workflow_id)

    if checkpoint is None:

        print("Workflow Not Found")
        return

    print("\nRecovering Previous Workflow...")

    step = checkpoint["current_step"]
    status = checkpoint["status"]

    print("Current Step:", step)
    print("Current Node:", checkpoint["current_node"])
    print("Status:", status)

    if status == "Completed":

        print("Workflow Already Completed")
        return

    if step == 1:

        print("Resuming from Planner")

        planner(workflow_id)
        data_fetcher(workflow_id)
        synthesis(workflow_id)
        formatter(workflow_id)

    elif step == 2:

        print("Resuming from Data Fetcher")

        data_fetcher(workflow_id)
        synthesis(workflow_id)
        formatter(workflow_id)

    elif step == 3:

        print("Resuming from Synthesis")

        synthesis(workflow_id)
        formatter(workflow_id)

    elif step == 4:

        print("Resuming from Formatter")

        formatter(workflow_id)

    else:

        print("Invalid workflow step:", step)


def create_new_order():

    user_id = input("\nEnter User ID: ")

    order_text = input("\nWhat would you like me to do? ")

    workflow_id = create_workflow(user_id, order_text)

    start_new_workflow(workflow_id)

    print("\nWorkflow ID:", workflow_id)

def show_previous_orders():

    user_id = input("\nEnter User ID: ")

    print("\n===== PREVIOUS ORDERS =====")

    history = get_workflow_history(user_id)

    if not history:

        print("No previous workflows found.")
        return

    for index, workflow in enumerate(history, start=1):

        workflow_id = workflow[0]
        order_text = workflow[1]
        status = workflow[2]
        updated_at = workflow[3]

        print(f"\n{index}. {order_text}")
        print(f"   Workflow ID: {workflow_id}")
        print(f"   Status: {status}")
        print(f"   Last Updated: {updated_at}")


def show_workflow_details():

    workflow_id = input("\nEnter Workflow ID: ")

    workflow = get_workflow(workflow_id)

    if workflow is None:

        print("Workflow Not Found")
        return

    print("\n===== WORKFLOW DETAILS =====")

    print("Workflow ID:", workflow[0])
    print("Order:", workflow[1])
    print("Current Step:", workflow[2])
    print("Current Node:", workflow[3])
    print("State:", workflow[4])
    print("Status:", workflow[5])
    print("Updated At:", workflow[6])

    print("\n===== CHECKPOINT HISTORY =====")

    history = get_checkpoint_history(workflow_id)

    for step in history:

        print(
            f"Step {step[0]} | "
            f"Node: {step[1]} | "
            f"Status: {step[3]}"
        )


def main():

    while True:

        print("\n")
        print("================================")
        print("       WORKFLOW SYSTEM")
        print("================================")

        print("1. Create New Order")
        print("2. View Previous Orders")
        print("3. View Workflow Details")
        print("4. Resume Workflow")
        print("5. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":

            create_new_order()

        elif choice == "2":

            show_previous_orders()

        elif choice == "3":

            show_workflow_details()

        elif choice == "4":

            workflow_id = input("\nEnter Workflow ID to resume: ")

            resume_workflow(workflow_id)

        elif choice == "5":

            print("Exiting...")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    main()