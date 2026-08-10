from checkpoint import save_checkpoint


def planner(workflow_id):

    print("Planner Node Running...")

    save_checkpoint(
        workflow_id,
        1,
        "Planner",
        {
            "task": "Generate Report",
            "progress": "25%"
        },
        "Running",
        "GPT-4",
        0.0,
        ""
    )


def data_fetcher(workflow_id):

    print("Data Fetcher Node Running...")

    save_checkpoint(
        workflow_id,
        2,
        "Data Fetcher",
        {
            "task": "Generate Report",
            "progress": "50%"
        },
        "Running",
        "GPT-4",
        0.1,
        ""
    )


def synthesis(workflow_id):

    print("Synthesis Node Running...")

    save_checkpoint(
        workflow_id,
        3,
        "Synthesis",
        {
            "task": "Generate Report",
            "progress": "75%"
        },
        "Running",
        "GPT-4",
        0.2,
        ""
    )


def formatter(workflow_id):

    print("Formatter Node Running...")

    save_checkpoint(
        workflow_id,
        4,
        "Formatter",
        {
            "task": "Generate Report",
            "progress": "100%"
        },
        "Completed",
        "GPT-4",
        0.0,
        ""
    )

    print("Workflow Completed Successfully!")