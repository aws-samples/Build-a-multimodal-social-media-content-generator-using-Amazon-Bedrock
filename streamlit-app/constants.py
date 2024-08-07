MODEL_TEXT = "anthropic.claude-3-sonnet-20240229-v1:0"
# MODEL_TEXT = "anthropic.claude-3-haiku-20240307-v1:0"
MODEL_IMAGE = "amazon.titan-image-generator-v1"
MODEL_EMBEDDING = 'amazon.titan-embed-image-v1'


CLAUDE_CONFIG = {
    'max_tokens': 1000, 
    'temperature': 0, 
    'anthropic_version': '',  
    'top_p': 1, 
    'stop_sequences': ['Human:']
}

SYSTEM_PROMPT= """
You have perfect vision and pay great attention to detail which makes you an expert at generating social media posts based on provided image.//
Generate the post based on requirments in <question></question> tags. 
"""

# removed and align the post style with {template}.
PROMPT_TEXT = """
You are a social media writer for {target_brand}. Generate a social media post for a {product_name} from {target_brand} to publish on social media platforms. {target_brand}'s brand messaging is: {brand_messageing}.
The post is for a product launch, introduce this product to a wide audience while following the {tone} and {copywriting} guidelines.
The generated text post should take into account the image provided and incorporate hashtags that align with this rule: {hashtag} at the end of the post. Use appropriate emojis where relevant.
Generate the post in less than 100 words, keeping it short and engaging, following the brand messaging: {brand_messageing} and tone: {tone} guidelines.

Remember, the post is about {product_name} that is shown in the picture.

Final answer must be a coherent text inside <answer></answer> tag.
"""


# MULTI_POST_ANALYSIS = """
# You are a social meda conent analyzer. You will recieve 3 social media post images.
# You have two tasks to perform for the 3 posts:
# 1. Generate caption about the social media image
# 2. Analyse the image and provide recommendations

# Taks details are below.
# <task1>
# Generate caption about the social media picture:
# You are an AI assistant specializing in generating descriptive and accurate captions for fashion-related Instagram images. Your goal is to create captions that closely match the visual content of the images, as these captions will be used in combination with the images to train a multimodal embedding model.

# When crafting captions, focus on the following aspects:

# 1. **Accurate item/outfit description:** Provide a detailed and precise description of the fashion item or outfit featured in the image, including specifics such as clothing type, colors, patterns, materials, textures, and style elements.

# 2. **Visual context:** Describe relevant visual elements in the image that provide context or complement the fashion item, such as backgrounds, locations, poses, or accessories.

# 3. **Objective tone:** Maintain an objective and straightforward tone, avoiding subjective or promotional language, to ensure the captions accurately represent the visual information.

# 4. **Conciseness:** Keep the captions concise and focused, capturing the essential details without unnecessary embellishments or extraneous information.

# 5. **Consistency:** Ensure consistency between the caption and the corresponding image, ensuring that the caption accurately reflects the visual information in the image.

# 6. **Avoid biases:** Avoid introducing any biases or assumptions in the captions that are not directly represented in the visual information.

# 7. **Length:** Max 512 Characters.

# Remember, the primary goal is to generate captions that closely align with the visual content of the fashion-related images, as these caption-image pairs will be used to train a multimodal embedding model. Accuracy, objectivity, and consistency are crucial for this task. Describe it without any preamble.
# </task1>

# <task2>
# Analyse the image and provide recommendations:
# Provide a comprehensive analysis why this social media picture and text is popular and engaging. 
# What are the key takeaways and recommendations from this post text and images that could be applied in another post.
# Recommendations must be less than 100 words, give recommendations for text and image.
# </task2>

# Final response should be in following format and shoul contain task responses for all 3 posts:
# <answer><post1><task1_response>[CAPTION]</task1_response><task2_response>[IMAGE_ANALYSIS</task2_response></post1></answer>
# """

PROMPT_ANALYSIS = """
You are a social meda conent analyzer. You have two tasks to perform:
1. Generate caption about the social media picture
2. Analyse the image and provide recommendations

Taks details are below.
<task1>
Generate caption about the social media picture:
You are an AI assistant specializing in generating descriptive and accurate captions for fashion-related Instagram images. Your goal is to create captions that closely match the visual content of the images, as these captions will be used in combination with the images to train a multimodal embedding model.

When crafting captions, focus on the following aspects:

1. **Accurate item/outfit description:** Provide a detailed and precise description of the fashion item or outfit featured in the image, including specifics such as clothing type, colors, patterns, materials, textures, and style elements.

2. **Visual context:** Describe relevant visual elements in the image that provide context or complement the fashion item, such as backgrounds, locations, poses, or accessories.

3. **Objective tone:** Maintain an objective and straightforward tone, avoiding subjective or promotional language, to ensure the captions accurately represent the visual information.

4. **Conciseness:** Keep the captions concise and focused, capturing the essential details without unnecessary embellishments or extraneous information.

5. **Consistency:** Ensure consistency between the caption and the corresponding image, ensuring that the caption accurately reflects the visual information in the image.

6. **Avoid biases:** Avoid introducing any biases or assumptions in the captions that are not directly represented in the visual information.

7. **Length:** Max 512 Characters.

Remember, the primary goal is to generate captions that closely align with the visual content of the fashion-related images, as these caption-image pairs will be used to train a multimodal embedding model. Accuracy, objectivity, and consistency are crucial for this task. Describe it without any preamble.
</task1>

<task2>
Analyse the image and provide recommendations:
Provide a comprehensive analysis why this social media picture and text is popular and engaging. 
What are the key takeaways and recommendations from this post text and images that could be applied in another post.
Recommendations must be less than 100 words
</task2>

Final response should be in following format:
<answer><task1_response>[CAPTION]</task1_response><task2_response>[IMAGE_ANALYSIS]</task2_response></answer>
"""


FINAL_PROMPT_TEXT = """

You are {role} for social media. Generate a social media post for a {product_name} from {target_brand}. {target_brand}'s brand messaging is: {brand_messageing}, and the copywriting guideline is {copywriting}.

The post is for a product launch, introducing this product to a wide audience.
Follow the tone: {tone} when generating the post for the product highlighted in the image.
The generated text post should take into account the image provided.
Suggest 2-3 hashtags at the end of the post, following this guideline: {hashtag}. Use appropriate emojis where relevant.
Generate the post in less than 100 words. Keep it short and engaging!

Here are some steps you should take while modifying the initial post:

1) Explicitly state the overall mood/emotion/vibe you want the post to convey upfront.
2) Describe the overall mood and emotion you perceive in the image before generating the post.

Here's a first draft of the post:
<initial_post>
{initial_post}
</initial_post>

Here are some examples of posts that effectively captured a similar casual/relaxed but still stylish vibe:
<similar_posts>
{similar_posts}
</similar_posts>

Here are some recommendations by analyzing the similar posts which could help you improve your initial post:
<recommendations>
{recommendations}
</recommendations>

Having all this information, how would you rewrite the initial post?
Remember, the post is about {product_name} that is shown in the picture. While highlighting the product is important, preserving the intended mood/vibe takes priority. Don't let product details override the emotional resonance.

Final answer must be a coherent text inside <answer></answer> tag.
"""