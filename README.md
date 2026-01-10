Wikipedia Search Engine
1. Project Overview
This project is a scalable search engine for the English Wikipedia, developed as part of an Information Retrieval course. It is designed to handle retrieval and ranking of millions of documents using a distributed architecture on the Google Cloud Platform (GCP).

The system features a Python-based backend (Flask) that interfaces with inverted indexes and metadata stored in Google Cloud Storage (GCS). The design emphasizes modularity, separation of concerns, and cloud-native data access.

2. System Architecture
The project follows a modular architecture to separate the web layer, business logic, data access, and ranking algorithms.

Key Components
Frontend (search_frontend.py): A Flask-based web server that exposes the REST API. It handles incoming HTTP requests and delegates search logic to the controller.
Controller (controllers/SearchController.py): The core orchestration layer. It manages the flow of:
Tokenizing the user query via text_processor.
Fetching relevant postings and metadata via data_provider.
Calculating relevance scores via ranker.
Data Provider (data_provider/): An abstraction layer for data access. It handles loading inverted indexes, PageRank scores, and document titles directly from GCS buckets, ensuring the application remains stateless.
Ranker (ranker/): Contains implementations of ranking algorithms (BM25) and score accumulation logic.
Text Processor (text_processor/): Handles query tokenization and normalization to match the indexing strategy.
3. Data & Indexes
The system does not store the full inverted index locally on the VM's disk. Instead, it streams data from Google Cloud Storage on demand or pre-loads necessary structures into memory.

Storage Location: Data is hosted in a GCS bucket (configured in search_frontend.py).
Inverted Index: Stored as pickle and bin files in the postings_gcp/ directory of the bucket.
PageRank: Pre-computed PageRank scores for all Wikipedia articles are stored in the pr/ directory.
Metadata: Mappings from document IDs to titles are maintained in id_to_title/.
4. Ranking & Retrieval
The search engine employs a composite ranking strategy to balance textual relevance with global document popularity.

Retrieval: The system uses a specialized inverted index to identify candidate documents containing query terms.
Ranking Algorithm:
BM25: Used as the primary scoring metric for textual relevance (default weight: 0.8).
PageRank: Integrated into the final score to boost high-quality, authoritative pages (default weight: 0.2).
Optimization: A ScoreAccumulator is used to efficiently aggregate scores across multiple query terms.
5. Deployment on GCP
The system runs on a Google Compute Engine (GCE) VM instance.

VM Requirements
Operating System: Debian/Ubuntu (Standard GCP images).
Memory: High-memory machine type recommended (e.g., n1-standard-4 or n2-highmem-4) to accommodate index dictionaries and posting lists in RAM if caching is enabled.
Network: Allow HTTP traffic on port 8080 (or your configured port).
Managing the VM
To avoid unnecessary cloud charges, always stop the VM when not in use.

Start the VM:

gcloud compute instances start <YOUR_INSTANCE_NAME> --zone=<YOUR_ZONE>
Stop the VM:

gcloud compute instances stop <YOUR_INSTANCE_NAME> --zone=<YOUR_ZONE>
Running the Application
SSH into the VM:

gcloud compute ssh <YOUR_INSTANCE_NAME> --zone=<YOUR_ZONE>
Activate Environment & Run:

# Navigate to project directory
cd IR_Project

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python search_frontend.py
The server will start on 0.0.0.0:8080.

6. API Usage
The search engine exposes a single endpoint for queries.

Search Endpoint
GET /search

Parameters:

query (string): The search query.
Example Request:

http://<EXTERNAL_IP>:8080/search?query=computer+science
Response Format: Returns a JSON list of tuples, where each tuple contains (doc_id, title).

[
  [12345, "Computer Science"],
  [67890, "Alan Turing"],
  ...
]
7. Testing
The repository includes a comprehensive test suite in the tests/ directory to ensure system correctness.

Run tests using pytest or unittest.
Tests cover BM25 logic, query tokenization, and data provider integrity.
8. Notes & Design Decisions
Cloud-Native Storage: Reading directly from GCS introduces latency but allows for virtually unlimited storage scale without managing local disks.
No Caching: By default, the system minimizes local caching to simulate a stateless production environment, though memory mapping is used for index files where applicable.
Cost Efficiency: The architecture allows the expensive compute resources (VM) to be shut down while preserving data in cheap object storage (GCS).
