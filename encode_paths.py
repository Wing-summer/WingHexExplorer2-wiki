import glob
import os
import re

def replace_image_paths(markdown_file):
    # Read the GitHub repository details from environment variables
    repository = os.getenv("GITHUB_REPOSITORY", "")
    branch = os.getenv("GITHUB_REF_NAME", "")

    if not repository:
        raise ValueError("GITHUB_REPOSITORY environment variable is not set.")
    if not branch:
        raise ValueError("GITHUB_REF_NAME environment variable is not set.")

    # Split repository into username and repo
    username, repo = repository.split("/")

    # Open the markdown file
    with open(markdown_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Regular expression to match Markdown-style image paths: ![alt text](image_path)
    md_img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    # Regular expression to match HTML <img> tags: <img src="image_path" ... />
    html_img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'

    # Function to replace local image path with GitHub URL
    def replace_image(match):
        # For Markdown-style
        if match.re.pattern == md_img_pattern:
            alt_text = match.group(1)
            local_path = match.group(2)
        # For HTML <img> tag
        elif match.re.pattern == html_img_pattern:
            local_path = match.group(1)
            alt_text = ""  # No alt text in <img> tag directly

        # Skip replacement if the URL starts with 'http'
        if local_path.startswith("http"):
            return match.group(0)  # Return the original match if it's a URL

        # Construct GitHub URL
        github_url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{local_path}"

        # Return the new image format (Markdown or HTML)
        if alt_text:
            return f"![{alt_text}]({github_url})"  # Markdown format
        else:
            return f'<img src="{github_url}" />'  # HTML <img> tag format

    # Replace Markdown image paths
    content = re.sub(md_img_pattern, replace_image, content)
    
    # Replace HTML <img> tag image paths
    content = re.sub(html_img_pattern, replace_image, content)

    # Write the updated content back to the file
    with open(markdown_file, "w", encoding="utf-8") as file:
        file.write(content)

# Check for script execution
if __name__ == "__main__":
    md_files = glob.glob("*.md")
    
    for md_file in md_files:
        replace_image_paths(md_file)
        
    exit(0)

    print(">> Update Finished!")
