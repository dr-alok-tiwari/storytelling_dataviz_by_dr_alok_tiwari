# Concurrency and Streamlit Community Cloud

The application is designed for concurrent classroom access, with the following safeguards:

- session-specific progress and widget state through `st.session_state`;
- deterministic, cached synthetic datasets returned as safe per-call copies;
- lazy execution of session tabs so hidden Concept, Demo, Lab, Quiz, and Reflect bodies do not all run together;
- NumPy-based linear trend lines instead of the heavier statsmodels/SciPy runtime stack;
- automated verification of independent Streamlit session state;
- automated stress coverage for eight simultaneous chart-generation workloads using the shared cached datasets.

## Important hosting limitation

Streamlit Community Cloud uses a shared resource envelope. It does not provide a guaranteed number of simultaneous users, and available CPU and memory can vary. Passing the session-isolation and eight-worker stress tests demonstrates application-level concurrency safety, but it is not a service-level guarantee for every classroom network or Cloud allocation.

For a high-stakes live class, open the app shortly before the session, verify the health of the deployment, and keep the Streamlit Cloud logs open. If the class size is large or usage is assessment-critical, deploy the same repository to a dedicated container service with fixed memory and CPU.
