CREATE TABLE IF NOT EXISTS checkpoints (
    workflow_id VARCHAR(100) PRIMARY KEY,
    current_step INTEGER,
    current_node VARCHAR(100),
    state JSONB,
    status VARCHAR(50),
    active_model VARCHAR(100),
    loop_score FLOAT,
    error_logs TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO checkpoints
(workflow_id, current_step, current_node, state, status, active_model, loop_score, error_logs)
VALUES
(
    'A101',
    4,
    'Formatter',
    '{"task": "Generate Report", "progress": "100%"}',
    'Completed',
    'GPT-4',
    0.0,
    ''
)
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
    