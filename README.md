# Loom

Loom is a lightweight, local version control system built from scratch in pure Python. 

This project is an architectural exploration of how version control systems (like Git) work under the hood, focusing on file system management, data hashing, and graph-based commit histories. 

## Current Status
**Phase 1: Initialization**
Loom currently supports the foundational setup phase. 

### Commands
* `python loom.py init` 
  Initializes a new Loom repository. This creates the hidden `.loom` directory structure (the vault) and sets up the initial `HEAD` reference to track the main branch. It includes safe edge-case handling to prevent overwriting an existing repository.

## Future Roadmap
* **Phase 2:** Content-Addressable Database (SHA-1 hashing and blob storage)
* **Phase 3:** The Staging Area (Building the index)
* **Phase 4:** Capturing the Tree (Directory structures as objects)
* **Phase 5:** The Immutable Snapshot (Commits and history traversal)
