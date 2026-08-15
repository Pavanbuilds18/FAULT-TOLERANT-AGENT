import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()


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

    
    connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", "5432")
)
    

    cursor = connection.cursor()

    query = """
    INSERT INTO checkpoints
    (
        workflow_id,
        current_step,
        current_node,
        state,
        status,
        active_model,
        loop_score,
        error_logs
    )

    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

    ON CONFLICT (workflow_id)
    DO UPDATE SET

    current_step = EXCLUDED.current_step,
    current_node = EXCLUDED.current_node,
    state = EXCLUDED.state,
    status = EXCLUDED.status,
    active_model = EXCLUDED.active_model,
    loop_score = EXCLUDED.loop_score,
    error_logs = EXCLUDED.error_logs,
    updated_at = CURRENT_TIMESTAMP;
    """

    cursor.execute(
        query,
        (
            workflow_id,
            current_step,
            current_node,
            json.dumps(state),
            status,
            active_model,
            loop_score,
            error_logs
        )
    )

    connection.commit()

    print("Checkpoint Saved Successfully!")

    cursor.close()
    connection.close()


def load_checkpoint(workflow_id):

    connection = psycopg2.connect(
        host="localhost",
        database="FAULT_TOLERANT_AGENT",
        user="postgres",
        password="REMOVED_SECRET",
        port="5432"
    )

    cursor = connection.cursor()

    query = """
    SELECT * FROM checkpoints
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
            "error_logs": result[8]  
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