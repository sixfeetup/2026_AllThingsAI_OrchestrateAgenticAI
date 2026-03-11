import os
import sys
from google import genai
from google.genai import types
from PIL import Image

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-image-preview" # Using the fast preview model

if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Prompts and Filenames
PROMPTS = {
    "title-epic-orchestrator.png": "An epic, wide-angle cinematic shot of a vast, misty landscape. In the center, a lone figure (the Orchestrator) stands on a high peak, holding a staff that emits a beam of light into the clouds. Above them, a complex, glowing constellation of interconnected nodes and lines (a task graph) fills the sky. The mood is one of epic scale and strategic depth. High fantasy style, breathtaking lighting, 8k.",
    "quest-artifacts.png": "A digital illustration of a pile of legendary artifacts in a dimly lit treasure room. Included in the pile is a glowing blue crystal shaped like the Docker whale logo, a weathered leather scroll that emits a soft light and shows a database schema, and a heavy iron-bound chest overflowing with glowing blue hard drives. The style should be rich and detailed, like concept art for a high-end RPG.",
    "critical-d20.png": "A high-quality macro photograph. A metallic, iridescent 20-sided die (d20) resting on a dark wood desk. The die shows a '20' on the top face, which is glowing with a faint, magical blue light. In the background, out of focus, is a glowing laptop screen with lines of code. The lighting is warm and cinematic, emphasizing the texture of the metal and the wood.",
    "skills-hologram.png": "A translucent, glowing blue holographic character sheet floating in a dark room. The sheet has categories like 'Strength' and 'Intelligence,' but the specific skills listed are 'Bash Scripting,' 'Security Audit,' 'Git Orchestration,' and 'Neural Mapping.' Some skills are glowing brightly, indicating they have been 'unlocked' or 'leveled up.' The style is high-tech fantasy, clean and futuristic but with a mystical edge.",
    "trap-detected-wizard.png": "A cinematic digital art piece in a high-fantasy style. A wizard in dark robes stands in a shadowy dungeon. Floating in the air before them is a large, glowing parchment contract. The wizard is wearing a translucent blue holographic headset or HUD that is highlighting specific clauses in red, with a warning icon that says 'TRAP DETECTED.' The aesthetic should be a mix of 'The Witcher' and 'Cyberpunk 2077.' High detail, 8k resolution, dramatic lighting.",
    "jetpack-carpet-legion.png": "A surreal digital painting. A sky filled with dozens of people sitting on glowing, flying magic carpets that look like woven circuits. The people are diverse and dressed in a mix of modern business casual and adventurer gear. They are flying toward a futuristic city in the clouds. The style is bright, optimistic, and energetic. 8k resolution, 'Studio Ghibli meets Moebius' aesthetic."
}

def generate_image(filename, prompt):
    print(f"Generating: {filename}...")
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(filename)
                print(f"Successfully saved {filename}")
                return True
        
        print(f"Failed to find image in response for {filename}")
        return False

    except Exception as e:
        print(f"Error generating {filename}: {e}")
        return False

def main():
    # Ensure we are in the images directory or specify it
    os.makedirs("output_images", exist_ok=True)
    
    for filename, prompt in PROMPTS.items():
        path = os.path.join("output_images", filename)
        if os.path.exists(path):
            print(f"Skipping {filename}, already exists.")
            continue
        generate_image(path, prompt)

if __name__ == "__main__":
    main()
