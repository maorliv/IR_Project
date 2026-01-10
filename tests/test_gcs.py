from google.cloud import storage

client = storage.Client()
bucket = client.bucket("ir-maor-2025-bucket")
def main():
    print("Connected to bucket:", bucket.name)
    blobs = list(client.list_blobs("ir-maor-2025-bucket", prefix="postings_gcp/"))
    print("Number of posting files:", len(blobs))


if __name__ == '__main__':
    main() # run the test