# 📖 Overview
Video Language Models (VLMs) often struggle with fine-grained visual clues, which are crucial for accurately answering Video Question Answering (Video QA) tasks.
These models tend to rely on coarse global representations, leading to failures in understanding subtle object-level details.

This project explores a simple yet effective idea:

**Can improving object-level visual focus help VLMs better understand fine-grained information in videos?**

# 💡 Motivation
Many Video QA failures occur because:

 - Important objects are small or localized
 - Models fail to attend to relevant regions
 - Global video representations dilute critical visual cues

To address this, we investigate whether **explicit object-level** inputs can improve performance.

# ⚙️ Approach
## 1. Object Detection (Attempt)

We first attempted to:

 - Detect objects in video frames using an object detector
 - Crop detected regions
 - Feed them into a VLM

However, the object detector failed to reliably capture relevant regions for fine-grained reasoning.

## 2. Manual Cropping (Key Observation)

To isolate the effect of object-level information, we manually:

 - Selected relevant regions from video frames
 - Cropped objects of interest
 - Performed captioning and QA using these cropped inputs

👉 Result:

 - The model showed significantly improved understanding of fine-grained details
This suggests that object-level representations are indeed critical

# 🧪 Key Insight

Even though automatic object detection failed,
manual experiments confirm that:

**Providing object-centric inputs can substantially improve fine-grained reasoning in VLMs.**

This highlights a gap between:

 - Detection quality
 - Reasoning capability

# 📂 Code Structure
### Object Detection
Code for running object detection on video frames using BoT-SORT
### Cropping Pipeline
Extracts object regions from detected bounding boxes
### VLM Inference
Runs inference using LLaVA-Video
Evaluates responses on Video QA tasks

# ⚠️ Limitations
 - Object detection is not reliable for fine-grained cues
 - Manual cropping is not scalable
 - No end-to-end training (pipeline-based approach)
