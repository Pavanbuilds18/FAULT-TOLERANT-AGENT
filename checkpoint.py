import psycopg2
import json
import os
import uuid
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )


# ============================================================
# CREATE WORKFLOW
# ============================================================

def create_workflow(user_id, order_text):

    workflow_id = str(uuid.uuid4())

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO workflows
    (
        workflow_id,
        user_id,
        order_text
    )
    VALUES (%s, %s, %s);
    """

    cursor.execute(
        query,
        (
            workflow_id,
            user_id,
            order_text
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Workflow Created Successfully!")
    print("Workflow ID:", workflow_id)

    return workflow_id


# ============================================================
# SAVE CHECKPOINT
# ============================================================

def save_checkpoint(
    workflow_id,
    current_step,
    current_node,
    state,
    status,
    active_model,
    loop_score,
    error_logs
):

    connection = get_connection()
    cursor = connection.cursor()

    # Find user who owns this workflow

    cursor.execute(
        """
        SELECT user_id
        FROM workflows
        WHERE workflow_id = %s;
        """,
        (workflow_id,)
    )

    workflow_user = cursor.fetchone()

    if workflow_user is None:

        cursor.close()
        connection.close()

        raise Exception(
            "Workflow does not exist: " + workflow_id
        )

    user_id = workflow_user[0]

    # --------------------------------------------------------
    # SAVE CURRENT CHECKPOINT
    # --------------------------------------------------------

    checkpoint_query = """
    INSERT INTO checkpoints
    (
        workflow_id,
        current_step,
        current_node,
        state,
        status,
        active_model,
        loop_score,
        error_logs,
        user_id
    )

    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

    ON CONFLICT (workflow_id)
    DO UPDATE SET

        current_step = EXCLUDED.current_step,
        current_node = EXCLUDED.current_node,
        state = EXCLUDED.state,
        status = EXCLUDED.status,
        active_model = EXCLUDED.active_model,
        loop_score = EXCLUDED.loop_score,
        error_logs = EXCLUDED.error_logs,
        user_id = EXCLUDED.user_id,
        updated_at = CURRENT_TIMESTAMP;
    """

    cursor.execute(
        checkpoint_query,
        (
            workflow_id,
            current_step,
            current_node,
            json.dumps(state),
            status,
            active_model,
            loop_score,
            error_logs,
            user_id
        )
    )

    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history_query = """
    INSERT INTO workflow_history
    (
        workflow_id,
        step_number,
        node_name,
        state,
        status,
        error_logs
    )

    VALUES (%s, %s, %s, %s, %s, %s);
    """

    cursor.execute(
        history_query,
        (
            workflow_id,
            current_step,
            current_node,
            json.dumps(state),
            status,
            error_logs
        )
    )

    connection.commit()

    print("Checkpoint Saved Successfully!")

    cursor.close()
    connection.close()


# ============================================================
# LOAD CHECKPOINT
# ============================================================

def load_checkpoint(workflow_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        workflow_id,
        current_step,
        current_node,
        state,
        status,
        updated_at,
        active_model,
        loop_score,
        error_logs,
        order_text,
        user_id

    FROM checkpoints

    WHERE workflow_id = %s;
    """

    cursor.execute(query, (workflow_id,))

    result = cursor.fetchone()

    if result:

        checkpoint = {
            "workflow_id": result[0],
            "current_step": result[1],
            "current_node": result[2],
            "state": result[3],
            "status": result[4],
            "updated_at": result[5],
            "active_model": result[6],
            "loop_score": result[7],
            "error_logs": result[8],
            "order_text": result[9],
            "user_id": result[10]
        }

        print("Checkpoint Loaded Successfully!")

        cursor.close()
        connection.close()

        return checkpoint

    else:

        print("Checkpoint Not Found!")

        cursor.close()
        connection.close()

        return None


# ============================================================
# GET ALL WORKFLOWS / PREVIOUS ORDERS
# ============================================================

def get_workflow_history(user_id=None):

    connection = get_connection()
    cursor = connection.cursor()

    if user_id:

        query = """
        SELECT
            w.workflow_id,
            w.order_text,
            c.status,
            c.updated_at

        FROM workflows w

        LEFT JOIN checkpoints c
            ON w.workflow_id = c.workflow_id

        WHERE w.user_id = %s

        ORDER BY w.created_at DESC;
        """

        cursor.execute(
            query,
            (user_id,)
        )

    else:

        query = """
        SELECT
            w.workflow_id,
            w.order_text,
            c.status,
            c.updated_at

        FROM workflows w

        LEFT JOIN checkpoints c
            ON w.workflow_id = c.workflow_id

        ORDER BY w.created_at DESC;
        """

        cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ============================================================
# GET ONE WORKFLOW
# ============================================================

def get_workflow(workflow_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        w.workflow_id,
        w.order_text,
        c.current_step,
        c.current_node,
        c.state,
        c.status,
        c.updated_at

    FROM workflows w

    LEFT JOIN checkpoints c
        ON w.workflow_id = c.workflow_id

    WHERE w.workflow_id = %s;
    """

    cursor.execute(
        query,
        (workflow_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


# ============================================================
# GET CHECKPOINT / WORKFLOW HISTORY
# ============================================================

def get_checkpoint_history(workflow_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        step_number,
        node_name,
        state,
        status,
        error_logs,
        created_at

    FROM workflow_history

    WHERE workflow_id = %s

    ORDER BY created_at ASC;
    """

    cursor.execute(
        query,
        (workflow_id,)
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results