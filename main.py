"""Entry point demonstrating the LLM‑driven Fluent worklist workflow.

This script shows how the components of the fluent_robot package can be
chained together to translate a natural language description into a
compiled Fluent worklist and simulate its execution.  It performs the
following steps:

1. Use the llm_stub to convert an English description into an IR job.
2. Validate the IR job against a simple deck_state.
3. Compile the IR into .gwl lines.
4. Simulate execution of the job and display resulting volumes.

Run this script directly to see a demonstration.  In a real system,
natural language input would be provided by users or other applications.
"""

from fluent_robot import plan_from_text, JobManager


def main():
    # Example task description.  You can modify this string to test
    # other phrases supported by the stub.
    description = "Transfer 50 uL from plate S1 A1 to plate D1 B1, wash, then decontaminate."
    print(f"Task description: {description}\n")
    # Step 1: LLM planning (stubbed)
    job = plan_from_text(description)
    print("Generated IR job:")
    for step in job.steps:
        print(f"  {step.id} – op={step.op}, args={step.args}")
    print()
    # Step 2: Set up deck_state.  In a real system this would be read
    # from the robot's deck configuration.  Here we assume S1 and D1 are present.
    deck_state = {"S1": {}, "D1": {}}
    manager = JobManager(deck_state=deck_state)
    # Step 3: Submit job (runs preflight check)
    try:
        manager.submit(job)
    except ValueError as e:
        print("Preflight validation failed:")
        print(e)
        return
    # Step 4: Compile and simulate
    worklist, sim_state = manager.run_next()
    print("Compiled worklist lines:\n")
    for line in worklist:
        print(line)
    print("\nSimulation state (delta volumes):")
    for labware, volumes in sim_state.items():
        # Print total volume per labware for brevity
        total_vol = sum(volumes)
        print(f"  {labware}: total volume = {total_vol} µL")


if __name__ == "__main__":
    main()