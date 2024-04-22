import torch
from PIL import Image
from clip import clip
import faiss

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Generate embeddings for images and captions
image_embeddings = []
caption_embeddings = []
for img_path, caption in zip(image_paths, captions):
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
    caption_tokens = clip.tokenize([caption]).to(device)

    with torch.no_grad():
        image_embedding = model.encode_image(image)
        caption_embedding = model.encode_text(caption_tokens)

    image_embeddings.append(image_embedding.cpu().numpy())
    caption_embeddings.append(caption_embedding.cpu().numpy())

# Build FAISS index
index = faiss.IndexFlatL2(model.visual.output_dim)
index.add(np.concatenate(image_embeddings, axis=0))

# Search function
def search(query):
    with torch.no_grad():
        query_tokens = clip.tokenize([query]).to(device)
        query_embedding = model.encode_text(query_tokens)

    distances, indices = index.search(query_embedding.cpu().numpy(), k=10)
    matching_images = [image_paths[idx] for idx in indices[0]]
    return matching_images
