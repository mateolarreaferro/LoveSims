import kagglehub

# Download latest version
path = kagglehub.dataset_download("annavictoria/speed-dating-experiment")

print("Path to dataset files:", path)